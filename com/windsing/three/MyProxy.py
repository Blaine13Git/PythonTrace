import sys
import socket
import threading


def server_loop(local_ip, local_port, remote_ip, remote_port, receive_first):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_ip, local_port))
    except:
        print("%s:%d 地址已经被占用" % (local_ip, local_port))
        sys.exit(0)

    print("正在监听的端口： %d" % local_port)
    server.listen(5)

    while True:
        client_socket, address = server.accept()
        print("%s:%d 连接到服务器" % (address[0], local_port[1]))

        proxy_thread = threading.Thread(target=proxy_handler,
                                        args=(client_socket, remote_ip, remote_port, receive_first))
        proxy_thread.start()


def proxy_handler(client_socket, remote_ip, remote_port, receive_first):

    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_ip, remote_port))

    # receive data from the remote end if necessary
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

        # send it to our response handler
        remote_buffer = response_handler(remote_buffer)

        # if we have data to send to our local client, send it
        if len(remote_buffer):
            print("Sending %d byte to localhost" % len(remote_buffer))
            client_socket.send(remote_buffer)

    # now lets loop and read from local,
    # send to remote, send to local
    while True:
        # read from local host
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            print("Received %d bytes from localhost." % len(local_buffer))
            hexdump(local_buffer)

            # send it to our request handler
            local_buffer = request_handler(local_buffer)

            # send off the data to the remote host
            remote_socket.send(local_buffer)
            print("Send to remote")

        # receive back the response
        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):



def main():
    if len(sys.argv[1:]) != 5:
        print("Usage: MyProxy.py [local_ip] [local_port] [remote_ip] [remote_port] [receive_first]")
        print("Example: MyProxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)

    # set local listen parameters
    local_ip = sys.argv[1]
    local_port = int(sys.argv[2])

    # set remote target
    remote_ip = sys.argv[3]
    remote_port = sys.argv[4]

    # this tells our proxy to connect and receive data before sending to the remote host
    receive_first = sys.argv[5]

    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False

    # now spin up our listening socket
    server_loop(local_ip, local_port, remote_ip, remote_port, receive_first)


main()
