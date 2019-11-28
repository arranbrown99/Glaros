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
from typing import List

from cloud_service_providers.AwsCSP import AwsCSP
from cloud_service_providers.AzureCSP import AzureCSP
import StockRetriever

counter = 0  # used in dummy condition to move after 4 calls to migrate()
check_every = 3  # seconds
cloud_service_providers = [
    'amzn',  # Amazon (AWS)
    'msft',  # Microsoft (Azure)
    # 'goog',  # Google (GCP)
]


def migrate(current):
    global counter
    move = False

    # Logic to decide (using StockRetriever)
    print("Is it time to move?")
    best_stock = StockRetriever.best_stock(cloud_service_providers)
    print(best_stock + " is the current best stock price")

    if current != best_stock:
        print("Moving from " + current + " to " + best_stock)
        move = True
    elif counter > 4:
        if current == 'amzn':
            best_stock = 'msft'
        else:
            best_stock = 'amzn'

        move = True
        print("For demos sake took too long will 'migrate' any way")
        print("Moving from " + current + " to " + best_stock)

    if move:  # dummy condition
        # Yes!!!
        print("Yes! Migrating...")
        # Start migration process
        print("Now migrating to " + best_stock)

    else:
        print("not now!")
        print()
        # If it's not time to move we start the Timer again.
        threading.Timer(check_every, migrate, [current]).start()
        counter += 1


def main():
    # First we need to identify on which CSP this Driver was created from
    if len(sys.argv) < 1:
        print('please enter either "amzn" or "msft"')
        return

    if sys.argv[1] == "amzn":
        currently_on = AwsCSP()
    elif sys.argv[1] == "msft":
        currently_on = AzureCSP()
    else:
        print("please enter either amzn or msft")
        return

    print("currently on " + currently_on.get_stock_name())
    print()
    # Start checking the stock prices and decide when to migrate
    migrate(currently_on.get_stock_name())

    # Checking if the abstract class is implemented correctly
    # x = AwsCSP()
    # y = AzureCSP()
    # x.identify()
    # y.identify()
    # print(x.get_stock_name())
    # print(y.get_stock_name())


if __name__ == '__main__':
    main()
