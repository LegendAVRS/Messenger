from socket import AF_INET, SOCK_STREAM, socket, gethostname, gethostbyname
from threading import Thread
import time
import datetime
from collections import OrderedDict
import os

from users import User
import info_database as db
import chat_store as store

# MỞ CMD
# os.system("start cmd")

# CÁC LỆNH KẾT NỐI VỚI SERVER
LOGIN = "/login"
REGISTER = "/register"
QUIT = "/quit"
LOGOUT = "/logout"
CLEAR = "/clear"
USERNAME = "/usr"
PASSWORD = "/pwd"
LIST = "/list"
ONLINE_LIST = "/online_list"
MOVE = "/tp"
HELP = "/help"
RE_LOCATION = "/re_location"
AT_SERVER = "SERVER"


OK = "ACCEPTED"

# PHẢN HỒI TỪ SERVER
login_instruction = "[SERVER] Insert [/login <username> <password>]"
error = "[SERVER] Unvalid Command."
username_error = "[SERVER] Username not valid."
password_error = "[SERVER] Wrong password."
account_used = "[SERVER] This account is being used"
username_instruction = "[SERVER] Insert username with [/usr + <name>]"
password_instruction = "[SERVER] Insert and confirm password with [/pwd <password> <password>]"
username_exist = "[SERVER] Username has already existed"
username_not_exist = "[SERVER] Username does not exist"
wrong_confirmation = "[SERVER] Wrong password confirmation"

"""========================================================================================================"""
# HẰNG TOÀN CỤC
PORT = 5050
BUFSIZ = 512
HOST = "localhost"
# HOST = gethostbyname(gethostname())
ADDR = (HOST, PORT)
MAX_CONNECTION = 15


"""========================================================================================================"""
# BIẾN TOÀN CỤC
client_info = {} # tài khoản và mật khẩu người dùng
client_online = OrderedDict() # người dùng đang online
client_location = {} # đối tượng mà người dùng đang chat


"""========================================================================================================"""

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR) # tạo server 

def get_messages(client):
    """
    => Lấy tin nhắn từ người dùng
    param client: client của người dùng 
    return: trả về tin nhắn nếu có ngược lại trả về False 
    """

    try:
        message = client.recv(BUFSIZ).decode()
        return message
    except Exception as e:
        print("[EXCEPTION in GET]", e)
        return False


def send_messages(client, msg):
    """
    => Gửi tin ngắn tới người dùng
    param client: client của người dùng
    param msg   : tin nhắn muốn gửi
    return: None
    """
    # client.send(bytes(msg, "utf8"))
    try:
        client.send(bytes(msg, "utf8"))
    except Exception as e:
        print("[EXCEPTION in SEND]", e)


def client_login(client):
    """
    => Trang ĐĂNG NHẬP TÀI KHOẢN
    param client: client của người dùng
    return: trả về User nếu không vấn đề
                   QUIT nếu thoát
                   -1 nếu sinh lỗi
    """

    send_messages(client, "[SERVER] LOGIN PAGE")
    time.sleep(0.1)

    try:
        while True:
            send_messages(client, login_instruction)
            msg = get_messages(client)

            if msg == False: # không nhận được tin nhắn
                return -1

            if msg == QUIT: # thoát
                return QUIT

            temp = msg.split()

            if len(temp) != 3:
                send_messages(client, error)
                continue

            cmd, username, password = temp
            if cmd != LOGIN:
                send_messages(client, error)
                continue

            if username in client_online: # tài khoản đang được sử dụng
                send_messages(client, account_used)
                continue

            if username not in client_info: # tài khoản không tồn tại
                send_messages(client, username_error)
                continue
            
            if password != client_info[username]: # sai mật khẩu
                send_messages(client, password_error)
                continue

            return User(username, password)
 
    except Exception as e:
        print("[EXCEPTION in LOGIN]", e)
        return -1


def client_register(client):
    """
    => Trang ĐĂNG KÝ TÀI KHOẢN
    param client: client của người dùng
    return: trả về OK nếu không vấn đề
                   QUIT nếu thoát
                   -1 nếu sinh lỗi
    """

    send_messages(client, "[SERVER] REGISTER PAGE")
    time.sleep(0.1)

    username, password = None, None

    # Đăng ký tài khoản
    try:
        while True:
            send_messages(client, username_instruction)
            
            msg = get_messages(client)

            if msg == False: # không nhận được tin nhắn
                return -1

            if msg == QUIT: # thoát 
                return QUIT

            temp = msg.split()

            if len(temp) != 2:
                send_messages(client, error)
                continue

            cmd, name = temp
            
            if cmd != USERNAME:
                send_messages(client, error)
                continue

            if db.exist(name) == True: # nếu username đã tồn tại
                send_messages(client, username_exist)
                continue

            username = name
            break
    except Exception as e:
        print("[EXCEPTION in USERNAME]", e)
        return -1


    send_messages(client, CLEAR)
    time.sleep(0.1)
    send_messages(client, f"[SERVER] Your username is {username}")

    # Đăng ký mật khẩu
    try:
        while True:
            send_messages(client, password_instruction)

            msg = get_messages(client)

            if msg == False: # không nhận được tin nhắn
                return -1

            if msg == QUIT: # thoát
                return QUIT

            temp = msg.split()

            if len(temp) != 3:
                send_messages(client, error)
                continue

            cmd, pwd, confirm = temp

            if cmd != PASSWORD:
                send_messages(client, error)
                continue
            
            if pwd != confirm: # nếu mật khẩu khác mật khẩu nhập lại
                send_messages(client, wrong_confirmation)
                continue

            password = pwd
            break
    except Exception as e:
        print("[EXCEPTION in PASSWORD]", e)
        return -1
           

    # Đăng ký thành công

    user = User(username, password) # tạo một User mới 
    # db.insert(user) # lưu trữ vào database

    # Tạo khung lưu trữ mới
    newpath = store.mainpath + username + ".db"
    store.path = newpath
    store.create_table()

    print("[ANNOUNCEMENT] New user has been added") # Thông báo tài khoản mới đc đăng ký
    print("=> ",user.username, user.password)
    return OK


def List(client):
    """
    => Gửi danh sách những tài khoản đã đăng ký
    param client: client của người dùng
    return: None
    """

    client_list = db.getall()
    msg = f"[SERVER] There are {len(client_list)} account"
    more = ":\n" if len(client_list) <= 1 else "s:\n"
    msg = msg + more
    for user in client_list:
        msg = msg + "\t\t- " + str(user[0]) + "\n"
    send_messages(client, msg)


def Online_list(client):
    """
    => Gửi danh sách những người đang online
    param client: client của người dùng
    return: None
    """

    msg = f"[SERVER] There are {len(client_online)} online account"
    more = ":\n" if len(client_online) <= 1 else "s:\n"
    msg = msg + more
    for username in client_online:
        msg = msg + "\t\t- " + str(username) + "\n"
    send_messages(client, msg)
        

def Help(client):
    """
    => Gửi danh sách câu lệnh được sử dụng với SERVER
    param client: client của người dùng
    return: None
    """


    msg = """
        "/quit":                Quit to menu
        "/clear":               Clear your screen
        "/list"                 List all accounts
        "/online_list"          List all online accounts
        "/tp + <name>"          Move to chat room with <name>
        "/help"                 List all command 
    """
    send_messages(client, msg)


def client_chat(client, name, receiver):
    """
    => Phần chat giữa name và receiver
    param client: client của người dùng
    param name: tên người dùng
    param receiver: tên đối tượng chat
    """

    welcome = f"""
                {"=" * 40}
                {f"Yourname = {name};".center(40)}
                {f"Receiver = {receiver}".center(40)}
                {"=" * 40}\n"""

    send_messages(client, CLEAR)
    time.sleep(0.1)
    send_messages(client, welcome)
    
    # Mở tất cả đoạn chat
    newpath = store.mainpath + name + ".db"
    store.path = newpath
    text = store.show(receiver)
    send_messages(client, text)

    while True:
        msg = get_messages(client)

        if msg == False:
            return -1
        
        if msg == QUIT:
            return QUIT

        if receiver in client_online and client_location[receiver] == name:
            recv_conn, recv_addr = client_online[receiver]
            send_messages(recv_conn, f"![{name}] {msg}")
        
        # lưu trữ message của bản thân
        newpath = store.mainpath + name + ".db"
        store.path = newpath
        store.update_chat(receiver, f"[You] {msg}\n")

        # Lưu trữ message của đối tượng chat
        newpath = store.mainpath + receiver + ".db"
        store.path = newpath
        store.update_chat(name, f"[{name}] {msg}\n")
            
            
            


def client_and_server(client, addr):
    """
    => Giao tiếp giữa SERVER và người dùng
    param client: client của người dùng
    param addr  : địa chỉ của người dùng
    return: None
    """


    send_messages(client, "[SERVER] Welcome back to VLC chat room!!!")
    time.sleep(0.1)
    send_messages(client, "[SERVER] Use '/login' to login or '/register' to register")
    time.sleep(0.1)

    user = None
    disconnect_msg = f"[DISCONNECTION] {addr} has disconnected"

    # Đăng nhập hoặc Đăng ký tài khoản
    while True:
        msg = get_messages(client)

        if msg == False: # không nhận được tin nhắn
            print(disconnect_msg) # thông báo đường truyền bị ngắt
            return

        if msg == REGISTER: # Phần ĐĂNG KÝ
            send_messages(client, CLEAR)

            command = client_register(client) # vào hàm ĐĂNG KÝ

            if command == -1: # sinh lỗi
                print(disconnect_msg) # thông báo đường truyền bị ngắt
                return

            if command == QUIT: # thoát
                send_messages(client, CLEAR)
                client_and_server(client, addr)
                return

            time.sleep(0.1)
            send_messages(client, CLEAR)
            time.sleep(0.1)
            send_messages(client, "[SERVER] Please login again!!!\n") # Đăng nhập lại sau khi Đăng ký

            client_and_server(client, addr)
            return


        elif msg == LOGIN: # Phần ĐĂNG NHẬP
            send_messages(client, CLEAR)

            temp_user = client_login(client) # vào hàm ĐĂNG NHẬP

            if temp_user == QUIT: # thoát
                send_messages(client, CLEAR)
                client_and_server(client, addr)
                return

            if temp_user == -1: # sinh lỗi
                print(disconnect_msg) # thông báo đường truyền bị ngắt
                return

            user = temp_user
            break

        else:
            try:
                send_messages(client, error)
                send_messages(client, "[SERVER] Use '/login' to login or '/register' to register")
            except Exception as e:
                print("[EXCEPTION in CONNECTION]", e)
                return -1


    # Truy cập tài khoản thành công
    send_messages(client, CLEAR)
    time.sleep(0.1)
    send_messages(client, "[SERVER] Correct password.")
    time.sleep(0.1)
    send_messages(client, CLEAR)
    time.sleep(0.1)
    send_messages(client, f"""
                ==============================================
                \t\tWelcome back {user.username}
                ==============================================""")

    client_online[user.username] = (client, addr)
    client_location[user.username] = AT_SERVER

    # Truy cập chat
    while True:
        msg = get_messages(client)

        if msg == False:
            print(disconnect_msg + f" with name = {user.username}")
            try:
                client_online.pop(user.username)
            except Exception as e:
                print("[EXCEPTION in DISCONNECTION] Failed to disconnect")
            return

        if msg == LOGOUT: # đăng xuất
            print(f"[LOGOUT] {user.username} has logged out") 
            
            send_messages(client, CLEAR)
            time.sleep(0.1)
            send_messages(client, "[SERVER] You have been logged out") 
            time.sleep(0.1)
            send_messages(client, CLEAR)
            time.sleep(0.1)
            try:
                client_online.pop(user.username)
            except Exception as e:
                print("[EXCEPTION in DISCONNECTION] Failed to disconnect")
            client_and_server(client, addr)
            return

        if msg == LIST: # liệt kê danh sách tài khoản
            List(client)
            continue

        if msg == ONLINE_LIST: # liệt kê danh sách online
            Online_list(client)
            continue

        if msg == HELP: # liệt kê danh sách lệnh hỗ trợ
            Help(client)
            continue

        temp = msg.split()

        if len(temp) != 2:
            send_messages(client, error)
            continue
        
        cmd, receiver = temp

        if cmd != MOVE: # kiểm tra lệnh MOVE
            send_messages(client, error)
            continue

        if receiver == user.username:
            send_messages(client, "[SERVER] This is your account.")
            continue

        if receiver not in client_info: # nếu tên tài khoản không nằm trong danh sách
            send_messages(client, username_not_exist)
            continue

        # Chọn thành công đối tượng chat
        client_location[user.username] = receiver
        command = client_chat(client, user.username, receiver)

        if command == -1: # chạy sinh lỗi hoặc chương trình client bị tắt đột ngột
            print(disconnect_msg + f" with name = {user.username}")
            return

        if command == QUIT: # Trở lại menu chính hay nói cách khác là chạy lại vòng lặp
            client_location[user.username] = AT_SERVER
            continue
                
            
        


def connection():
    """
    => Wait for connection from new clients, start new thread once connected
    :return: None
    """


    while True:
        try:
            client, addr = SERVER.accept()
            print(f"[CONNECTION] Connection from {addr}")

            Thread(target=client_and_server, args=(client, addr)).start()
        except Exception as e:
            print("[EXCEPTION]", e)
            break
    print("[END] The server has been crashed!!!")


def get_info():
    """
    => get client's username and password
    :return: a dictionary stores the username and password
    """

    account = dict(db.getall())
    return account


if __name__ == "__main__":
    # get all username and password 
    client_info = get_info()
    client_info["SERVER"] = "NoNeedToAsk" # Tạo một tài khoản giả cho SERVER
    print(client_info)

    # open server with some connections
    print("[LISTENING] Server is starting...")
    SERVER.listen(MAX_CONNECTION)

    # start the server
    server_thread = Thread(target=connection)
    server_thread.start()
    server_thread.join()
    SERVER.close()

