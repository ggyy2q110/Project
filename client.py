"""
ftp多线程客户端 第一种方案
"""
from socket import *
import sys, time

# 全局变量
Host = "192.168.139.130"
Port = 8800
Server_addr = (Host, Port)


# ftp客户端
class Client:
    def __init__(self, sock_tcp):
        self.sock_tcp = sock_tcp

    def do_exit(self):
        self.sock_tcp.send(b"E")
        self.sock_tcp.close()
        sys.exit("谢谢使用")

    def do_list(self):
        self.sock_tcp.send(b"L")
        data = self.sock_tcp.recv(1024).decode()
        if data == "OK":
            file_list = self.sock_tcp.recv(4096)
            print(file_list.decode())
        else:
            print(data.decode())

    def do_get(self, filename):
        msg = "G " + filename
        self.sock_tcp.send(msg.encode())
        data = self.sock_tcp.recv(128).decode()
        if data == "OK":
            f = open(filename, "wb")
            while True:
                data = self.sock_tcp.recv(1024)
                if data == b"##":
                    break
                f.write(data)
                f.flush()
            f.close()
        else:
            print(data)

    def do_post(self, filename):
        msg = "P " + filename
        self.sock_tcp.send(msg.encode())
        data = self.sock_tcp.recv(128).decode()
        if data == "OK":
            f = open(filename, "rb")
            while True:
                data = f.read(1024)
                if not data:
                    time.sleep(0.1)
                    self.sock_tcp.send(b"##")
                    f.close()
                    break
                self.sock_tcp.send(data)
        else:
            print(data)


# 客户端启动函数
def main():
    sock_tcp = socket()
    sock_tcp.connect(Server_addr)
    ftp = Client(sock_tcp)
    while True:
        print("查看:list")
        print("下载:get filename")
        print("上传:pos filename")
        print("退出:exit")
        msg = input("请输入命令:")
        if msg == "exit":
            ftp.do_exit()
        elif msg == "list":
            ftp.do_list()
        elif msg[:3] == "get":
            filename = msg.split(" ")[-1]
            ftp.do_get(filename)
        elif msg[:3] == "pos":
            filename = msg.split(" ")[-1]
            ftp.do_post(filename)
        else:
            print("请输入正确命令:")


if __name__ == '__main__':
    main()
