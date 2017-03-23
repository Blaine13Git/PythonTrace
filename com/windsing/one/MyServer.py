import socket
import threading

bind_ip = '0.0.0.0'  # 表示本机
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)  # 最大积压连接数
print(">>正在监听%s:%d" % (bind_ip, bind_port))


# 对接入的client进行处理
def handle_client(client_socket):
    # print what the client send
    request = client_socket.recv(4096)
    print("接收的内容：%s" % request)
    client_socket.send(b"ACK!")
    client_socket.close()


while True:
    client, address = server.accept()  # 服务器接受访问，并返回连接对象和地址
    print("%s:%d 已经连接" % (address[0], address[1]))

    # 创建一个指向我们的handle_client函数的新线程对象，handle_client函数的参数设置为client
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()



