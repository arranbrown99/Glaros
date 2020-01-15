import remote_process

ip_address = "54.194.29.151"
username = 'ec2-user'

def test_remote():
    assert(remote_process.remote_python(ip_address,username,'infinite.py')) == True,"should run a python program in the background"
    assert(remote_process.remote_remove(ip_address,username,'test.txt')) == True,"should delete the file test.txt if it exists"
    assert(remote_process.remote_remove(ip_address,username,'scp')) == True,"should delete the directory scp if it exists"
    assert(remote_process.remote_remove(ip_address,username,'vm_scp.py')) == True,"should delete the file vm_scp.py if it exists"
    assert(remote_process.remote_remove(ip_address,username,'nohup.out')) == True,"should delete the file test.txt if it exists"
    assert(remote_process.remote_remove(ip_address,username,'cs27-main')) == True,"should delete the file test.txt if it exists"






if __name__ == '__main__':
    test_remote()
    print("All tests passed OK.")
