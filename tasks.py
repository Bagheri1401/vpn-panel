import paramiko

def create_v2ray_user(server, username, uuid):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=server.ip_address, port=server.ssh_port, username=server.ssh_user, key_filename=server.ssh_key_path)
    command = f"bash /etc/v2ray/add_user.sh {username} {uuid}"
    stdin, stdout, stderr = client.exec_command(command)
    result = stdout.read().decode()
    client.close()
    return result
