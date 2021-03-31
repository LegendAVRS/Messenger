from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import time
import sys
import os
import cv2


def show_img(path):
    img = cv2.imread(path)
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def send_messages(msg):
    """
    => send messages to server
    :param msg: str
    :return: None
    """

    message = msg.encode("utf8")
    client_socket.send(message)

    # if msg == "/logout":
    #     client_socket.close()


HOST = "localhost"
PORT = 5050
ADDR = (HOST, PORT)
BUFSIZ = 512


client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)
lock = Lock()

def msg_box():
    statement = messagebox.askyesno(title="AVATAR??", message="Do you want to set your AVATAR??")
    return statement

def img_selecting():
    filename = filedialog.askopenfilename(initialdir="/", title="Select your AVATAR",
                                    filetypes=(("png files", "*.png"), ("jpeg files", "*.jpeg"), ("jpg files", "*.jpg")))
    return filename

class Client():
    # COMMAND
    CLEAR = "/clear"
    CONSOLE = "/console"

    # MARK
    ERROR = "ERROR"
    CODE_NAME = "#NAME#"
    AVATAR = "AVATAR"

    # SERVER'S COMMAND
    password_instruction = "Insert and confirm password with [/pwd <password> <password>]"

    # Boolean 
    stop = False
    logged_in = False
    console = False
    close = False
    pwd_confirm = False

    # Variables
    messages = []
    UI_messages = []

    this_name = "You"
    can_run = True

    parts = 0

    def __init__(self):
        # Xóa avatar
        path = __file__[:-9] + "\\avatar"
        for f in os.listdir(path):
            os.remove(os.path.join(path, f))

        receive_thread = Thread(target = self.receive_messages)
        receive_thread.start()
        update_thread = Thread(target = self.update_messages)
        update_thread.start()

    def Avatar_Selection(self):
        filename = img_selecting()
        print(filename)

        path = __file__[:-9] + "\\temp\\temp.png"
        temp_img = cv2.imread(filename)
        temp_img = cv2.resize(temp_img, (400, 400)) 
        cv2.imwrite(path, temp_img)
        filename = path

        show_img(filename)
        with open(filename, "rb") as image:
            image_data = image.read(2048)
            while image_data:
                client_socket.send(image_data)
                image_data = image.read(2048)
        time.sleep(1)
        send_messages("ENDofFILE")

    def receive_messages(self):
        """
        => receive messages from server
        :return: None
        """

        if self.close == True:
            return
        try:
            msg = client_socket.recv(BUFSIZ)

            # make sure memory is safe to access
            lock.acquire()
            self.messages.append(msg)
            lock.release()
            return msg
        except Exception as e:
            print("[EXCEPTION in RECEIVE] ", e)
            return


    def send_messages(self, msg):
        """
        => send messages to server
        :param msg: str
        :return: None
        """

        message = msg.encode("utf8")
        client_socket.send(message)
        time.sleep(0.1)

        # if msg == "/logout":
        #     client_socket.close()


    def get_messages(self):
        """
        => returns a list of str messages
        :return: list[str]
        """

        messages_copy = self.messages[:]

        # make sure memory if safe to access
        lock.acquire()
        self.messages = []
        lock.release()

        return messages_copy


    def disconnect(self):
        send_messages("{quit}")


    def update_messages(self):
        """
        => updates the local list of messages
        :return: None
        """

        msgs = []

        # Lấy ảnh
        image_msgs = []
        need_img = False

        initialize = True
        run = True
        while run:


            if self.close == True:
                return

            time.sleep(0.1) # update every 1/10 of a second
            new_messages = self.get_messages() # get any new messages from client
            msgs.extend(new_messages) # add to local list of messages

            for temp_msg in new_messages: # display new messages
                print(temp_msg)
                msg = None
                try:
                    msg = temp_msg.decode()
                except:
                    # print(cnt, "cant decode")

                    if need_img == True:
                        image_msgs.append(temp_msg)
                    continue

                # print(msg)
                if len(msg) > len("#LEN#") and msg[:5] == "#LEN#":
                    self.parts = int(msg[5:])
                    continue

                if msg == "ENDofFILE":
                    initialize = True

                    # Truy xuất ảnh
                    print("Write Ava")
                    path = __file__[:-9] + "\\avatar\\" + self.this_name + ".png"
                    with open(path, "wb") as file:
                        for image_data in image_msgs:
                            file.write(image_data)
                    image_msgs = []
                    need_img = False

                    show_img(path)
                    continue

                if len(msg) > 6 and msg[:6] == self.CODE_NAME:

                    temp_name = msg[6:]

                    # Lấy avatar
                    print("Get ava")
                    if temp_name == "You":
                        path = __file__[:-9] + "\\avatar"
                        for f in os.listdir(path):
                            os.remove(os.path.join(path, f))
                    else:
                        need_img = True

                    # Đổi tên
                    self.this_name = temp_name

                    continue

                if self.close == True:
                    return

                if msg == self.AVATAR:
                    need_avatar = "Yes" if msg_box() else "No"
                    send_messages(need_avatar)

                    if need_avatar == "No":
                        continue

                    self.Avatar_Selection()
                    continue

                self.UI_messages.append(msg)

                if msg == self.ERROR:
                    messagebox.showwarning(title="Warning", message=self.ERROR)
                    continue

                type = 1

                if msg[0] == "!": # type with name
                    type = 2

                elif msg[0] == "?": # type with no name 
                    type = 3

                if msg != self.CLEAR:
                    if type == 1:
                        print("")
                    elif type == 2:
                        msg = msg[1:]
                        name = msg.split()[0]
                        msg = msg[len(name) + 1:] + '\n'
                        

                    elif type == 3:
                        msg = msg[1:]
                        


                if msg == "Correct password.":
                    self.logged_in = True
                    self.stop = True
                    time.sleep(1.5)
                
                elif msg == "You have been logged out":
                    self.logged_in = False
                    self.stop = True
                    time.sleep(1.5)
                
                elif msg == self.CLEAR:
                    print("")
                
                elif msg == "{quit}":
                    run = False
                    break

                elif msg == self.CONSOLE:
                    self.console = True
                
                elif msg == self.password_instruction:
                    self.pwd_confirm = True



    


# start()




