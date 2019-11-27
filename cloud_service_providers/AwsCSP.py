from cloud_service_providers.AbstractCSP import AbstractCSP
import boto3
import botocore


class AwsCSP(AbstractCSP):

    def __init__(self):
        self.stock_name = "amzn"
        # Here we need to configure all the things necessary to connect
        # to the AWS instance.

    def identify(self):
        print("This was called from an AwsCSP instance.")

    def start_vm(self):
        pass

    def stop_vm(self):
        pass

    def get_info(self):
        pass

    def execute_command(self):
        pass

    def upload_file(self):
        pass
