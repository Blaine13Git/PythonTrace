import sys
import threading
import socket
import getopt
import subprocess

# 定义全局变量
listen = False
command = False
upload = False
execute = ""
target = ""
port = 0
upload_destination = ""


# 创建一个负责处理命令行参数的主函数，并调用其余的函数
def usage():
    print("Net Tool\n")
    print("Usage: MyNetcat.py -t target_host -p port ")
    print("-l  --listen  - listen on [host]:[port] for incoming connections")
    print("-e  --execute  - execute the given file upon receiving a connection")
    print("-c  --command  - initialize a command shell")
    print("-u  --upload  - upon receiving connection upload a file and write to [destination]")

    print("Examples:")
    print("MyNetcat.py -t 192.168.0.1 -p 5555 -l -c")
    print("MyNetcat.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe")
    print("MyNetcat.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"")
    print("echo 'ABCDEFGHI' | ./MyNetcat.py -t 192.168.11.12 -p 135")
    sys.exit(1)


def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((target, port))
        if len(buffer):
            client.send(buffer)
        while True:
            recv_len = 1
            response = ""
            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data
                if recv_len < 4096:
                    break
            print(response)

            buffer = raw_input("")
            buffer += "\n"
            client.send(buffer)
    except:
        print("异常，退出")
        client.close()

    print()


def main():
    global listen
    global command
    global upload
    global execute
    global target
    global port
    global upload_destination

    if not len(sys.argv[1:]):
        usage()

    # read the command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu",
                                   ["help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print(str(err))

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"

    # listen or just send data from stdin?
    if not listen and len(target) and port > 0:
        # read in the buffer from the commandline, this will block, so send CTRL-D if not sending input
        buffer = sys.stdin.read()

        # send data off
        client_sender(buffer)

    if listen:
        server_loop()


main()


def server_loop():
    print()
