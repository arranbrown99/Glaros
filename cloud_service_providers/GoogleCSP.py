import time
from subprocess import call, check_output
import json
import os

from cloud_service_providers.AbstractCSP import AbstractCSP

"""
to run first set up the cloud-sdk
https://cloud.google.com/sdk/docs/downloads-apt-get
and authorise it 
https://cloud.google.com/docs/authentication/getting-started
"""


class GoogleCSP(AbstractCSP):
    stock_name = "goog"
    username = os.environ['GOOGLE_USERNAME']
    ui_colour = "rgb(255,205,86)"
    formal_name = "Google"

    def __init__(self):
        """
        Read information about where to find the VM from environment variables
        """
        self.project = os.environ['GOOGLE_PROJECT']
        self.zone = os.environ['GOOGLE_ZONE']
        self.name = os.environ['GOOGLE_VM_NAME']

    def identify(self):
        vm_id = self.get_info()['id']
        return vm_id

    def get_ip(self):
        # returns the ip address of the google vm
        # ip addresses are not assigned if the vm is not on so in that case we should throw an error
        if self.is_running():
            info = self.get_info()
            ip = info['networkInterfaces'][0]['accessConfigs'][0]['natIP']
            return ip
        else:
            raise Exception

    def start_vm(self):
        # Start the VM
        print('\nStart VM')
        # command is 
        # gcloud compute instances start google-vm
        output = self.execute_commands(["gcloud", "compute", "instances", "start", self.name])
        return output

    def stop_vm(self):
        # Stop the VM
        # uses deallocate rather than stop as it costs less money
        print('\nStop VM')
        output = self.execute_commands(["gcloud", "compute", "instances", "stop", self.name])
        return output

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

    def get_info(self):
        # command is
        # gcloud compute instances describe google-vm
        output = check_output(["gcloud", "compute", "instances", "describe", self.name, "--format=json"])
        return json.loads(output)

    @staticmethod
    def status(self):
        # helper method for is running that fetches the running status of the vm
        status = self.get_info()['status']
        return status

    def is_running(self):
        # returns true if the vm is on otherwise returns false
        status = self.status(self)
        if status == "RUNNING":
            return True
        else:
            return False


def main():
    """
    For testing and debugging purposes starts a VM and prints its IP address
    """
    google_vm = GoogleCSP()
    google_vm.start_vm()
    print(google_vm.get_ip())
    print(google_vm.get_username())
    print(google_vm.identify())


if __name__ == '__main__':
    main()
