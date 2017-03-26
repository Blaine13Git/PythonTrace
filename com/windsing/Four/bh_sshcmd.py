import paramiko


def ssh_command(ip,user,passwd,command):
    client = paramiko.SSHClient()
