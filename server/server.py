import socket


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IP, SOCK_STREAM = TCP
server.bind(('localhost', 1002))  # 127.0.0.1
server.listen()

client_socket, client_address = server.accept()
username = "quant" #ten tai khoan dang ki
avatar = username + ".png" #tao ten file avatar theo ten dang ki
file = open(avatar, "wb")
image_chunk = client_socket.recv(2048)  # bat dau nhan hinh
while image_chunk:
    file.write(image_chunk)
    image_chunk = client_socket.recv(2048)
#nhan xong
file.close()
client_socket.close()