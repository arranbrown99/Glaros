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
import StockRetriever

sys.path.append(os.path.abspath('./dashboard/'))

from dashboard.settings import GENERAL_INFO_FILE

counter = 0  # used in dummy condition to move after 4 calls to migrate()
check_every = 15 * 60  # seconds
# Files not to be uploaded to receiving VMs
exclude_files = ['.git', '.gitlab-ci.yml', '__pycache__']


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
        migrate(best_stock, currently_on)

    else:
        print("not now!")
        print()
        # If it's not time to move we start the Timer again.
        threading.Timer(check_every, event_loop, [currently_on]).start()


def write_log_before(sender, target):
    with open('migrations.log', 'a') as migrations_log:
        migrations_log.write(str(datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S")) + " Starting migration from %s to %s...\n" %
                             (sender.get_formal_name(), target.get_formal_name()))


# Write to logfile once migration finishes
def write_log_after(sender, target):
    with open('migrations.log', 'a') as migrations_log:
        migrations_log.write(str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) +
                             " Finished migration from %s to %s.\n" % (
                                 sender.get_formal_name(), target.get_formal_name()))


# boot VM on another CSP / abstracted from migrate()
def boot_vm(moving_to):
    if moving_to.is_running() is False:
        print("Turning on " + moving_to.get_stock_name() + " vm.")
        moving_to.start_vm()
    time.sleep(30)


# run Driver.py on VM / abstracted from migrate()
def run_booted_vm(moving_to, currently_on):
    try:
        remote_process.remote_python(
            moving_to.get_ip(),
            moving_to.get_username(),
            "runglaros " +
            currently_on.get_stock_name() + " " + moving_to.get_stock_name())
    except Exception as e:
        raise MigrationError(e)


def migrate(stock_name, currently_on):
    try:
        update_general_info(GENERAL_INFO_FILE, currently_on, "Migrating")
        # Write to logfile
        write_log_before(currently_on, stock_name)
        # create object for 'best' stock
        moving_to = AbstractCSP.get_csp(stock_name)
        print("Moving to " + moving_to.get_stock_name())
        # Log migration to database
        database_entry(currently_on, moving_to)
        # start VM
        boot_vm(moving_to)
        parent_dir = os.path.abspath('.')
        remote_filepath = os.path.basename(parent_dir)

        # guarantees the folder exists on the remote vm, as scp does not create
        # this directory
        remote_process.remote_mkdir(
            moving_to.get_ip(),
            moving_to.get_username(),
            remote_filepath)

        print("Remote vm started up, ip address is " + moving_to.get_ip())
        # files to be sent
        # start sending entire directory of project
        ignore(parent_dir, moving_to, remote_filepath)

        # run the Driver on newly started VM and send the current CSP provider
        run_booted_vm(moving_to, currently_on)
    except MigrationError as e:
        print(e)
        update_general_info(GENERAL_INFO_FILE, currently_on, "Running")
        event_loop(currently_on)
    except sqlite3.Error as e:
        print(e)
        update_general_info(GENERAL_INFO_FILE, currently_on, "Running")
        event_loop(currently_on)


def database_entry(currently_on, moving_to):
    # Log migration to database
    connection = None
    try:
        now = datetime.now()
        connection = sqlite3.connect('./dashboard/db.sqlite3')
        print("The sqlite3 connection is established.")
        cursor = connection.cursor()
        insert_query = """ INSERT INTO dashboard_app_migrationentry (_from,_to,_date) VALUES ('%s', '%s', '%s')""" \
                       % (currently_on.get_formal_name(), moving_to.get_formal_name(),
                          now.strftime("%Y-%m-%d"))
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
    write_log_after(sender.get_stock_name(), currently_on.get_stock_name())


def update_general_info(file, currently_on, status):
    data = {"GLAROS_CURRENTLY_ON": currently_on.formal_name,
            "GLAROS_CURRENT_STATUS": status,
            "GLAROS_CURRENT_IP": currently_on.get_ip(),
            "GLAROS_CURRENTLY_ON_COLOUR": currently_on.ui_colour}

    with open(file, "w") as jsonFile:
        json.dump(data, jsonFile)


def ignore(parent_dir, moving_to, remote_filepath):
    files_to_upload = [f for f in os.listdir(path='.') if f not in exclude_files]
    try:
        for _file in files_to_upload:
            print("Uploading -> " + _file)
            if os.path.isdir(_file):
                recursive = True
            else:
                recursive = False
            vm_scp.upload_file(os.path.join(parent_dir, _file),
                               moving_to.get_ip(),
                               moving_to.get_username(),
                               remote_path="~/" + remote_filepath + "/" + _file,
                               recursive=recursive)
    except Exception as e:
        raise MigrationError(e)


def main():
    # First we need to identify on which CSP this Driver was created from
    try:
        if len(sys.argv) == 2:
            currently_on = AbstractCSP.get_csp(sys.argv[1])

        elif len(sys.argv) == 3:
            came_from = AbstractCSP.get_csp(sys.argv[1])
            currently_on = AbstractCSP.get_csp(sys.argv[2])
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
    event_loop(currently_on)
    return 0

if __name__ == '__main__':
    sys.exit(main())
