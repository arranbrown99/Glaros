#from AbstractCSP import AbstractCSP
import os
import traceback
#from azure.cli.core import get_default_cli
import subprocess
import json

class AzureCSP():

    def __init__(self):

        self.stock_name = "msft"

        # Here we need to configure all the things necessary to connect
        # to the Azure instance.
        self.TENANT_ID = '6e725c29-763a-4f50-81f2-2e254f0133c8'

        self.LOCATION = 'eastus'
        self.GROUP_NAME = 'cs27'
        self.VM_NAME = 'cs27VM2'

 #   def az_cli(self, args_str):
  #      args = args_str.split()
   #     cli = get_default_cli()
    #    cli.invoke(args)
     #   if cli.result.result:
      #      return cli.result.result
       # elif cli.result.error:
       #     raise cli.result.error
       # return True

    def identify(self):
        print("This was called from an AzureCSP instance.")

    def print_vm(self):
        # response = self.az_cli("vm list")
        # print("vm's: %s" % response)
        # az vm list -d -o table --query "[?name=='vm-name']"
        process = subprocess.Popen(['az','vm','list','-d','-o','table','--query','"[name=='+ self.VM_NAME +']"'],stdout=subprocess.PIPE)
        out, err = process.communicate()
#        d = json.loads(out)
        print(out)
        print()
        print()

    def is_running(self):
        pass

    def execute_commands(self, commands):
        pass

    def start_vm(self):
        # Start the VM
        print('\nStart VM')
        process = subprocess.Popen(['az','vm','start','-g',self.GROUP_NAME,'-n',self.VM_NAME],stdout=subprocess.PIPE)
        out, err = process.communicate()
        return 0

    def stop_vm(self):
        # Stop the VM
        print('\nStop VM')
        process = subprocess.Popen(['az','vm','stop','-g',self.GROUP_NAME,'-n',self.VM_NAME],stdout=subprocess.PIPE)
        print("Done")
        out, err = process.communicate()
        return 0

 

    def execute_command(self):
        pass

    def upload_file(self):
        pass


if __name__ == '__main__':
    azure_vm = AzureCSP()
    azure_vm.print_vm()
    azure_vm.stop_vm()
    azure_vm.print_vm()
    azure_vm.start_vm()
    azure_vm.print_vm()
