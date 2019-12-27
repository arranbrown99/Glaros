# tests for scp_aws
import sys
my_file = 'cs27-main/'
import scp_aws
import os

# inputs
ip = '52.204.54.141'
un = 'test3'
pw = sys.argv[2]

# to use, pass password on command line

def test_uploadFile():
    """ tests function uploadFile behaves as desired.
    """

    # invalid local_path, default remote_path
    assert(scp_aws.uploadFile('doesnt_exist.txt',ip,un,pw)) == None
    # valid local_path, default remote_path
    print("before 2nd assertion.")
    assert(scp_aws.uploadFile('test.txt',ip,un,pw)) == 1
    # invalid local_path, invalid remote_path
    assert(scp_aws.uploadFile('doesnt_exist.txt', ip, un,pw, 'doesnt_exist/')) == None
    # valid local_path, invalid remote_path
    assert(scp_aws.uploadFile('test.txt', ip, un,pw, 'doesnt_exist/')) == None

def test_downloadFile():
    """ tests function downloadFile behaves as desired.
    """

    # invalid remote_path, default local_path
    assert(scp_aws.downloadFile('doesnt_exist.txt',ip,un,pw)) == None
    # valid remote_path, default local_path
    assert(scp_aws.downloadFile('text.txt',ip,un,pw)) != 1
    # invalid remote_path, invalid local_path
    assert(scp_aws.downloadFile('doesnt_exist.txt',ip,un,'doesnt_exist/',pw)) == None
    # valid remote_path, invalid local_path
    assert(scp_aws.downloadFile('test.txt',ip,un,'doesnt_exist/',pw)) == None



if __name__ == '__main__':
    test_uploadFile()
    test_downloadFile()
    print("All tests passed OK.")
