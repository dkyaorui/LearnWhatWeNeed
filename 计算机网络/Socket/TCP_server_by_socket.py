"""
使用socket模块创建TCP服务器
use socket package to create a TCP server
"""
import socket
import threading
import time
# socket.SOCK_STREAM declare the TCP connection
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def tcp_link(sock, addr):
    print("Accept a new connection from %s:%s" % addr)
    # send a data to client
    sock.send(b'Welcome to tcp server test')
    while True:
        # receive 1024 bytes data every time
        data = sock.recv(1204)
        time.sleep(1)
        if not data or data.decode("utf-8") == "exit":
            break
        sock.send(("Hello %s!" % data.decode("utf-8")).encode("utf-8"))
    sock.close()
    print("Connection from %s:%s closed" % addr)


if __name__ == '__main__':
    # 监听端口 listen the port 127.0.0.1
    server.bind(("127.0.0.1", 10000))
    # 限制最大链接数 limit the max number of connections
    server.listen(3)
    print("Waiting for connecting...")
    while True:
        sock, addr = server.accept()
        # 使用线程处理新的请求 use the threading to process the new request
        _thread = threading.Thread(target=tcp_link, args=(sock, addr))
        _thread.start()

