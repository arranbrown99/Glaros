from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient

# Connection made with username and password. Remove password once ssh keys configured.

def uploadFile(local_path, remote_path=''):
    '''Connect to the AWS virtual machine via SSH and copy a file to it. Optional
    remote_path specifies path to which file will be copied. Default is ~.
    '''
	local_path = str(local_path)

	try:
		ssh = SSHClient()
		ssh.load_system_host_keys()
		ssh.set_missing_host_key_policy(AutoAddPolicy())
		ssh.connect('52.204.54.141', username='test3', password='test3')
	except Exception:
		print("Error: Could not connect.")

	scp = SCPClient(ssh.get_transport())
        if remote_path != '':
            scp.put(local_path, remote_path=remote_path)
        else:
            scp.put(local_path)

	scp.close()

def downloadFile(remote_path, local_path=''):
    '''Connect to AWS virtual machine via SSH and remotely copy a file from it to the
    local machine. Optional local_path specifies path to which file will be saved on local
    machine.
    '''

	remote_path = str(remote_path)

	try:
		ssh = SSHClient()
		ssh.load_system_host_keys()
		ssh.set_missing_host_key_policy(AutoAddPolicy())
		ssh.connect('52.204.54.141', username='test3', password='test3')
	except Exception:
		print("Error: Could not connect.")
	
	scp = SCPClient(ssh.get_transport())
        if local_path != '':
            scp.get(remote_path, local_path=local_path) 
        else:
            scp.get(remote_path)

	scp.close()
