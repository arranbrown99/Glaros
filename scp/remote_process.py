import vm_scp

def start_process(ip_address,username):
    key = vm_scp.get_key_for_host(ip_address)
    ki = RSAkey.from_private_key_file(key)

    

