# from AbstractCSP import AbstractCSP
import time
from subprocess import call, check_output
import json
from cloud_service_providers.AbstractCSP import AbstractCSP
import os

"""
uses subprocesses to call the azure cli

install this first on ubuntu

curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

on centOS ie amazon use these commands
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
sudo sh -c 'echo -e "[azure-cli] name=Azure CLI baseurl=https://packages.microsoft.com/yumrepos/azure-cli
 enabled=1 gpgcheck=1 gpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/azure-cli.repo'
sudo yum install azure-cli

then must first be logged in on command line use
az login
or run the login function in this script
this login stays for 3 months
"""


class AzureCSP(AbstractCSP):
    # Static Variables
    ui_colour = 'rgb(54,162,235)'
    formal_name = 'Azure'

    def __init__(self):

        self.stock_name = "msft"

        # Here we need to configure all the things necessary to connect
        # to the Azure instance.

        self.LOCATION = os.environ['AZURE_LOCATION']
        self.GROUP_NAME = os.environ['AZURE_GROUP_NAME']
        self.VM_NAME = os.environ['AZURE_VM_NAME']
        self.username = os.environ['AZURE_USERNAME']

    def identify(self):
        info = self.get_info()
        return info[0]["id"]

    def get_info(self):

        command = ["az", "vm", "list", "-d", "--output", "json", "--query", "[?name=='" + self.VM_NAME + "']"]

        info = check_output(command)
        return json.loads(info)

    def get_ip(self):
        info = self.get_info()
        ip = info[0]["publicIps"]
        return ip

    def is_running(self):
        info = self.get_info()
        powerstate = info[0]["powerState"]
        if powerstate == "VM running":
            return True
        else:
            return False

    def start_vm(self):
        # Start the VM
        print('\nStart VM')
        output = self.execute_commands(["az", "vm", "start", "-g", self.GROUP_NAME, '-n', self.VM_NAME])
        time.sleep(2 * 60)  # mins
        return output

    def stop_vm(self):
        # Stop the VM
        # uses deallocate rather than stop as it costs less money
        print('\nStop VM')
        return self.execute_commands(["az", "vm", "deallocate", "-g", self.GROUP_NAME, '-n', self.VM_NAME])

    @staticmethod
    def execute_commands(commands):
        """

        Parameters
        ----------
        commands : takes in a command that is a list of the command separated by spaces

        Returns
        -------
        the output of the command
        """
        return call(commands)

    def login(self):
        """
        Logs in to Azure will take you to microsoft website
        Note this logs in for 3 months
        Returns
        -------
        the output of the command
        """
        return self.execute_commands(["az", "login"])

    def logout(self):
        """
        Logs out of Azure will take you to microsoft website
        Returns
        -------
        the output of the command
        """
        return self.execute_commands(["az", "logout"])


def main():
    """
    For testing and debugging purposes starts a VM and prints its IP address
    """
    azure_vm = AzureCSP()

    if not azure_vm.is_running():
        azure_vm.start_vm()

    print(azure_vm.get_ip())
    print(azure_vm.get_username())


if __name__ == '__main__':
    main()
