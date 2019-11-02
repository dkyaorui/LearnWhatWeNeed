"""
使用socketserver模块创建TCP服务器。
TCPServer 是单线程的，如果你想创建多进程/多线程的TCPserver 请使用ForkingTCPServer/ThreadingTCPServer。

use socketserver package to create a TCP server
The TCPServer is a single thread server.IF you want to creat a multithreading/multiforking server,
please use the ForkingTCPServer/ThreadingTCPServer package.
"""
from socketserver import TCPServer, StreamRequestHandler
import time


class EchoHandler(StreamRequestHandler):
    def handle(self):
        print("Get a connection from {}".format(self.client_address))
        self.request.send(b"hello")
        while True:
            data = self.request.recv(1024).strip()
            time.sleep(1)
            if not data or data.decode("utf-8") == "exit":
                break
            self.request.send(("Hello %s!" % data.decode("utf-8")).encode("utf-8"))
        print("Connection from %s:%s closed" % self.client_address)


if __name__ == '__main__':
    server = TCPServer(("127.0.0.1", 10000), EchoHandler)
    server.serve_forever()
