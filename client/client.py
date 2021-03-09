import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IP, SOCK_STREAM = TCP
client.connect(('localhost', 1002))  # 127.0.0.1

ftype = input('select type:')
client.send(bytes(ftype, 'utf-8'))
if ftype == '/image':
    filename = input('filename:')
    file = open(filename, 'rb')
    image_data = file.read(2048)

    while image_data:
        client.send(image_data)
        image_data = file.read(2048)

    file.close()
elif ftype == '/text':
    filename = input('filename:')
    file = open(filename, 'rb')
    image_data = file.read(2048)

    while image_data:
        client.send(image_data)
        image_data = file.read(2048)

    file.close()
else:
    pass
client.close()