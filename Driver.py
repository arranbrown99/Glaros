"""
This class represents the main program that will be running on the current CSP.
Every so often it will compare tbe stock prices of all available
CSPs (through StockRetriever) and it will decide when it's time to
move/migrate to another CSP.

--- Event Loop ---

Driver running on Azure VM.
Periodically check the StockReceiver - list of cloud providers, static String
for the Stock Exchange name.
Decide to move to AWS.
Create the object for AWS.
If vm not turned on:

Start aws vm.

Send using python scp script - the SSH keys are set up before hand and
not handled by the script.
Run the newly made driver on the remote VM with a flag for which VM
we're currently on.
Old driver stops.

Once the new driver successfully migrates.
Delete old driver on the now remote vm
Stop now remote vm
update dns
restart the event loop

"""
import sys
import threading
import os
import time
import sqlite3
import json
from datetime import datetime
import dns

from glaros_ssh import remote_process, vm_scp

from cloud_service_providers.AbstractCSP import AbstractCSP
from cloud_service_providers.AwsCSP import AwsCSP
from cloud_service_providers.AzureCSP import AzureCSP
from cloud_service_providers.GoogleCSP import GoogleCSP
import StockRetriever

sys.path.append(os.path.abspath('./dashboard/'))

from dashboard.settings import GENERAL_INFO_FILE

counter = 0  # used in dummy condition to move after 4 calls to migrate()
check_every = 15 * 60  # seconds
# Files not to be uploaded to receiving VMs
exclude_files = ['.git', 'gunicorn.sock', 'admin', '__pycache__']


class Error(Exception):
    '''
    Base class for exceptions
    '''
    pass


class MigrationError(Error):
    '''
    Exception raised for errors in the migration.

    Attributes
    ------
        message -- explanation of the error
    '''

    def __init__(self, message):
        self.message = message


def event_loop(currently_on):
    """
    Periodically check the stock prices and decide what CSP to move to.

    Parameters
    ----------
    currently_on: the CSP object that is the current vm being ran on passed in through command line arguments
    """
    current = currently_on.get_stock_name()

    # Logic to decide when to move
    cloud_service_providers = AbstractCSP.get_stock_names()
    best_stock = StockRetriever.best_stock(cloud_service_providers)
    print(best_stock + " is the current best stock price")
    print("Is it time to move?")

    if current != best_stock:

        print("Yes! Migrating...")
        print("Moving from " + current + " to " + best_stock)
        # Start migration process
        print("Now migrating to " + best_stock)
        try:
            migrate(best_stock, currently_on)
        except MigrationError as e:
            raise e


    else:
        print("not now!")
        print()
        # If it's not time to move we start the Timer again.
        threading.Timer(check_every, event_loop, [currently_on]).start()


def write_log_before(sender, target):
    """
    Write to a log file the time we start moving

    Parameters
    ----------
    sender: the CSP we are moving to
    target : the CSP we are currently on
    """
    with open('migrations.log', 'a') as migrations_log:
        migrations_log.write(str(datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S")) + " Starting migration from %s to %s...\n" %
                             (sender.get_formal_name(), target.get_formal_name()))


# Write to logfile once migration finishes
def write_log_after(sender, target):
    """
        Write to a log file the time we finish moving meaning we can see how long a migration takes

    Parameters
    ----------
    sender: the CSP we are moving to
    target : the CSP we are currently on
    """
    with open('migrations.log', 'a') as migrations_log:
        migrations_log.write(str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) +
                             " Finished migration from %s to %s.\n" % (
                                 sender.get_formal_name(), target.get_formal_name()))


def boot_vm(moving_to):
    """
    start remote vm

    Parameters
    ----------
    moving_to: the CSP we are moving to
    """
    if moving_to.is_running() is False:
        print("Turning on " + moving_to.get_stock_name() + " vm.")
        moving_to.start_vm()
    # wait 30 seconds so as to let the remote vm start up
    time.sleep(30)


def run_booted_vm(moving_to, currently_on):
    """
    start runglaros on the remote machine, start the new driver

    Parameters
    ----------
    moving_to: the CSP we are moving to
    currently_on : the CSP we are currently on
    """
    try:
        remote_process.remote_python(
            moving_to.get_ip(),
            moving_to.get_username(),
            "runglaros " +
            moving_to.get_stock_name() + " " + currently_on.get_stock_name())
    except Exception as e:
        raise MigrationError(e)


def migrate(stock_name, currently_on):
    """
    Logs where we are and where we are going
    Starts remote vm
    Sends

    Parameters
    ----------
    stock_name : stock name of the CSP we are going to move to
    currently_on : the CSP we are currently on


    Returns
    -------
    when the migration ends at which point the new driver on the remote vm will take over
    """
    retry_counter = 20
    while retry_counter > 0:
        try:
            update_general_info(GENERAL_INFO_FILE, currently_on, "Migrating")

            moving_to = AbstractCSP.get_csp(stock_name)
            # Write to logfile
            write_log_before(currently_on, moving_to)
            print("Moving to " + moving_to.get_stock_name())
            # Log migration to database
            database_entry(currently_on, moving_to)
            # start VM
            boot_vm(moving_to)
            print("Remote vm started up, ip address is " + moving_to.get_ip())
            # files to be sent
            # start sending entire directory of project
            ignore(moving_to)

            # run the Driver on newly started VM and send the current CSP provider
            run_booted_vm(moving_to, currently_on)
            return
        except MigrationError as e:
            print(e)
            update_general_info(GENERAL_INFO_FILE, currently_on, "Running")

        except sqlite3.Error as e:
            print(e)
            update_general_info(GENERAL_INFO_FILE, currently_on, "Running")
        retry_counter -= 1
        time.sleep(30)
    raise MigrationError("Failed to migrate")


def database_entry(currently_on, moving_to):
    """

    Update information about time and location of migration for front end

    Parameters
    ----------
    moving_to: the CSP we are moving to
    currently_on : the CSP we are currently on
    """
    # Log migration to database
    connection = None
    try:
        now = datetime.now()
        connection = sqlite3.connect('./dashboard/db.sqlite3')
        print("The sqlite3 connection is established.")
        cursor = connection.cursor()
        insert_query = """ INSERT INTO dashboard_app_migrationentry (_from,_to,_date) VALUES ('%s', '%s', '%s')""" \
                       % (currently_on.get_formal_name(), moving_to.get_formal_name(),
                          now.strftime("%Y-%m-%d, %H:%M:%S"))
        cursor.execute(insert_query)
        connection.commit()
        cursor.close()

    except sqlite3.Error as e:
        raise e
    finally:
        if connection:
            connection.close()
            print("The sqlite3 connection is now closed.")


def after_migration(sender, currently_on):
    """
    Ran on the new driver
    Deletes files from sender then
    Stops senders vm
    then updates log

    Parameters
    ----------
    sender : the CSP that we started on
    currently_on : the CSP we are now on
    """
    # delete old driver on now remote vm
    parent_dir_path = os.path.abspath('.')
    parent_dir = os.path.basename(parent_dir_path)
    print("Deleting " + parent_dir +
          " from " + sender.get_stock_name() + " vm.")
    remote_process.remote_remove(
        sender.get_ip(),
        sender.get_username(),
        parent_dir)
    # stop vm
    if sender.is_running():
        print("Turning off " + sender.get_stock_name() + " vm.")
        sender.stop_vm()

    # Update logfile
    write_log_after(sender, currently_on)


def update_general_info(file, currently_on, status):
    """

    Updates the status of the project ie Running or Migrating and current ip

    Parameters
    ----------
    file : the file that is the status of the project
    currently_on : CSP we are currently on
    status : ie Running or Migrating
    """
    data = {"GLAROS_CURRENTLY_ON": currently_on.formal_name,
            "GLAROS_CURRENT_STATUS": status,
            "GLAROS_CURRENT_IP": currently_on.get_ip(),
            "GLAROS_CURRENTLY_ON_COLOUR": currently_on.ui_colour}

    with open(file, "w") as jsonFile:
        json.dump(data, jsonFile)


def ignore(moving_to):
    """
    Sends files to remote vm if said file is not in the blacklist

    Parameters
    ----------
    moving_to : CSP we are going to move to
    """
    parent_dir = os.path.abspath('.')
    remote_filepath = os.path.basename(parent_dir)
    try:
        ignore_helper(parent_dir, moving_to, remote_filepath)
    except Exception as e:
        raise MigrationError(e)


def ignore_helper(parent_dir, moving_to, remote_filepath):
    """
    helper function for ignore
    guarantees the folder exists on the remote vm, as scp does not create
    this directory

    Parameters
    ----------
    parent_dir : the parent directory of the current file
    moving_to : CSP we are moving to
    remote_filepath : the filepath the file will be sent to
    """
    remote_process.remote_mkdir(
        moving_to.get_ip(),
        moving_to.get_username(),
        remote_filepath)
    files_to_upload = [f for f in os.listdir(parent_dir) if f not in exclude_files]
    try:
        for _file in files_to_upload:
            print("Uploading -> " + _file)
            path_to_file = os.path.join(parent_dir, _file)
            if os.path.isdir(path_to_file):
                ignore_helper(path_to_file, moving_to, os.path.join(remote_filepath, _file))
            else:
                vm_scp.upload_file(path_to_file,
                                   moving_to.get_ip(),
                                   moving_to.get_username(),
                                   remote_path="~/" + remote_filepath + "/" + _file,
                                   recursive=False)
    except Exception as e:
        raise MigrationError(e)


def main():
    """
    First we need to identify on which CSP this Driver was created from
    Achieved through command line arguments

    """
    try:

        if len(sys.argv) == 2:
            currently_on = AbstractCSP.get_csp(sys.argv[1])
        elif len(sys.argv) == 3:
            currently_on = AbstractCSP.get_csp(sys.argv[1])
            came_from = AbstractCSP.get_csp(sys.argv[2])

            update_general_info(GENERAL_INFO_FILE, currently_on, "Migrating")
            after_migration(came_from, currently_on)
        else:
            raise AbstractCSP.InvalidCSPError(sys.argv,
                                              "Please enter a valid CSP stock name")
    except AbstractCSP.InvalidCSPError as e:
        return e.message + e.expression

    # Update the General Information file
    update_general_info(GENERAL_INFO_FILE, currently_on, "Running")
    print("Currently on " + currently_on.get_stock_name())
    print()
    # update dns
    print("Updating DNS")
    dns.change_ip(currently_on.get_ip())

    # Start checking the stock prices and decide when to migrate
    try:
        event_loop(currently_on)
    except MigrationError as e:
        return e

    return 0


if __name__ == '__main__':
    sys.exit(main())
