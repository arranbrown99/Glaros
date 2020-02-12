from paramiko import SSHConfig, SSHClient, AutoAddPolicy, ssh_exception, RSAKey
from scp import SCPClient, SCPException
import os.path


def get_key_for_host(host):
    '''returns the path that is the private key for a given host by looking at ~/.ssh/config
    important this only works if there is 1 private key in the config file for a given host'''
    ssh_config = SSHConfig()
    user_config_file = os.path.expanduser("~/.ssh/config")
    if os.path.exists(user_config_file):
        with open(user_config_file) as f:
            ssh_config.parse(f)
    user_config = ssh_config.lookup(host)
    if 'identityfile' in user_config:
        path = os.path.expanduser(user_config['identityfile'][0])
        if not os.path.exists(path):
            raise Exception(
                "Specified IdentityFile " + path + " for " + host + " in ~/.ssh/config not existing anymore.")
        else:
            return path


def connection(ip_address, username, password=''):
    # try to establish connection to remote virtual machine
    try:
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        if password == '':
            key = get_key_for_host(ip_address)
            ki = RSAKey.from_private_key_file(key)
            ssh.connect(ip_address, username=username, pkey=ki)
        else:
            ssh.connect(ip_address, username=username, password=password)
        return ssh
    except:
        pass


def progress4(filename, size, sent, peername):
    print("(%s:%s) %s\'s progress: %.2f%%   \r" % (peername[0], peername[1], filename, float(sent) / float(size) * 100))


def upload_file(local_path, ip_address, username, password='', remote_path='', recursive=False):
    '''
    Connect to the AWS virtual machine via SSH and copy a file to it. Optional
    remote_path specifies path to which file will be copied. Default is ~.
    '''
    local_path = str(local_path)

    # Check if local_path is valid
    if not os.path.exists(local_path):
        print("Error: invalid local_path: " + local_path)
        return

    ssh = connection(ip_address, username, password)
    if not ssh:
        return

    scp = SCPClient(ssh.get_transport(), progress4=progress4)
    # try to upload file
    try:
        if remote_path != '':
            scp.put(local_path, remote_path=remote_path, recursive=recursive)
        else:
            scp.put(local_path, recursive=recursive)
    except SCPException as e:
        print(e)
        print("Error: Could not upload file.")
        return
    finally:
        scp.close()
    return 1
