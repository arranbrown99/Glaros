from glaros_ssh import remote_process


from cloud_service_providers.AzureCSP import AzureCSP
from cloud_service_providers.AwsCSP import AwsCSP
# inputs
aws_vm = AwsCSP()
ip_address = aws_vm.get_ip()
username = aws_vm.get_username()

def test_remote():
#    assert(remote_process.remote_python(ip_address,username,'infinite.py')) == True,"should run a python program in the background"
    assert(remote_process.remote_remove(ip_address,username,'test.txt')) == True,"should delete the file test.txt if it exists"
    assert(remote_process.remote_remove(ip_address,username,'scp')) == True,"should delete the directory scp if it exists"
    assert(remote_process.remote_remove(ip_address,username,'vm_scp.py')) == True,"should delete the file vm_scp.py if it exists"
    assert(remote_process.remote_remove(ip_address,username,'nohup.out')) == True,"should delete the file test.txt if it exists"
#    assert(remote_process.remote_remove(ip_address,username,'cs27-main')) == True,"should delete the file test.txt if it exists"

def test_mkdir():
    dir_name = 'test_mkdir'
    remote_process.remote_mkdir(ip_address,username,dir_name)
   # assert(remote_process.remote_ls(ip_address,username,'-d test_mkdir')) == 'test_mkdir'
    ls_output = remote_process.remote_ls(ip_address,username,'-d ' + dir_name)[0].strip('\n')
    assert(ls_output == dir_name),"remote_mkdir should create a remote directory"
    remote_process.remote_remove(ip_address,username,dir_name)
    ls_output = remote_process.remote_ls(ip_address,username,'-d ' + dir_name)
    assert(ls_output == []),"after remote_remove should be no directory with that name"

if __name__ == '__main__':
    test_remote()
    test_mkdir()
    print("All tests passed OK.")
