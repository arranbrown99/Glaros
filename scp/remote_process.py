import vm_scp

#given a command executes the cmd on a remote computer
def remote_cmd(ip_address,username,cmd):
    ssh =  vm_scp.connection(ip_address,username)
    if ssh == False:
        print("could not connect")
        return
    
    try:
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
    except:
        print("command failed")
        return 

def remote_python(ip_address,username,python_file):
    cmd = 'nohup python ' + python_file + ' &'
    return remote_cmd(ip_address,username,cmd)

    

