from cloud_service_providers.AbstractCSP import AbstractCSP
import os
import traceback
from azure.cli.core import get_default_cli


class AzureCSP(AbstractCSP):

    def __init__(self):

        self.stock_name = "msft"

        # Here we need to configure all the things necessary to connect
        # to the Azure instance.
        self.TENANT_ID = '6e725c29-763a-4f50-81f2-2e254f0133c8'

        self.LOCATION = 'eastus'
        self.GROUP_NAME = 'cs27'
        self.VM_NAME = 'cs27VM2'

    def az_cli(self, args_str):
        args = args_str.split()
        cli = get_default_cli()
        cli.invoke(args)
        if cli.result.result:
            return cli.result.result
        elif cli.result.error:
            raise cli.result.error
        return True

    def identify(self):
        print("This was called from an AzureCSP instance.")

    def print_vm(self):
        # response = self.az_cli("vm list")
        # print("vm's: %s" % response)
        get_default_cli().invoke(['vm', 'list', '-g', self.GROUP_NAME])

    def is_running(self):
        pass

    def execute_commands(self, commands):
        pass

    def start_vm(self):
        # Start the VM
        print('\nStart VM')
        try:

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
    azure_vm = AzureCSP()
    azure_vm.print_vm()
