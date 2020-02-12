from glaros_ssh import remote_process
from cloud_service_providers.AzureCSP import AzureCSP


class TestRemoteProcess(unittest.TestCase):

    def test_remote(self):
        # inputs
        azure_vm = AzureCSP()
        if azure_vm.is_running() is False:
            azure_vm.start_vm()
        ip_address = azure_vm.get_ip()
        username = azure_vm.get_username()

        # Delete specified file or directory if it exists
        remote_process.remote_remove(ip_address, username, 'test.txt')
        remote_process.remote_ls(ip_address, username, 'test.txt')

        remote_process.remote_remove(ip_address, username, 'tests')
        remote_process.remote_ls(ip_address, username, 'tests')

        remote_process.remote_remove(ip_address, username, 'test_vm_scp.py')
        remote_process.remote_ls(ip_address, username, 'test_vm_scp.py')


if __name__ == '__main__':
    unittest.main()
