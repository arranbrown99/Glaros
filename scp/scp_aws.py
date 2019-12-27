from paramiko import SSHClient, AutoAddPolicy, ssh_exception
from scp import SCPClient
import os.path

# Connection made with username and password. Remove password once ssh keys configured.

def uploadFile(local_path, ip_address, username, password='', remote_path=''):
    '''Connect to the AWS virtual machine via SSH and copy a file to it. Optional
    remote_path specifies path to which file will be copied. Default is ~.
    '''
    local_path = str(local_path)

    # Check if local_path is valid
    if os.path.exists(local_path) == False:
        print("Error: invalid local_path")
        return

    # try to establish connection to AWS virtual machine
    try:
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        if(password==''):
            ssh.connect(ip_address, username=username)
        else:
            ssh.connect(ip_address, username=username, password=password)
    except Exception:
        print("Error: Could not connect.")
        return

    # try to upload file
    try:
        scp = SCPClient(ssh.get_transport())
        if remote_path != '':
            scp.put(local_path, remote_path=remote_path)
        else:
            scp.put(local_path)
    except Exception:
        print("Error: Could not upload file.")
        return
    finally:
        scp.close()
    return 1

def downloadFile(remote_path, ip_address, username, password='',local_path=''):
    '''Connect to AWS virtual machine via SSH and remotely copy a file from it to the
    local machine. Optional local_path specifies path to which file will be saved on local
    machine.
    '''

    remote_path = str(remote_path)

    # Check if remote_path is valid
    if os.path.exists(remote_path) == False:
        print("Error: invalid remote_path")
        return

    # try establish a connection to AWS virtual machine
    try:
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        if(password==''):
            ssh.connect(ip_address=ip_address, username=username)
        else:
            ssh.connect(ip_address=ip_address, username=username, password=password)
    except Exception:
        print("Error: Could not connect.")
        return

    # try to download file
    try:
        scp = SCPClient(ssh.get_transport())
        if local_path != '':
            scp.get(remote_path, local_path=local_path) 
        else:
            scp.get(remote_path)
    except Exception:
        print("Error: Could not upload file.")
        return
    finally:
        scp.close()
    return 1
