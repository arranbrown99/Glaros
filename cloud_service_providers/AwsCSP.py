import os
import boto3
from botocore.exceptions import ClientError
from cloud_service_providers.AbstractCSP import AbstractCSP
import CredentialsParser as cp

AWS_DIR = os.environ['AWS_DIR']  # (ie: ~/.aws/)
instance_id = "i-02d62ad8d9438ea4e"


class AwsCSP(AbstractCSP):

    def __init__(self):
        self.stock_name = "amzn"
        credentials = cp.CredentialsParser(os.path.join(AWS_DIR, 'credentials.csv'))
        self.client = boto3.client(
            'ec2',
            # Locate ".aws/credentials.csv" and get the access keys
            # for the username "PythonManager"
            aws_access_key_id=credentials.get("PythonManager").get("Access key ID"),
            aws_secret_access_key=credentials.get("PythonManager").get("Secret access key"),
            region_name='eu-west-1'
        )
        # response = self.client.describe_instances()
        # instances = self.client.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

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
            response = self.client.start_instances(InstanceIds=[instance_id], DryRun=False)
            print(response)
        except ClientError as e:
            print(e)

    def stop_vm(self):
        # Do a dryrun first to verify permissions
        try:
            self.client.stop_instances(InstanceIds=[instance_id], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise

        # Dry run succeeded, call stop_instances without dryrun
        try:
            response = self.client.stop_instances(InstanceIds=[instance_id], DryRun=False)
            print(response)
        except ClientError as e:
            print(e)

    def get_info(self):
        response = self.client.describe_instances()
        print(response)

    def execute_commands(self, commands):
        pass

    def upload_file(self):
        pass

    def is_running(self):
        response = self.client.describe_instance_status(InstanceIds=[instance_id])
        return response['InstanceStatuses'][0]['InstanceState']['Name'] == 'running'
