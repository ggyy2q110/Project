"""
ftp多线程服务端
"""
from socket import *
from multiprocessing import Process
import signal, time, os, sys

# 全局变量
Host = "192.168.139.130"
Port = 8800
Server_addr = (Host, Port)
FTP = "../day14/"


# ftp服务端
class Server(Process):
    def __init__(self, conn_tcp):
        super().__init__()
        self.conn_tcp = conn_tcp

    def list(self):
        file_list = os.listdir(FTP)
        if not file_list:
            self.conn_tcp.send("文件库为空".encode())
            return
        else:
            self.conn_tcp.send(b"OK")
            time.sleep(0.1)

        # 发送文件列表
        data = "\n".join(file_list)
        self.conn_tcp.send(data.encode())

    def get(self, filename):
        try:
            f = open("%s%s" % (FTP, filename), "rb")
        except:
            self.conn_tcp.send("文件不存在".encode())
            return
        else:
            self.conn_tcp.send(b"OK")
            time.sleep(0.1)

        # 发送下载文件
        while True:
            data = f.read(1024)
            if not data:
                time.sleep(0.1)
                self.conn_tcp.send(b"##")
                break
            else:
                self.conn_tcp.send(data)
        f.close()

    def post(self, filename):
        try:
            f = open("%s%s" % (FTP, filename), "rb")
        except:
            self.conn_tcp.send(b"OK")
            time.sleep(0.1)
        else:
            self.conn_tcp.send("文件已经存在".encode())
            return

            # 接收上传文件
        f = open("%s%s" % (FTP, filename), "wb")
        while True:
            data = self.conn_tcp.recv(1024)
            if data == b"##":
                f.close()
                break
            f.write(data)
            f.flush()

    def run(self):
        while True:
            data = self.conn_tcp.recv(1024).decode()
            if not data or data[0] == "E":
                return
            elif data[0] == "L":
                self.list()
            elif data[0] == "G":
                filename = data.split(" ")[-1]
                self.get(filename)
            elif data[0] == "P":
                filename = data.split(" ")[-1]
                self.post(filename)


# 客户端启动函数
def main():
    sock_tcp = socket()
    sock_tcp.bind(Server_addr)
    sock_tcp.listen(5)
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    while True:
        conn_tcp, addr = sock_tcp.accept()
        print("from", addr)
        p = Server(conn_tcp)
        p.start()


if __name__ == '__main__':
    main()
