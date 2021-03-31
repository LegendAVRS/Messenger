from socket import AF_INET, SOCK_STREAM, socket, gethostname, gethostbyname
from threading import Thread
import time
import datetime
from collections import OrderedDict
from shutil import copyfile
import os
import cv2

from users import User
import info_database as db
import chat_store as store
import groupname_store as groupname
import groupmem_store as groupmem
import groupchat_store as groupchat

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
JOIN = "/join"
HELP = "/help"
GROUP_LIST = "/group_list"

PARTY_CREATE = "/party_create"
PARTY_INVITE = "/party_invite"

RE_LOCATION = "/re_location"


"""========================================================================================================"""
# CÁC NHÃN
AT_GROUP = "GROUP="
AT_SERVER = "SERVER"
CREATOR = "HOST"
ADMIN = "ADMIN"
MEMBER = "MEMBER"
OK = "ACCEPTED"
ERROR = "ERROR"
CODE_NAME = "#NAME#"
CONNECT = "CONNECT"
DISCONNECT = "DISCONNECT"
ADD = "ADD"
GROUP = "GROUP"
AVATAR = "AVATAR"
SET_AVA = "SET_AVA"

# PHẢN HỒI TỪ SERVER
login_instruction = "Insert [/login <username> <password>]"
error = "Invalid Command."
username_error = "Username not valid."
password_error = "Wrong password."
account_used = "This account is being used"
username_instruction = "Insert username with [/usr + <name>]"
password_instruction = "Insert and confirm password with [/pwd <password> <password>]"
username_exist = "Username has already existed"
username_not_exist = "Username does not exist"
wrong_confirmation = "Wrong password confirmation"

party_create_instruction = "Insert [/party create <group name>]"
party_invite_instruction = "Insert [/party invite <username>]"
group_exist = "Group name has already existed"
group_not_exist = "Group name does not exist"
is_member = "This member is in your group"
group_ok = "You have successfully created a group: "
not_member = "You are not a member in this group"

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
client_info = {}  # tài khoản và mật khẩu người dùng
client_online = OrderedDict()  # người dùng đang online
client_location = {}  # đối tượng mà người dùng đang chat
group = {}  # tên các nhóm gồm các thành viên của nhóm


"""========================================================================================================"""

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)  # tạo server

def Avatar(client, name):
    """
    => Gửi avatar cho người dùng
    param client: client của người dùng
    param name: tên người dùng
    return: None
    """

    path = __file__[:-9] + "\\avatar\\" + name + ".png"

    # img_file = open(__file__[:-9] + "\\avatar\\" + "test.png", "wb")

    with open(path, "rb") as image:
        cnt = 0
        image_data = image.read(512)
        while image_data:
            cnt += 1
            image_data = image.read(512)

    send_messages(client, f"#LEN#{str(cnt)}")

    with open(path, "rb") as image:
        image_data = image.read(512)
        while image_data:
            client.send(image_data)
            image_data = image.read(512)
    time.sleep(5)
    send_messages(client, "ENDofFILE")

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
        time.sleep(0.1)
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

    send_messages(client, "LOGIN PAGE")

    try:
        while True:
            send_messages(client, login_instruction)
            msg = get_messages(client)

            if msg == False:  # không nhận được tin nhắn
                return -1

            if msg == QUIT:  # thoát
                return QUIT

            temp = msg.split()

            if len(temp) != 3:
                send_messages(client, error)
                continue

            cmd, username, password = temp

            if cmd != LOGIN:
                send_messages(client, error)
                continue

            if username in client_online:  # tài khoản đang được sử dụng
                send_messages(client, account_used)
                continue

            if username not in client_info:  # tài khoản không tồn tại
                send_messages(client, username_error)
                continue

            if password != client_info[username]:  # sai mật khẩu
                send_messages(client, password_error)
                continue

            return User(username, password)

    except Exception as e:
        print("[EXCEPTION in LOGIN]", e)
        return -1


def All_list_append(name):
    """
    => Thêm tên người dùng mới vào list của những người dùng khác
    param name: tên người dùng được thêm
    return: None
    """

    for username in client_online:
        recv_conn, recv_addr = client_online[username]
        send_messages(recv_conn, f"!ADD {name}")


def client_register(client):
    """
    => Trang ĐĂNG KÝ TÀI KHOẢN
    param client: client của người dùng
    return: trả về OK nếu không vấn đề
                   QUIT nếu thoát
                   -1 nếu sinh lỗi
    """

    send_messages(client, "REGISTER PAGE")

    username, password = None, None

    # Đăng ký tài khoản
    try:
        while True:
            send_messages(client, username_instruction)

            msg = get_messages(client)

            if msg == False:  # không nhận được tin nhắn
                return -1

            if msg == QUIT:  # thoát
                return QUIT

            temp = msg.split()

            if len(temp) != 2:
                send_messages(client, error)
                continue

            cmd, name = temp

            if cmd != USERNAME:
                send_messages(client, error)
                continue

            if db.exist(name) == True:  # nếu username đã tồn tại
                send_messages(client, username_exist)
                continue

            username = name
            break
    except Exception as e:
        print("[EXCEPTION in USERNAME]", e)
        return -1

    send_messages(client, CLEAR)
    send_messages(client, f"Your username is {username}")

    # Đăng ký mật khẩu
    try:
        while True:
            send_messages(client, password_instruction)

            msg = get_messages(client)

            if msg == False:  # không nhận được tin nhắn
                return -1

            if msg == QUIT:  # thoát
                return QUIT

            temp = msg.split()

            if len(temp) != 3:
                send_messages(client, error)
                continue

            cmd, pwd, confirm = temp

            if cmd != PASSWORD:
                send_messages(client, error)
                continue

            if pwd != confirm:  # nếu mật khẩu khác mật khẩu nhập lại
                send_messages(client, wrong_confirmation)
                continue

            password = pwd
            break
    except Exception as e:
        print("[EXCEPTION in PASSWORD]", e)
        return -1

    # Đăng ký thành công

    user = User(username, password)  # tạo một User mới
    # db.insert(user)  # lưu trữ vào database
    # client_info[username] = password  # Lưu trữ vào chương trình

    # Tạo khung lưu trữ mới
    newpath = store.mainpath + username + ".db"
    store.path = newpath
    store.create_table()

    print(
        "[ANNOUNCEMENT] New user has been added"
    )  # Thông báo tài khoản mới đc đăng ký
    print("=> ", user.username, user.password)

    try:
        while True:
            send_messages(client, AVATAR)

            msg = get_messages(client)

            if msg == False: # không nhận được tin nhắn
                return -1

            if msg == QUIT:
                return QUIT # Thoát

            if msg == "Yes":
                path = __file__[:-9] + "\\avatar\\" + user.username + ".png"

                with open(path, "wb") as file:
                    while True:
                        image_chunk = client.recv(2048)
                        # print(image_chunk) // test
                        if image_chunk == bytes("ENDofFILE", "utf8"):
                            break
                        file.write(image_chunk)
                # print("end of process") // test
                break

            elif msg == "No":
                default_img = __file__[:-9] + "\\default.jpg"
                dir_path = __file__[:-9] + "\\avatar\\" + user.username + ".png"
                copyfile(default_img, dir_path)
                break
            
            else:
                send_messages(client, error)
    except Exception as e:
        print("[EXCEPTION]", e)
        return -1

    return OK


def List(client):
    """
    => Gửi danh sách những tài khoản đã đăng ký
    param client: client của người dùng
    return: None
    """

    client_list = db.getall()

    msg = "!list"
    for user in client_list:
        if user not in client_online:
            msg = msg + " " + str(user[0])
    send_messages(client, msg)


def Online_list(client):
    """
    => Gửi danh sách những người đang online
    param client: client của người dùng
    return: None
    """

    msg = "!online_list"
    for username in client_online:
        msg = msg + " " + str(username)
    send_messages(client, msg)


def Help(client):
    """
    => Gửi danh sách câu lệnh được sử dụng với SERVER
    param client: client của người dùng
    return: None
    """

    msg = """
        "/quit":                  Quit to menu
        "/logout"                 Logout
        "/list"                   List all accounts
        "/online_list"            List all online accounts
        "/group_list"             List all group
        "/tp + <name>"            Move to chat room with <name>
        "/help"                   List all command
        "/join + <name>"          Join a group
        "/party_create + <name>"  Create a new group and you are the host    
    """
    send_messages(client, msg)


def Group_list(client):
    """
    => Gửi danh sách những nhóm đã tạo
    param client: client của người dùng
    return: None
    """

    msg = ""
    if len(group) <= 1:
        msg = f"There is {len(group)} group\n"
    else:
        msg = f"There are {len(group)} groups\n"
    for group_name in group:
        msg = msg + "\t\t" + str(group_name) + "\n"
    send_messages(client, msg)


def New_Group(client, name, username):
    """
    => Tạo một nhóm mới với tên là name và người tạo là ADMIN
    param name: tên nhóm
    param username: tên người tạo
    param client: client của người tạo
    return: None
    """

    send_messages(client, group_ok + f"== {name} ==")
    group[name] = [(username, ADMIN)]

    first_msg = f"[FIRST MESSAGE] {username} has created the group\n"

    # Tạo phần chat mới
    groupchat.path = groupchat.mainpath + name + "_chat" + ".db"
    groupchat.create_table()
    groupchat.update_chat(first_msg)

    # Thêm thành viên là người tạo
    groupmem.path = groupmem.mainpath + name + "_mem" + ".db"
    groupmem.create_table()
    groupmem.insert(username, CREATOR)

    # Thêm nhóm vào danh sách
    groupname.create_table()
    groupname.insert(name)


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
    send_messages(client, welcome)

    # Mở tất cả đoạn chat
    newpath = store.mainpath + name + ".db"
    store.path = newpath

    text = store.show(receiver)

    if text == -1:  # Chưa tồn tại đoạn chat giữa hai người
        text = ""
        store.update_chat(receiver, "")

        newpath = store.mainpath + receiver + ".db"
        store.path = newpath
        store.update_chat(name, "")

    newpath = store.mainpath + name + ".db"
    store.path = newpath
    text = "?" + text
    send_messages(client, text)

    # Phần chat của người dùng
    while True:
        msg = get_messages(client)

        if msg == False:
            return -1

        if msg == QUIT:
            return QUIT

        if receiver in client_online and client_location[receiver] == name:
            recv_conn, recv_addr = client_online[receiver]
            send_messages(recv_conn, f"?[{name}] {msg}")

        # lưu trữ message của bản thân
        newpath = store.mainpath + name + ".db"
        store.path = newpath
        store.update_chat(receiver, f"?[You] {msg}\n")

        # Lưu trữ message của đối tượng chat
        newpath = store.mainpath + receiver + ".db"
        store.path = newpath
        store.update_chat(name, f"?[{name}] {msg}\n")


def is_in_group(username, name):
    """
    => Kiểm tra nếu username ở trong nhóm tên name
    param username: tên người dùng
    param name: tên nhóm
    return: True (nếu username đã tồn tại trong nhóm)
          : No (nếu username chưa tồn tại trong nhóm)
    """

    for member in group[name]:
        if member[0] == username:
            return True

    return False


def role(username, name):
    """
    => Xem xét chức danh của người dùng là gì
    param username: tên người dùng
    param name: tên nhóm
    return: "MEMBER" (thành viên)
          : "ADMIN" (quản trị viên)
    """

    for member in group[name]:
        if member[0] == username:
            return member[1]

    return -1


def group_chat(client, username, name):
    """
    => Chat nhóm
    param client: client của người dùng
    param username: tên người dùng
    param name: tên nhóm
    return: None
    """

    # welcome = f"""
    #             {"=" * 40}
    #             {f"Yourname = {name};".center(40)}
    #             {f"Group = {name}".center(40)}
    #             {"=" * 40}\n"""
    # send_messages(client, CLEAR)
    # send_messages(client, welcome)

    # Mở đoạn chat
    groupchat.path = groupchat.mainpath + name + "_chat" + ".db"
    message = groupchat.show()
    message = "?" + message
    # for member in group[name]:
    #     if member[0] in client_online and client_location[member[0]] == AT_GROUP + name:
    #         recv_conn, recv_addr = client_online[member[0]]
    #         send_messages(recv_conn, message)
    send_messages(client, message)

    # Phần chat của người dùng
    while True:
        msg = get_messages(client)

        if msg == False:  # Không nhận được tin nhắn
            return -1

        if msg == QUIT:
            return QUIT

        temp = msg.split()
        msg = f"[{username}] {msg}\n"
        changed = False

        if len(temp) == 2 and temp[0][0] == "/":
            cmd, invited_member = temp
            if cmd != PARTY_INVITE:
                send_messages(client, ERROR)
                continue

            if invited_member not in client_info:  # Không tồn tại người dùng
                send_messages(client, ERROR)
                continue

            if role(username, name) == MEMBER:  # Member không được thêm thành viên
                send_messages(client, ERROR)
                continue

            if is_in_group(
                invited_member, name
            ):  # Nếu thành viên đã tồn tại trong nhóm
                send_messages(client, ERROR)
                continue

            # Lưu trữ thành viên
            groupmem.path = groupmem.mainpath + name + "_mem" + ".db"
            groupmem.insert(invited_member)

            # Thông báo thành viên mới
            msg = f"[ANNOUNCEMENT] {name} has added {invited_member} to group\n"
            changed = True
            group[name].append((invited_member, MEMBER))

        # Gửi trực tiếp đến những người đang online
        for member in group[name]:
            if member[0] == username and changed == False:
                continue
            if (
                member[0] in client_online
                and client_location[member[0]] == AT_GROUP + name
            ):
                recv_conn, recv_addr = client_online[member[0]]
                send_messages(recv_conn, "!" + msg)

        # Lưu trữ vào đoạn chat chung
        groupchat.path = groupchat.mainpath + name + "_chat" + ".db"
        groupchat.update_chat(msg)


def Online_list_display(client, name):
    """
    => Gửi tin nhắn để hiện thị những người đang online
    param client: client của người dùng
    param name: tên của người dùng
    return: None
    """

    for username in client_online:
        send_messages(client, f"!CONNECT {username}")


def List_display(client, name):
    """
    => Gửi tin nhắn để hiện thị những tài khoản đang hiện hữu
    param client: client của người dùng
    param name: tên của người dùng
    return: None
    """

    for username in client_info:
        send_messages(client, f"!ADD {username}")


def All_online_list_append(name):
    """s
    => Thêm name vào online_list của những người dùng khác
    param name: tên người dùng được thêm vào
    return: None
    """

    for username in client_online:
        recv_conn, recv_addr = client_online[username]
        send_messages(recv_conn, f"!CONNECT {name}")


def All_online_list_discard(name):
    """
    => Xóa name ra khỏi online_list của những người dùng khác
    param name: tên người dùng bị xóa đi
    return: None
    """

    for username in client_online:
        recv_conn, recv_addr = client_online[username]
        send_messages(recv_conn, f"!DISCONNECT {name}")


def Which_group_are_you_in(client, name):
    """
    => Gửi tin nhắn những nhóm name thuộc về
    param client: client của người dùng
    param name: tên người dùng
    return: None
    """

    for group_name in group:
        for member in group[group_name]:
            if name == member[0]:
                send_messages(client, f"!GROUP {group_name}")


def client_and_server(client, addr):
    """
    => Giao tiếp giữa SERVER và người dùng
    param client: client của người dùng
    param addr  : địa chỉ của người dùng
    return: None
    """

    welcome_msg = "Welcome back to VLC chat room!!!\n"
    welcome_msg = welcome_msg + "\tUse '/login' to login or '/register' to register\n"
    send_messages(client, welcome_msg)

    user = None
    disconnect_msg = f"[DISCONNECTION] {addr} has disconnected"

    # Đăng nhập hoặc Đăng ký tài khoản
    while True:
        msg = get_messages(client)

        if msg == False:  # không nhận được tin nhắn
            print(disconnect_msg)  # thông báo đường truyền bị ngắt
            return

        if msg == REGISTER:  # Phần ĐĂNG KÝ
            send_messages(client, CLEAR)

            command = client_register(client)  # vào hàm ĐĂNG KÝ

            if command == -1:  # sinh lỗi
                print(disconnect_msg)  # thông báo đường truyền bị ngắt
                return

            if command == QUIT:  # thoát
                send_messages(client, CLEAR)
                client_and_server(client, addr)
                return

            send_messages(client, CLEAR)
            send_messages(
                client, "Please login again!!!\n"
            )  # Đăng nhập lại sau khi Đăng ký

            client_and_server(client, addr)
            return

        elif msg == LOGIN:  # Phần ĐĂNG NHẬP
            send_messages(client, CLEAR)

            temp_user = client_login(client)  # vào hàm ĐĂNG NHẬP

            if temp_user == QUIT:  # thoát
                send_messages(client, CLEAR)
                client_and_server(client, addr)
                return

            if temp_user == -1:  # sinh lỗi
                print(disconnect_msg)  # thông báo đường truyền bị ngắt
                return

            user = temp_user
            break

        else:
            try:
                send_messages(client, error)
                send_messages(
                    client, "Use '/login' to login or '/register' to register"
                )
            except Exception as e:
                print("[EXCEPTION in CONNECTION]", e)
                return -1

    # Truy cập tài khoản thành công
    send_messages(client, CLEAR)
    send_messages(client, "Correct password.")
    send_messages(client, CLEAR)
    send_messages(client, CODE_NAME + user.username)  # Gửi đi tên tài khoản
    welcomeback_msg = f"""
                ==============================================
                \t\tWelcome back {user.username}
                =============================================="""
    send_messages(client, welcomeback_msg)


    Which_group_are_you_in(client, user.username)
    Online_list_display(client, user.username)
    List_display(client, user.username)

    client_online[user.username] = (client, addr)
    client_location[user.username] = AT_SERVER
    
    All_online_list_append(user.username)

    # Truy cập chat
    while True:
        msg = get_messages(client)

        if msg == False:
            print(disconnect_msg + f" with name = {user.username}")

            All_online_list_discard(user.username)

            try:
                client_online.pop(user.username)
            except Exception as e:
                print("[EXCEPTION in DISCONNECTION] Failed to disconnect")
            return

        if msg == LOGOUT:  # đăng xuất
            print(f"[LOGOUT] {user.username} has logged out")
            
            All_online_list_discard(user.username)

            send_messages(client, CLEAR)
            send_messages(client, "You have been logged out")
            send_messages(client, CLEAR)
            send_messages(client, CODE_NAME + "You")
            try:
                client_online.pop(user.username)
            except Exception as e:
                print("[EXCEPTION in DISCONNECTION] Failed to disconnect")
            client_and_server(client, addr)
            return

        if msg == LIST:  # liệt kê danh sách tài khoản
            List(client)
            continue

        if msg == ONLINE_LIST:  # liệt kê danh sách online
            Online_list(client)
            continue

        if msg == HELP:  # liệt kê danh sách lệnh hỗ trợ
            Help(client)
            continue

        if msg == GROUP_LIST:
            Group_list(client)
            continue

        temp = msg.split()

        if len(temp) == 2:
            cmd, receiver = temp

            if cmd == MOVE:  # kiểm tra lệnh MOVE
                if receiver == user.username:
                    send_messages(client, "This is your account.")
                    continue

                if (
                    receiver not in client_info
                ):  # nếu tên tài khoản không nằm trong danh sách
                    send_messages(client, username_not_exist)
                    continue

                # Chọn thành công đối tượng chat
                client_location[user.username] = receiver
                command = client_chat(client, user.username, receiver)

                if (
                    command == -1
                ):  # chạy sinh lỗi hoặc chương trình client bị tắt đột ngột
                    print(disconnect_msg + f" with name = {user.username}")

                    All_online_list_discard(user.username)

                    try:
                        client_online.pop(user.username)
                    except Exception as e:
                        print("[EXCEPTION in DISCONNECTION] Failed to disconnect")
                    return

                if (
                    command == QUIT
                ):  # Trở lại menu chính hay nói cách khác là chạy lại vòng lặp
                    client_location[user.username] = AT_SERVER
                    send_messages(client, CLEAR)
                    send_messages(client, welcomeback_msg)
                    continue

            elif cmd == PARTY_CREATE:
                group_name = receiver
                if group_name in group:
                    send_messages(client, group_exist)
                    continue
                New_Group(client, group_name, user.username)
                continue

            elif cmd == JOIN:
                group_name = receiver

                if group_name not in group:
                    send_messages(client, group_not_exist)
                    continue

                if (
                    is_in_group(user.username, group_name) == False
                ):  # Nếu thành viên không ở trong nhóm
                    send_messages(client, not_member)
                    continue

                client_location[user.username] = AT_GROUP + group_name
                command = group_chat(client, user.username, group_name)

                if (
                    command == -1
                ):  # chạy sinh lỗi hoặc chương trình client bị tắt đột ngột
                    print(disconnect_msg + f" with name = {user.username}")

                    All_online_list_discard(user.username)

                    try:
                        client_online.pop(user.username)
                    except Exception as e:
                        print("[EXCEPTION in DISCONNECTION] Failed to disconnect")
                    return

                if (
                    command == QUIT
                ):  # Trở lại menu chính hay nói cách khác là chạy lại vòng lặp
                    client_location[user.username] = AT_SERVER
                    send_messages(client, CLEAR)
                    send_messages(client, welcomeback_msg)
                    continue

            else:
                send_messages(client, error)
                continue

        send_messages(client, error)


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
    => Lấy thông tin tài khoản mật khẩu của người dùng và tên các nhóm
    :return: None
    """

    global client_info, group

    client_info = dict(db.getall())
    client_info["SERVER"] = "NoNeedToAsk"
    client_info["You"] = "Init###"

    names = groupname.show()
    for name in names:
        groupmem.path = groupmem.mainpath + name[0] + "_mem" + ".db"
        group[name[0]] = groupmem.show()


def info_display():
    print("CLIENT INFO:")
    for acc in client_info:
        s = f"\t* username: {acc}; password: {client_info[acc]}"
        print(s)

    print("GROUP INFO:")
    for name in group:
        print(f"\t* {name}:")
        for member in group[name]:
            print(f"\t\t- {member[0]} -> {member[1]}")


if __name__ == "__main__":
    get_info()
    info_display()

    # open server with some connections
    print("[LISTENING] Server is starting...")
    SERVER.listen(MAX_CONNECTION)

    # start the server
    server_thread = Thread(target=connection)
    server_thread.start()
    server_thread.join()
    SERVER.close()
