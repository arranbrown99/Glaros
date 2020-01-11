import remote_process

ip_address = '34.196.229.24'
username = 'test2'

def test_remote():
    remote_process.remote_python(ip_address,username,'infinite.py')

if __name__ == '__main__':
    test_remote()
    print("All tests passed OK.")
