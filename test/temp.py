import unittest
import os
import sys
from unittest.mock import patch

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from glaros_ssh import remote_process
from cloud_service_providers.AzureCSP import AzureCSP
import configparser
from dns import gen_config
import StockRetriever

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


if __name__ == '__main__':
    unittest.main()


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


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
