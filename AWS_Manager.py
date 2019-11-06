import os, json
import CredentialsParser as cp
import boto3
from pprint import pprint

# How to use this:
# Create an AWS directory (ie. C:\Users\<your_name>\.aws\)
# Copy 'credentials.csv' in that folder
# Create a 'system' environmental variable called "AWS_DIR" for the AWS directory
# Create a virtual environment and install the 'requirements.txt' ($pip install -r requirements.txt)
# Run AWS_Manager.py (make sure you restart the command-line after updating Env. Vars.)


AWS_DIR = os.environ['AWS_DIR']  # (ie: ~/.aws/)
credentials = cp.CredentialsParser(os.path.join(AWS_DIR, 'credentials.csv'))
client = boto3.client(
    'ec2',
    # Locate ".aws/credentials.csv" and get the access keys
    # for the username "PythonManager"
    aws_access_key_id=credentials.get("PythonManager").get("Access key ID"),
    aws_secret_access_key=credentials.get("PythonManager").get("Secret access key"),
    region_name='eu-west-1'
)

response = client.describe_instances()
pprint(response)
