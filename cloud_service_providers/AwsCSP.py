import time
import os
import boto3
from botocore.exceptions import ClientError
from cloud_service_providers.AbstractCSP import AbstractCSP
import cloud_service_providers.CredentialsParser as cp

AWS_DIR = os.path.expanduser(os.environ['AWS_DIR'])  # (ie: ~/.aws/)
instance_id = "i-02d62ad8d9438ea4e"


class AwsCSP(AbstractCSP):
    # Static Variables
    ui_colour = 'rgb(255,99,132)'
    formal_name = 'Aws'
    stock_name = "amzn"

    def __init__(self):
        """
        Reads from a csv file the credentials used to access the VM
        """
        credentials = cp.CredentialsParser(
            os.path.join(AWS_DIR, 'credentials.csv'))
        self.client = boto3.client(
            'ec2',
            # Locate ".aws/credentials.csv" and get the access keys
            # for the username "PythonManager"
            aws_access_key_id=credentials.get(
                "PythonManager").get("Access key ID"),
            aws_secret_access_key=credentials.get(
                "PythonManager").get("Secret access key"),
            region_name='eu-west-1'

        )
        self.username = "ec2-user"

    def identify(self):
        print("This was called from an AwsCSP instance.")

    def start_vm(self):
        # Do a dryrun first to verify permissions
        try:
            self.client.start_instances(InstanceIds=[instance_id], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise

        # Dry run succeeded, run start_instances without dryrun
        try:
            self.client.start_instances(
                InstanceIds=[instance_id], DryRun=False)
        except ClientError as e:
            print(e)

        # self.wait_until(not self.is_running())
        while not self.is_running():
            time.sleep(1)

    def stop_vm(self):
        # Do a dryrun first to verify permissions
        try:
            self.client.stop_instances(InstanceIds=[instance_id], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise

        # Dry run succeeded, call stop_instances without dryrun
        try:
            self.client.stop_instances(InstanceIds=[instance_id], DryRun=False)
        except ClientError as e:
            print(e)

        # self.wait_until(not self.is_stopped())
        while not self.is_stopped():
            time.sleep(1)

    def get_info(self):
        response = self.client.describe_instances(InstanceIds=[instance_id])
        return response

    def is_running(self):
        response = self.client.describe_instance_status(
            InstanceIds=[instance_id], IncludeAllInstances=True)
        return response['InstanceStatuses'][0]['InstanceState']['Name'] == 'running'

    def is_stopped(self):
        """

        Returns
        -------
        True if vm is stopped
        """
        response = self.client.describe_instance_status(
            InstanceIds=[instance_id], IncludeAllInstances=True)
        return response['InstanceStatuses'][0]['InstanceState']['Name'] == 'stopped'

    def get_ip(self):
        if self.is_running:
            response = self.client.describe_instances(
                InstanceIds=[instance_id])
            return response['Reservations'][0]['Instances'][0]['NetworkInterfaces'][0]['Association']['PublicIp']
        else:
            raise Exception("VM is not turned on")
