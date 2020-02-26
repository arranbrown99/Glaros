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

from glaros_ssh import remote_process, vm_scp
from cloud_service_providers.AwsCSP import AwsCSP
from cloud_service_providers.AzureCSP import AzureCSP
from cloud_service_providers.GoogleCSP import GoogleCSP
from datetime import datetime
import StockRetriever
import dns

sys.path.append(os.path.abspath('./dashboard/'))

from dashboard.settings import GENERAL_INFO_FILE

counter = 0  # used in dummy condition to move after 4 calls to migrate()
check_every = 15 * 60  # seconds
cloud_service_providers = [
    'amzn',  # Amazon (AWS)
    'msft',  # Microsoft (Azure)
    'goog',  # Google (GCP)
]
# Files not to be uploaded to receiving VMs
exclude_files = ['.git', '.gitlab-ci.yml', '__pycache__']
# dictionary of stock objects - ca n be expanded to include "goog"
stock_objs = {"amzn": AwsCSP(), "msft": AzureCSP(),"goog": GoogleCSP()}


def event_loop(currently_on):
    current = currently_on.get_stock_name()

    # Logic to decide (using StockRetriever)
    best_stock = StockRetriever.best_stock(cloud_service_providers)
    print(best_stock + " is the current best stock price")
    print("Is it time to move?")

    if current != best_stock:

        print("Yes! Migrating...")
        print("Moving from " + current + " to " + best_stock)
        # Start migration process
        print("Now migrating to " + best_stock)
        migrate(best_stock, currently_on)

    #    elif counter == 10:
    #        if current == 'amzn':
    #            best_stock = 'msft'
    #        else:
    #            best_stock = 'amzn'
    #
    #        move = True
    #        print("For demos sake took too long will 'migrate' any way")
    #        print("Moving from " + current + " to " + best_stock)
    #        migrate(best_stock,currently_on)

    else:
        print("not now!")
        print()
        # If it's not time to move we start the Timer again.
        threading.Timer(check_every, event_loop, [currently_on]).start()


#        counter += 1


def write_log_before(sender, target):
    with open('migrations.log', 'a') as migrations_log:
        migrations_log.write(str(datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S")) + " Starting migration from %s to %s...\n" %
                             (sender, target))


# Write to logfile once migration finishes
def write_log_after(sender, target):
    with open('migrations.log', 'a') as migrations_log:
        migrations_log.write(str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) +
                             " Finished migration from %s to %s.\n" % (sender, target))


# Create object for best stock
def create_stock_object(stock_name):
    obj = stock_objs.get(stock_name)
    return obj


# boot VM on another CSP / abstracted from migrate()
def boot_vm(moving_to):
    if (moving_to.is_running() is False):
        try:
            print("Turning on " + moving_to.get_stock_name() + " vm.")
            moving_to.start_vm()
        except BaseException:
            print("Failed to start VM.")
            return
    time.sleep(30)


# run Driver.py on VM / abstracted from migrate()
def run_booted_vm(moving_to, currently_on):
    try:
        remote_process.remote_python(
            moving_to.get_ip(),
            moving_to.get_username(),
            "runglaros from_" +
            currently_on.get_stock_name())
    except Exception as e:
        print(e)
        print("Failed to run Driver.py on new VM.")
        return


def migrate(stock_name, currently_on):
    # Write to logfile
    write_log_before(currently_on, stock_name)
    # create object for 'best' stock
    moving_to = create_stock_object(stock_name)
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
    files_to_upload = [f for f in os.listdir() if f not in exclude_files]
    # start sending entire directory of project
    try:
        #   parent_dir = os.path.dirname(os.path.realpath(__file__))
        for _file in files_to_upload:
            print("Uploading -> " + _file)
            if os.path.isdir(_file):
                recursive = True
            else:
                recursive = False
            vm_scp.upload_file(
                os.path.join(
                    parent_dir,
                    _file),
                moving_to.get_ip(),
                moving_to.get_username(),
                remote_path="~/" +
                            remote_filepath +
                            "/" +
                            _file,
                recursive=recursive)
    except Exception as e:
        print(e)
        print("Could not move directory")
        return

    # run the Driver on newly started VM and send the current CSP provider
    run_booted_vm(moving_to, currently_on)


def database_entry(currently_on, moving_to):
    # Log migration to database
    try:
        now = datetime.now()
        connection = sqlite3.connect('./dashboard/db.sqlite3')
        print("The sqlite3 connection is established.")
        cursor = connection.cursor()
        insert_query = """ INSERT INTO dashboard_app_migrationentry (_from,_to,_date) VALUES ('%s', '%s', '%s')""" % (
            currently_on.get_formal_name(), moving_to.get_formal_name(),
            now.strftime("%Y-%m-%d"))
        count = cursor.execute(insert_query)
        connection.commit()
        cursor.close()

    except sqlite3.Error as e:
        print(e)
    finally:
        if (connection):
            connection.close()
            print("The sqlite3 connection is now closed.")


def after_migration(sender, currently_on):
    # delete old driver on now remote vm
    parent_dir_path = os.path.abspath('.')
    parent_dir = os.path.basename(parent_dir_path)
    print(
        "Deleting " +
        parent_dir +
        " from " +
        sender.get_stock_name() +
        " vm.")
    remote_process.remote_remove(
        sender.get_ip(),
        sender.get_username(),
        parent_dir)
    # stop vm
    if sender.is_running():
        print("Turning off " + sender.get_stock_name() + " vm.")
        sender.stop_vm()

    # update dns
    dns.change_ip(currently_on.get_ip())

    # Update logfile
    write_log_after(sender.get_stock_name(), currently_on.get_stock_name())


def update_general_info(file, currently_on):
    with open(file, "r") as jsonFile:  # Read whole file
        data = json.load(jsonFile)

    data["GLAROS_CURRENTLY_ON"] = currently_on.formal_name
    data["GLAROS_CURRENT_STATUS"] = "Running"
    data["GLAROS_CURRENT_IP"] = currently_on.get_ip()
    data["GLAROS_CURRENTLY_ON_COLOUR"] = currently_on.ui_colour

    with open(file, "w") as jsonFile:
        json.dump(data, jsonFile)


def ignore(parent_dir, moving_to, remote_filepath):
    files_to_upload = [f for f in os.listdir() if f not in exclude_files]
    try:
        #   parent_dir = os.path.dirname(os.path.realpath(__file__))
        for _file in files_to_upload:
            print("Uploading -> " + _file)
            if os.path.isdir(_file):
                recursive = True
            else:
                recursive = False
            vm_scp.upload_file(
                os.path.join(
                    parent_dir,
                    _file),
                moving_to.get_ip(),
                moving_to.get_username(),
                remote_path="~/" +
                            remote_filepath +
                            "/" +
                            _file,
                recursive=recursive)
    except Exception as e:
        print(e)
        print("Could not move directory")
        return


def main():
    # First we need to identify on which CSP this Driver was created from
    if len(sys.argv) < 1:
        print('Please enter either "amzn" or "msft"')
        return

    if sys.argv[1] == "from_msft":
        from_msft = AzureCSP()
        currently_on = AwsCSP()

        after_migration(from_msft, currently_on)
    elif sys.argv[1] == "from_amzn":
        from_amzn = AwsCSP()
        currently_on = AzureCSP()

        after_migration(from_amzn, currently_on)

    elif sys.argv[1] == "from_goog":
        from_goog = GoogleCSP()
        #to_do

    elif sys.argv[1] in stock_objs.keys():
        currently_on = create_stock_object(sys.argv[1])
    else:
        print("Please enter msft or amzn...")
        return

    # Update the General Information file
    update_general_info(GENERAL_INFO_FILE, currently_on)

    print("Currently on " + currently_on.get_stock_name())
    print()
    # update dns
    print("Updating DNS")
    dns.change_ip(currently_on.get_ip())

    # Start checking the stock prices and decide when to migrate
    event_loop(currently_on)


if __name__ == '__main__':
    main()
