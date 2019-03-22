import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

if __name__ == '__main__':
    for data in [b"Python", b"UDP", b"World"]:
        client.sendto(data, ("127.0.0.1", 10000))
        print(client.recv(1024).decode("utf-8"))
    client.close()
