import unittest
from dns import change_service


class TestDNS(unittest.TestCase):
    def test_a_record(self):
        '''
        Test that the a_record has been updated
        '''
