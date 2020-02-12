from unittest.mock import patch
import configparser

from dns import gen_config


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
