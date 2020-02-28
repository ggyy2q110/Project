"""
http server
"""
from socket import *
from select import *


class Httpd:
    def __init__(self, host="0.0.0.0", port=8888, dir=None):
        self.host = host
        self.port = port
        self.dir = dir
        self.map = {}
        self.sok_tcp = socket()
        self.sok_tcp.bind((self.host, self.port))
        self.sok_tcp.setblocking(False)

    def start(self):
        self.sok_tcp.listen(5)
        ep = epoll()
        ep.register(self.sok_tcp, EPOLLIN)
        self.map = {self.sok_tcp.fileno(): self.sok_tcp}
        while True:
            events = ep.poll()
            for fd, event in events:
                if fd == self.sok_tcp.fileno():
                    con_tcp, addr = self.map[fd].accept()
                    con_tcp.setblocking(False)
                    ep.register(con_tcp, EPOLLIN)
                    self.map[con_tcp.fileno()] = con_tcp
                elif event & EPOLLIN:
                    self.handle(self.map[fd], ep, fd)

    def handle(self, con_tcp, ep, fd):
        data = con_tcp.recv(1024)
        if not data:
            ep.unregister(fd)
            self.map[fd].close()
            del self.map[fd]
            return
        info = data.decode().split(" ")[1]
        if info == "/":
            info = "index.html"
        try:
            f = open(self.dir + info)
        except:
            data = "HTTP/1.1 404 Not Found\r\n"
            data += "Content-Type:text/html\r\n"
            data += "\r\n"
            data += "Sorry...."
        else:
            data = "HTTP/1.1 200 OK\r\n"
            data += "Content-Type:text/html\r\n"
            data += "\r\n"
            data += f.read()
            f.close()
        con_tcp.send(data.encode())


if __name__ == '__main__':
    host = "192.168.139.130"
    port = 8800
    dir = "../day11/"
    httpd = Httpd(host, port, dir)
    httpd.start()
