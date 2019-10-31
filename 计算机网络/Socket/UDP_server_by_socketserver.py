"""
使用socketserver模块创建UDP服务器
UDPServer 是单线程的，如果你想创建多进程/多线程的UDPserver 请使用ForkingUDPServer/ThreadingUDPServer。

use socketserver package to create a UDP server
The UDPServer is a single thread server.IF you want to creat a multithreading/multiforking server,
please use the ForkingUDPServer/ThreadingUDPServer package.
"""
from socketserver import BaseRequestHandler, UDPServer
import time


class EchoHandle(BaseRequestHandler):
    def handle(self):
        print("Get a UDP connection from {}".format(self.client_address))
        time.sleep(1)
        msg, sock = self.request
        print(msg)
        sock.sendto(b"hi", self.client_address)


if __name__ == '__main__':
    server = UDPServer(("127.0.0.1", 10000), EchoHandle)
    server.serve_forever()
