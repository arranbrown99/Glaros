import unittest
import Driver

ip_address = "54.194.29.151"
username = 'ec2-user'


class TestRemoteProcess(unittest.TestCase):

    def test_remote(self):
        # Delete specified file or directory if it exists
        self.assertTrue(
            remote_process.remote_remove(ip_address, username, 'test.txt'))
        self.assertTrue(
            remote_process.remote_remove(ip_address, username, 'scp'))
        self.assertTrue(
            remote_process.remote_remove(ip_address, username, 'vm_scp.py'))
        self.assertTrue(
            remote_process.remote_remove(ip_address, username, 'nohup.out'))
        self.assertTrue(
            remote_process.remote_remove(ip_address, username, 'cs27-main'))


if __name__ == '__main__':
    unittest.main()
