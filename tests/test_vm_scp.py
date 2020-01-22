# tests for scp_aws

from context import *
my_file = 'cs27-main/'

# inputs
ip = '34.196.229.24'
un = 'test2'
if len(sys.argv) > 1:
    pw = sys.argv[-1]
else:
    pw = ''
# to use password enter on command line
class TestVMSCP(unittest.TestCase):

    def test_uploadFile(self):
        """ tests function uploadFile behaves as desired.
        """

        # invalid local_path, default remote_path
        self.assertIsNone(vm_scp.uploadFile('doesnt_exist.txt',ip,un,pw))
        # valid local_path, default remote_path
        self.assertIs(vm_scp.uploadFile('test.txt',ip,un,pw),1)
        # invalid local_path, invalid remote_path
        self.assertIsNone(vm_scp.uploadFile('doesnt_exist.txt', ip, un,pw, 'doesnt_exist/'))
        # valid local_path, invalid remote_path
        self.assertIsNone(vm_scp.uploadFile('test.txt', ip, un,pw, 'doesnt_exist/'))
        # sending itself
        self.assertIs(vm_scp.uploadFile('vm_scp.py',ip,un,pw),1)
        SCP_BASE_DIR = os.path.dirname(os.path.realpath(__file__))
        PROJECT_BASE_DIR = os.path.dirname(SCP_BASE_DIR)
        self.assertIs(vm_scp.uploadFile(SCP_BASE_DIR,ip,un,pw),1)
        self.assertIs(vm_scp.uploadFile(PROJECT_BASE_DIR,ip,un,pw),1)


    def test_downloadFile(self):
        """ tests function downloadFile behaves as desired.
        """

        # invalid remote_path, default local_path
        self.assertIsNone(vm_scp.downloadFile('doesnt_exist.txt',ip,un,pw))
        # valid remote_path, default local_path
        self.assertIsNotNone(vm_scp.downloadFile('text.txt',ip,un,pw))
        # invalid remote_path, invalid local_path
        self.assertIsNone(vm_scp.downloadFile('doesnt_exist.txt',ip,un,'doesnt_exist/',pw))
        # valid remote_path, invalid local_path
        self.assertIsNone(vm_scp.downloadFile('test.txt',ip,un,'doesnt_exist/',pw))



if __name__ == '__main__':
    unittest.main()
