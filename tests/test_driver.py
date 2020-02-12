import unittest
import sys
import os
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import Driver
from cloud_service_providers.AwsCSP import AwsCSP
from cloud_service_providers.AzureCSP import AzureCSP


class testDriver(unittest.TestCase):

    def test_create_stock_object(self):
        """ test correct and incorrect inputs for create_stock_object()
        """
        self.assertEqual(Driver.create_stock_object("amzn"), AwsCSP())
        self.assertEqual(Driver.create_stock_object("msft"), AzureCSP())
        # self.assertEqual(Driver.create_stock_object("goog"), GoogleCSP())

        self.assertIsNone(Driver.create_stock_object("fake"))

    def test_boot_vm(self):
        """ test boot_vm() works as expected when given a VM
        """
        # use the test VM
        test_vm = AzureCSP()
        # switch on VM
        Driver.boot_vm(test_vm)
        self.assertTrue(test_vm.is_running)
        # turn off VM
        test_vm.stop_vm()

    def test_run_booted_vm(self):
        """ test that run_booted_vm works as expected
        """
        # use test VM and switch it on
        test_vm = AzureCSP()
        test_vm.start_vm()

        # same VM passed as currently_on and moving_to so expected to
        # raise exception
        self.assertRaises(Exception, Driver.run_booted_vm(test_vm, "foo"))
        test_vm.stop_vm()


if __name__ == '__main__':
    unittest.main()
