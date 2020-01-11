# tests for scp_aws
import sys
my_file = 'cs27-main/'
import vm_scp
import os

# inputs
ip = '34.196.229.24'
un = 'test2'
if len(sys.argv) > 1:
    pw = sys.argv[-1]
else:
    pw = ''
# to use password enter on command line

def test_uploadFile():
    """ tests function uploadFile behaves as desired.
    """

    # invalid local_path, default remote_path
    assert(vm_scp.uploadFile('doesnt_exist.txt',ip,un,pw)) == None,"should not be able to send a file that doesn't exist"
    # valid local_path, default remote_path
    assert(vm_scp.uploadFile('test.txt',ip,un,pw)) == 1,"should send a file that exists"
    # invalid local_path, invalid remote_path
    assert(vm_scp.uploadFile('doesnt_exist.txt', ip, un,pw, 'doesnt_exist/')) == None,"should not be able to send to a remote path that doesn't exist"
    # valid local_path, invalid remote_path
    assert(vm_scp.uploadFile('test.txt', ip, un,pw, 'doesnt_exist/')) == None,"should not be able to send to a remote path that doesn't exist"
    # sending itself
    assert(vm_scp.uploadFile('vm_scp.py',ip,un,pw)) == 1, "should send vm_scp.py"
    SCP_BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    PROJECT_BASE_DIR = os.path.dirname(SCP_BASE_DIR)
    assert(vm_scp.uploadFile(SCP_BASE_DIR,ip,un,pw)) == 1, "should send the directory this is in"
    print(PROJECT_BASE_DIR)
    assert(vm_scp.uploadFile(PROJECT_BASE_DIR,ip,un,pw)) == 1, "should send the directory containing the entire project"


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
