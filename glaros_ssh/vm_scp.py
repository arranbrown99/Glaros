import paramiko
from paramiko import SSHConfig, SSHClient, AutoAddPolicy, ssh_exception, RSAKey
from scp import SCPClient, SCPException
import os.path


def get_key_for_host(host, index):
    '''returns the path that is the private key for a given host by looking at ~/.ssh/config
    important this only works if there is 1 private key in the config file for a given host'''
    ssh_config = SSHConfig()
    user_config_file = os.path.expanduser("~/.ssh/config")
    if os.path.exists(user_config_file):
        with open(user_config_file) as f:
            ssh_config.parse(f)
    user_config = ssh_config.lookup(host)
    if 'identityfile' in user_config:
        path = os.path.expanduser(user_config['identityfile'][index])
        if not os.path.exists(path):
            raise Exception(
                "Specified IdentityFile " + path + " for " + host + " in ~/.ssh/config not existing anymore.")
        else:
            return path


def connection(ip_address, username):
    # try to establish connection to remote virtual machine
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    # loop over all of the private keys in config and see if we can connect with any of them
    num_lines = sum(1 for line in open(os.path.expanduser("~/.ssh/config")))
    for index in range(0, num_lines):
        key = get_key_for_host(ip_address, index)
        ki = RSAKey.from_private_key_file(key)
        try:
            ssh.connect(ip_address, username=username,
                        pkey=ki, banner_timeout=6000000)
            return ssh
        except:
            continue
    raise SCPException("No valid private key in ~/.ssh/config")


def progress4(filename, size, sent, peername):
    print("(%s:%s) %s\'s progress: %.2f%%   \r" %
          (peername[0], peername[1], filename, float(sent) / float(size) * 100))


def upload_file(local_path, ip_address, username, remote_path='', recursive=False):
    '''
    Connect to the AWS virtual machine via SSH and copy a file to it. Optional
    remote_path specifies path to which file will be copied. Default is ~.
    '''
    local_path = str(local_path)

    # Check if local_path is valid
    if not os.path.exists(local_path):
        raise SCPException("Error: invalid local_path: " + local_path)

    ssh = connection(ip_address, username)
    if not ssh:
        raise SCPException("SSH connection refused")

    scp = SCPClient(ssh.get_transport(), progress4=progress4)
    # try to upload file
    try:
        if remote_path != '':
            scp.put(local_path, remote_path=remote_path, recursive=recursive)
        else:
            scp.put(local_path, recursive=recursive)
    except Exception as e:
        raise SCPException(e)
    finally:
        scp.close()
        ssh.close()
