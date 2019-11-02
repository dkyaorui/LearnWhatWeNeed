import socket

if __name__ == '__main__':
    # socket.SOCK_STREAM declare the TCP connection
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 建立连接 create a connection
    client.connect(("127.0.0.1", 10000))
    # 接收数据 receive the data
    print(client.recv(1024).decode('utf-8'))
    for data in [b'Python', b'TCP', b'World']:
        client.send(data)
        print(client.recv(1024).decode('utf-8'))
    client.send(b'exit')
    client.close()
