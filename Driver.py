"""
This class represents the main program that will be running on the current CSP.
Every so often it will compare tbe stock prices of all available CSPs (through StockRetriever)
and it will decide when it's time to move/migrate to another CSP.

Event Loop

Driver running on Azure VM.
periodically check the StockReceiver - list of cloud providers, static String for the Stock Exchange name.
Decide to move to AWS.
Create the object for AWS.
StartVM on AWS.
Send using python scp script - the SSH keys are set up before hand and not handled by the script.
Run the newly made driver on the remote VM.
Ping new driver
Have old driver delete itself

"""
import sys
import threading

import threading
from cloud_service_providers.AwsCSP import AwsCSP
from cloud_service_providers.AzureCSP import AzureCSP

counter = 0  # used in dummy condition to move after 4 calls to migrate()
currently_on = None
check_every = 3  # seconds


def migrate():
    global counter
    move = False

    # Logic to decide (using StockRetriever)
    print("Is it time to move?")
    if counter > 4:
        move = True

    if move:  # dummy condition
        # Yes!!!
        print("Yes! Migrating...")
        # Start migration process

    else:
        print("not now!")
        # If it's not time to move we start the Timer again.
        threading.Timer(check_every, migrate).start()
        counter += 1


cloud_service_providers = [
    'amzn',  # Amazon (AWS)
    'msft',  # Microsoft (Azure)
    # 'goog',  # Google (GCP)
]

if __name__ == '__main__':
    # First we need to identify on which CSP this Driver was created from
    # Perhaps through a command line argument???
    currently_on = AwsCSP()

    # Start checking the stock prices and decide when to migrate
    migrate()

    # Checking if the abstract class is implemented correctly
    x = AwsCSP()
    y = AzureCSP()
    x.identify()
    y.identify()
    print(x.get_stock_name())
    print(y.get_stock_name())
