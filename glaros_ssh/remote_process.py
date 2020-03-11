import os
from glaros_ssh import vm_scp


class Error(Exception):
    """
    Base class for exceptions
    """
    pass


class RemoteProcessError(Error):
    """
    Exception raised from errors in the remote command.

    Attributes
    ------
        message -- explanation of the error from the remote machine
    """

    def __init__(self, message):
        self.message = message


def remote_cmd(ip_address, username, cmd):
    """
    given a command executes the cmd on a remote computer
    Parameters
    ----------
    ip_address : ip_address of the remote vm
    username : username on the remote vm
    cmd : command to be executed on the remote vm

    Returns
    -------
    the output of the command in a list
    """
    ssh = vm_scp.connection(ip_address, username)
    if not ssh:
        print("could not connect")
        return

    try:
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
        # true if the command returns an error
        read_error = ssh_stderr.readlines()
        ssh.close()
        if len(read_error) > 5:
            raise RemoteProcessError(read_error)

        return ssh_stdout.readlines()
    except BaseException:
        print("command failed")
        return


def remote_python(ip_address, username, python_file):
    """
    Runs a python command on the remote vm
    nohup so process on child vm continues even after logout of parent vm
    & to run in the background
    cd parent_dir; moves into the cs27-main so that the code is alway
    excuted in the same working directory

    Parameters
    ----------
    ip_address : ip_address of the remote vm
    username : username on the remote vm
    python_file :  python file to be executed on the remote vm

    Returns
    -------
    output of the command in a list
    """

    parent_dir = os.path.basename(os.path.abspath('.'))
    cmd = 'cd ' + parent_dir + ';./' + python_file
    return remote_cmd(ip_address, username, cmd)


def remote_mkdir(ip_address, username, dir_name):
    """
    linux mkdir command
    used to create the remote directory we will send files to

    Parameters
    ----------
    ip_address : ip_address of the remote vm
    username : username on the remote vm
    dir_name : directory name we will be creating

    Returns
    -------
    output of the command in a list
    """

    cmd = 'mkdir ' + dir_name
    return remote_cmd(ip_address, username, cmd)


def remote_ls(ip_address, username, arguments):
    """
    Linux ls command
    used for testing

    Parameters
    ----------
    ip_address : ip_address of the remote vm
    username : username on the remote vm
    arguments : directory we will be ls into

    Returns
    -------
    output of the command in a list
    """
    # used for testing
    cmd = 'ls ' + arguments
    return remote_cmd(ip_address, username, cmd)


def remote_remove(ip_address, username, remote_filepath):
    """
    removes a file in a remote vm
    sudo to delete files created by root
    -r to delete directories
    Parameters
    ----------
    ip_address : ip_address of the remote vm
    username : username on the remote vm
    remote_filepath : filepath to the file we want to remove

    Returns
    -------

    """

    cmd = 'sudo rm -r ' + remote_filepath
    return remote_cmd(ip_address, username, cmd)
