from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
import sys
import os

# import UI


class CommandConsole:

    this_name = "You"

    txtChat_width = 80
    txtChat_height = 36

    txtChat_font = "Arial 10"

    txtSend_font = "Arial 10"
    txtSend_length = 0
    # Khởi tạo UI
    def __init__(self):
        # Text hiển thị trong SendText
        self.currentText = ""

        # Root
        self.root = tk.Tk()
        self.root.title("Messenger")
        self.root.configure(background="#242526")

        # # Khởi tạo frame danh sách bạn bè
        # self.frmFriend = tk.Frame(
        #     self.root,
        #     background="#1b1c1f",
        #     height=625,
        #     width=250,
        #     highlightthickness=2,
        #     highlightbackground="black",
        # )
        # self.frmFriend.grid(row=0, column=0, sticky=tk.N, rowspan=2)

        # # Khởi tạo frame người dùng
        # self.frmUser = tk.Frame(
        #     self.root,
        #     background="gray",
        #     height=40,
        #     width=250,
        #     highlightthickness=2,
        #     highlightbackground="black",
        # )
        # self.frmUser.grid(row=2, column=0, sticky=tk.N)

        # # Khởi tạo frame đói tượng chat hiện tại
        # self.frmCur = tk.Frame(self.root, background="gray", height=40, width=645)
        # self.frmCur.grid(row=0, column=1, sticky=tk.NW, columnspan=2)

        # Khởi tạo chat text box
        self.txtChat = tk.Text(
            self.root,
            width=self.txtChat_width,
            height=self.txtChat_height,
            highlightbackground="#313236",
            highlightthickness=1,
            background="#313236",
            fg="white",
        )
        self.txtChat.grid(columnspan=2, row=1, column=1, sticky=tk.NW)

        self.txtChat.tag_configure("right", justify="right")
        self.txtChat.tag_configure("left", justify="left")
        self.txtChat.tag_configure("bold", font=f"{self.txtChat_font} bold")
        self.txtChat.tag_configure("text_font", font=f"{self.txtChat_font}")
        self.txtChat.config(state=tk.DISABLED)

        # # Khởi tạo button file
        # self.btnFile = ttk.Button(self.root, text="File")
        # self.btnFile.grid(row=1, column=1, ipady=3, pady=(0, 10))

        # Khởi tạo chat input text box
        self.txtSend = tk.Text(
            self.root,
            width=self.txtChat_width,
            height=2,
            font=self.txtSend_font,
            highlightthickness=1,
            highlightcolor="gray",
            highlightbackground="#43454a",
            background="#43454a",
            fg="white",
        )
        self.txtSend.bind("<KeyRelease-Return>", self.SendMessage)
        self.txtSend.bind("<FocusOut>", self.InsertPlaceHolder)
        self.txtSend.bind("<Button-1>", self.DeletePlaceHolder)
        self.txtSend.bind("<KeyRelease>", self.TextLenCount)
        self.txtSend.tag_configure("lightgray", foreground="lightgray")
        self.InsertPlaceHolder()
        self.txtSend.grid(row=2, column=1, sticky=tk.NW)

        # Khởi tạo button send
        self.btnSend = ttk.Button(self.root, text="Send", command=self.SendMessage)
        self.btnSend.grid(row=2, column=2, ipady=3, sticky=tk.NW)

    #     # Mainloop
    #     # self.root.mainloop()

    # Chèn string placeholder khi txtSend không có focus
    def InsertPlaceHolder(self, event=None):
        self.txtChat.focus_set()
        if self.txtSend_length == 0:
            self.txtSend.insert(1.0, "Type text here...", "lightgray")

    # Xóa string placholder khi txtSend không có focus
    def DeletePlaceHolder(self, event):
        if self.txtSend_length == 0:
            self.txtSend.delete(1.0, tk.END)

    # Đếm độ dài xâu hiện có trong txtSend
    def TextLenCount(self, event=None):
        text = self.txtSend.get(1.0, tk.END)
        self.txtSend_length = len(text)
        if self.txtSend.get(1.0, tk.END) == "\n":
            self.txtSend_length -= 1

    # Gửi tin nhắn
    def SendMessage(self, event=None):
        text = self.txtSend.get(1.0, tk.END)
        text = text.strip()
        self.txtSend.delete(1.0, tk.END)
        if self.txtSend_length == 0 or text == "\n":
            return

        send_messages(text)

        if (
            len(text) > len("/party_invite")
            and text[: len("/party_invite")] == "/party_invite"
        ):
            return

        text = text + "\n"

        self.txtChat.config(state=tk.NORMAL)
        self.txtChat.insert("end", f"[{self.this_name}]: ", "bold")
        self.txtChat.insert("end", f"{text}", "text_font")

        if event == None:
            self.txtChat.insert("end", "\n")

        self.TextLenCount()
        self.txtChat.config(state=tk.DISABLED)

    def Display(self, sender, msg):
        self.txtChat["state"] = tk.NORMAL
        self.txtChat.insert("end", sender, "bold")
        self.txtChat.insert("end", msg + "\n", "text_font")
        self.txtChat["state"] = tk.DISABLED

    def InsertMessage(self, msg, type, name=None):
        # type = 1: gửi SERVER
        # type = 2: gửi có người nhắn
        # type = 3: chuỗi tin nhắn được in ra

        if type == 3:
            messages = msg.split("\n")
            for message in messages:
                op = 0
                ed = message.find("]")
                sender = message[op : ed + 1]
                message = message[ed + 2 :]
                self.Display(sender, message)
            return

        sender = "[SERVER] " if type == 1 else f"{name} "

        self.Display(sender, msg)

    def Clear(self):
        self.txtChat["state"] = tk.NORMAL
        self.txtChat.delete(1.0, tk.END)
        self.txtChat["state"] = tk.DISABLED


HOST = "localhost"
PORT = 5050
ADDR = (HOST, PORT)
BUFSIZ = 512


client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)
lock = Lock()


class Client:
    # COMMAND
    CLEAR = "/clear"
    CONSOLE = "/console"

    # MARK
    ERROR = "ERROR"
    CODE_NAME = "#NAME#"

    # SERVER'S COMMAND
    password_instruction = (
        "Insert and confirm password with [/pwd <password> <password>]"
    )

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

    # cmdConsole = CommandConsole()

    def __init__(self):
        # receive_thread = Thread(target=self.receive_messages)
        # receive_thread.start()
        update_thread = Thread(target=self.update_messages, daemon=True)
        update_thread.start()

    # Changed
    def receive_messages(self):
        """
        => receive messages from server
        :return: None
        """

        try:
            msg = client_socket.recv(BUFSIZ).decode()
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
        run = True
        while run:

            if self.close == True:
                return

            time.sleep(0.1)  # update every 1/10 of a second
            new_messages = self.get_messages()  # get any new messages from client
            msgs.extend(new_messages)  # add to local list of messages

            for msg in new_messages:  # display new messages
                # print(msg)

                if self.close == True:
                    return

                self.UI_messages.append(msg)

                if msg == self.ERROR:
                    messagebox.showwarning(title="Warning", message=self.ERROR)
                    continue

                if len(msg) > 6 and msg[:6] == self.CODE_NAME:
                    self.this_name = msg[6:]
                    print(self.this_name)
                    # self.cmdConsole.this_name = self.this_name
                    continue

                type = 1

                if msg[0] == "!":  # type with name
                    type = 2

                elif msg[0] == "?":  # type with no name
                    type = 3

                if msg != self.CLEAR:
                    if type == 2:
                        msg = msg[1:]
                        name = msg.split()[0]
                        msg = msg[len(name) + 1 :] + "\n"
                        # self.cmdConsole.InsertMessage(msg, 2, name)

                    elif type == 3:
                        msg = msg[1:]
                        # self.cmdConsole.InsertMessage(msg, 3)

                if msg == "Correct password.":
                    self.logged_in = True
                    self.stop = True
                    time.sleep(1.5)

                elif msg == "You have been logged out":
                    self.logged_in = False
                    self.stop = True
                    time.sleep(1.5)

                elif msg == "{quit}":
                    run = False
                    break

                elif msg == self.CONSOLE:
                    self.console = True

                elif msg == self.password_instruction:
                    self.pwd_confirm = True

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.close = True
            client_socket.close()
            # self.cmdConsole.root.destroy()

    # def start(self):

    # self.cmdConsole.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    # self.cmdConsole.root.mainloop()


# start()
