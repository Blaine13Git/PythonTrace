import socket

# dict.youdao.com/
# target_host = "dict.youdao.com"
# target_port = 80
target_host = "localhost"
target_port = 9999

# create socket object
# IPv4 = socket.AF_INET
# TCP = socket.SOCK_STREAM
my_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
my_client.connect((target_host, target_port))
print("<<<<<<<<<<<<<<>>>>>>>>>>>>>>")

# sent some data
# my_client.send(b"GET / HTTP/1.1\r\nHost:dict.youdao.com\n")
my_client.send(b"hello server 0")

# receive some data
my_response = my_client.recv(4096)
print(my_response)
