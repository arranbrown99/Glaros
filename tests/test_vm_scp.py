# tests for scp_aws
from scp import SCPException

from glaros_ssh import vm_scp
from cloud_service_providers.AzureCSP import AzureCSP


# to use password enter on command line
class TestVMSCP(unittest.TestCase):

    def test_uploadFile(self):
        # inputs
        azure_vm = AzureCSP()
        if azure_vm.is_running() is False:
            azure_vm.start_vm()
        ip = azure_vm.get_ip()
        un = azure_vm.get_username()

        if len(sys.argv) > 1:
            pw = sys.argv[-1]
        else:
            pw = ''

        """ tests function uploadFile behaves as desired.
        """

        # invalid local_path, default remote_path
        self.assertRaises(SCPException, vm_scp.upload_file('doesnt_exist.txt', ip, un, pw))
        # valid local_path, default remote_path
        self.assertIs(vm_scp.upload_file('test.txt', ip, un, pw), 1)
        # invalid local_path, invalid remote_path
        self.assertRaises(SCPException,
                          vm_scp.upload_file('doesnt_exist.txt', ip, un, pw, 'doesnt_exist/'))
        # valid local_path, invalid remote_path
        self.assertRaises(SCPException,
                          vm_scp.upload_file('test.txt', ip, un, pw, 'doesnt_exist/'))
        # sending itself
        self.assertIs(vm_scp.upload_file('test_vm_scp.py', ip, un, pw), 1)
        scp_base_dir = os.path.dirname(os.path.realpath(__file__))
        self.assertIs(vm_scp.upload_file(scp_base_dir, ip, un, pw, recursive=True), 1)


if __name__ == '__main__':
    unittest.main()
