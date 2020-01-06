# tests for scp_aws
import sys
my_file = 'cs27-main/'
import vm_scp
import os

# inputs
#ip = '52.204.54.141'
#ip = '54.89.139.235'
ip = '34.196.229.24'
un = 'test2'
pw = sys.argv[1]

# to use, pass password on command line

def test_uploadFile():
    """ tests function uploadFile behaves as desired.
    """

    # invalid local_path, default remote_path
    assert(vm_scp.uploadFile('doesnt_exist.txt',ip,un,pw)) == None
    # valid local_path, default remote_path
    print("before 2nd assertion.")
    assert(vm_scp.uploadFile('test.txt',ip,un,pw)) == 1
    # invalid local_path, invalid remote_path
    assert(vm_scp.uploadFile('doesnt_exist.txt', ip, un,pw, 'doesnt_exist/')) == None
    # valid local_path, invalid remote_path
    assert(vm_scp.uploadFile('test.txt', ip, un,pw, 'doesnt_exist/')) == None

def test_downloadFile():
    """ tests function downloadFile behaves as desired.
    """

    # invalid remote_path, default local_path
    assert(vm_scp.downloadFile('doesnt_exist.txt',ip,un,pw)) == None
    # valid remote_path, default local_path
    assert(vm_scp.downloadFile('text.txt',ip,un,pw)) != 1
    # invalid remote_path, invalid local_path
    assert(vm_scp.downloadFile('doesnt_exist.txt',ip,un,'doesnt_exist/',pw)) == None
    # valid remote_path, invalid local_path
    assert(vm_scp.downloadFile('test.txt',ip,un,'doesnt_exist/',pw)) == None



if __name__ == '__main__':
    test_uploadFile()
    test_downloadFile()
    print("All tests passed OK.")
