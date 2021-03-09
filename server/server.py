import socket


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IP, SOCK_STREAM = TCP
server.bind(('localhost', 1002))  # 127.0.0.1
server.listen()

client_socket, client_address = server.accept()
ftype = client_socket.recv(2048).decode()
if ftype == '/image':
    file = open('server.png', "wb")
    image_chunk = client_socket.recv(2048)  # stream-based protocol

    while image_chunk:
        file.write(image_chunk)
        image_chunk = client_socket.recv(2048)

    file.close()
elif ftype == '/text':
    file = open('server.txt', "wb")
    image_chunk = client_socket.recv(2048)  # stream-based protocol

    while image_chunk:
        file.write(image_chunk)
        image_chunk = client_socket.recv(2048)

    file.close()
client_socket.close()