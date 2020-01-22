# from AbstractCSP import AbstractCSP
import time
from subprocess import call, check_output
import json
from cloud_service_providers.AbstractCSP import AbstractCSP

# uses subprocesses to call the azure cli

# install this first on ubuntu
# curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# on centOS ie amazon use these commands
# sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
# sudo sh -c 'echo -e "[azure-cli] name=Azure CLI baseurl=https://packages.microsoft.com/yumrepos/azure-cli enabled=1 gpgcheck=1 gpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/azure-cli.repo'
# sudo yum install azure-cli

# then must first be logged in on command line use
# az login
# or run the login function in this script
# this login stays for 3 months

class AzureCSP(AbstractCSP):

    def __init__(self):

        self.stock_name = "msft"

        # Here we need to configure all the things necessary to connect
        # to the Azure instance.
        self.TENANT_ID = '6e725c29-763a-4f50-81f2-2e254f0133c8'

        self.LOCATION = 'eastus'
        self.GROUP_NAME = 'cs27'
        self.VM_NAME = 'cs27VM2'
        self.username = 'glarosAzure'

    def identify(self):
        info = self.get_info()
        return info[0]["id"]
        

    def get_info(self):
        command = ["az", "vm", "list","-d", "--output","json","--query", "[?name=='cs27VM2']"]
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
        time.sleep(2*60)  # mins
        return output

    def stop_vm(self):
        # Stop the VM
        # uses deallocate rather than stop as it costs less money
        print('\nStop VM')
        return self.execute_commands(["az", "vm", "deallocate", "-g", self.GROUP_NAME, '-n', self.VM_NAME])

    def execute_commands(self, commands):
        return call(commands)

    def upload_file(self):
        pass

    def login(self):
        # this logs in for 3 months
        return self.execute_commands(["az", "login"])

    def logout(self):
        return self.execute_commands(["az", "logout"])


def main():
    azure_vm = AzureCSP()

    if not azure_vm.is_running():
        azure_vm.start_vm()

    print(azure_vm.get_ip())
    print(azure_vm.get_username())

if __name__ == '__main__':
    main()
