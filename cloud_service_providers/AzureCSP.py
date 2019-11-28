from AbstractCSP import AbstractCSP
import os
import traceback

from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.compute.models import DiskCreateOption

class AzureCSP(AbstractCSP):



    def __init__(self):

        self.stock_name = "msft"

        # Here we need to configure all the things necessary to connect
        # to the Azure instance.
        self.TENANT_ID = '6e725c29-763a-4f50-81f2-2e254f0133c8'

        self.LOCATION = 'eastus'
        self.GROUP_NAME = 'cs27'
        self.VM_NAME = 'cs27VM2'


    def identify(self):
        print("This was called from an AzureCSP instance.")

    def print_vm(self):
        virtual_machine = compute_client.virtual_machines.get(
            GROUP_NAME,
            VM_NAME
        )
        print(virtual_machine)


    def start_vm(self):
        # Start the VM
        print('\nStart VM')
        try:
            async_vm_start = compute_client.virtual_machines.start(
                GROUP_NAME, VM_NAME)
            return 0
        except:
            print("Failed to start VM")
            return


    def stop_vm(self):
        pass

    def get_info(self):
        pass

    def execute_command(self):
        pass

    def upload_file(self):
        pass

if __name__ == '__main__':
    print("here")
    azure_vm = Azure_CSP()
    print(azure_vm.GROUP_NAME)

