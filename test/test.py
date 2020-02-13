import unittest
import os
import sys
from unittest.mock import patch
from scp import SCPException

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from glaros_ssh import remote_process
import configparser
from dns import gen_config
import StockRetriever
from glaros_ssh import vm_scp
from cloud_service_providers.AzureCSP import AzureCSP

# list for good test input
good_l = ['amzn', 'goog', 'msft', ]

# list for bad test input
bad_l = ['foooo']


# tests for StockRetriever
class TestStockRetrieverMethods(unittest.TestCase):

    def test_get_stock_price(self):
        """test  a correct and incorrect input for get_stock_price
        """
        # Test good input
        self.assertIsNotNone(StockRetriever.get_stock_price(good_l[0]))
        self.assertIsNotNone(StockRetriever.get_stock_price(good_l[1]))
        self.assertIsNotNone(StockRetriever.get_stock_price(good_l[2]))
        # Test bad input
        self.assertIsNone(StockRetriever.get_stock_price(bad_l[0]))

    def test_calculate_difference(self):
        """test a correct and incorrect input for calculate_difference
        """
        # Test good input
        self.assertIsNotNone(StockRetriever.calculate_difference(good_l[0]))
        # Test bad input
        self.assertIsNone(StockRetriever.calculate_difference(bad_l[0]))

    def test_get_stock_data(self):
        """test that get_stock_data returns a dictionary
        """
        self.assertIs(type(StockRetriever.get_stock_data(good_l)), dict)

    def test_best_stock(self):
        """test that best_stock returns a string
        """
        self.assertIs(type(StockRetriever.best_stock(good_l)), str)


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

        remote_process.remote_remove(ip_address, username, 'test')
        remote_process.remote_ls(ip_address, username, 'test')

        remote_process.remote_remove(ip_address, username, 'test_vm_scp.py')
        remote_process.remote_ls(ip_address, username, 'test_vm_scp.py')


class TestDNS(unittest.TestCase):
    def test_config(self):
        __config_file__ = 'config.ini'
        with patch('builtins.input', side_effect=[f'{sys.argv[1]}', f'{sys.argv[2]}', f'{sys.argv[3]}']):
            gen_config()

        config = configparser.ConfigParser()
        config.read(__config_file__)

        self.assertEqual(config['dns']['domain'], f'{sys.argv[1]}')
        self.assertEqual(config['dns']['key'], f'{sys.argv[2]}')
        self.assertEqual(config['dns']['secret'], f'{sys.argv[3]}')


# tests for scp_aws
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
        with self.assertRaises(SCPException):
            vm_scp.upload_file('doesnt_exist.txt', ip, un)
        # valid local_path, default remote_path
        vm_scp.upload_file('test.txt', ip, un)
        # invalid local_path, invalid remote_path
        with self.assertRaises(SCPException):
            vm_scp.upload_file('doesnt_exist.txt', ip, un, 'doesnt_exist/')
        # valid local_path, invalid remote_path
        with self.assertRaises(SCPException):
            vm_scp.upload_file('test.txt', ip, un, 'doesnt_exist/')
        # sending itself
        vm_scp.upload_file('test.py', ip, un)
        scp_base_dir = os.path.dirname(os.path.realpath(__file__))
        vm_scp.upload_file(scp_base_dir, ip, un, recursive=True)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
