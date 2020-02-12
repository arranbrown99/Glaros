from cloud_service_providers.AzureCSP import AzureCSP


# tests use AzureTesting VM
class TestAzureVM(unittest.TestCase):

    def test_on_off(self):
        """ turn on VM, assert on is true, turn off VM, assert off is true
        """
        testing_vm = AzureCSP()
        testing_vm.stop_vm()  # to make sure the vm is turned off works even if the vm is off

        testing_vm.start_vm()
        # VM successfully switches on
        self.assertTrue(testing_vm.is_running())

        testing_vm.stop_vm()
        # VM successfully switches off
        self.assertFalse(testing_vm.is_running())

    def test_get_ip(self):
        testing_vm = AzureCSP()
        """ get_ip() should return an address when VM is ON, should not when VM is OFF
        """
        if testing_vm.is_running() is False:
            # no ip address returned
            self.assertIsNone(testing_vm.get_ip())
        else:
            self.assertIsNotNone(testing_vm.get_ip())


if __name__ == '__main__':
    unittest.main()
