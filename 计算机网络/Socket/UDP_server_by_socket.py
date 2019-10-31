"""
使用socket模块创建UDP服务器
use socket package to create a UDP server
"""
import socket
# socket.SOCK_DGRAM declare the UDP connection
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

if __name__ == '__main__':
    server.bind(("127.0.0.1", 10000))
    print("Waiting for receiving data....")
    while True:
        data, addr = server.recvfrom(1024)
        print("Received from %s:%s" % addr)
        print("Data: %s" % data.decode("utf-8"))
        server.sendto(b"Hello, %s" % data, addr)
