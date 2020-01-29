import os
from glaros_ssh import vm_scp

# given a command executes the cmd on a remote computer


def remote_cmd(ip_address, username, cmd):
    ssh = vm_scp.connection(ip_address, username)
    if not ssh:
        print("could not connect")
        return

    try:
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
        print(ssh_stderr.readlines())
        return ssh_stdout.readlines()
    except BaseException:
        print("command failed")
        return


def remote_python(ip_address, username, python_file):
    # nohup so process on child vm continues even after logout of parent vm
    # & to run in the background
    # cd parent_dir; moves into the cs27-main so that the code is alway
    # excuted in the same working directory
    parent_dir = os.path.basename(os.path.abspath('.'))
    cmd = 'cd ' + parent_dir + ';./' + python_file
    return remote_cmd(ip_address, username, cmd)


def remote_mkdir(ip_address, username, dir_name):
    # used to create the directory we will send files to
    cmd = 'mkdir ' + dir_name
    return remote_cmd(ip_address, username, cmd)


def remote_ls(ip_address, username, arguments):
    # used for testing
    cmd = 'ls ' + arguments
    return remote_cmd(ip_address, username, cmd)


def remote_remove(ip_address, username, remote_filepath):
    #-r to delete directories
    #-f to delete automatically without human confirmation
    # this could be dangerous if we accidently delete important files but
    # everything should be backed up
    cmd = 'rm -r ' + remote_filepath
    return remote_cmd(ip_address, username, cmd)
