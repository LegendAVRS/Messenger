import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IP, SOCK_STREAM = TCP
client.connect(('localhost', 1002))  # 127.0.0.1
#nguoi dung nhap ten file
name = input("ten file: ")
file = open(name, 'rb')
image_data = file.read(2048)
#bat dau gui anh
while image_data:
    client.send(image_data)
    image_data = file.read(2048)
#da gui xong
file.close()
client.close()