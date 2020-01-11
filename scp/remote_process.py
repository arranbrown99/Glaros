import vm_scp

#given a command executes the cmd on a remote computer
def remote_cmd(ip_address,username,cmd):
    ssh =  vm_scp.connection(ip_address,username)
    if ssh == False:
        print("could not connect")
        return
    
    try:
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
        return True
    except:
        print("command failed")
        return 

def remote_python(ip_address,username,python_file):
    #nohup so process on child vm continues even after logout of parent vm
    # & to run in the background
    cmd = 'nohup python ' + python_file + ' &'
    return remote_cmd(ip_address,username,cmd)

def remote_remove(ip_address,username,remote_filepath):
    #-r to delete directories
    #-f to delete automatically without human confirmation
    #this could be dangerous if we accidently delete important files but everything should be backed up
    cmd = 'rm -r -f ' + remote_filepath
    return remote_cmd(ip_address,username,cmd)
