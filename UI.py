import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from threading import Thread
from PIL import ImageTk, Image, ImageDraw, ImageOps
import time
from Widget import *

# UI chương trình chính
class UI:
    friend_list = []
    online_friend_list = []
    row_index_friend = 0

    row_index_group = 0

    txtChat_width = 80
    txtChat_height = 36
    chat_row = 0

    txtChat_font = ("Comic Sans MS", 10)

    lblFrm_font = "Arial 12 bold"

    msg_loaded = True
    run = True
    chat_cleared = True
    # client = "123"

    def __init__(self, client):
        self.client = client

        # Root
        self.root = tk.Tk()
        self.root.title("Messenger")
        self.root.configure(background="blue")
        self.root.protocol("WM_DELETE_WINDOW", self.OnClose)

        # Khởi tạo frame danh sách bạn bè
        self.frmList = tk.Frame(
            self.root,
            background="#2f3136",
            width=200,
            height=600,
            highlightbackground="black",
        )

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Khởi tạo frame chứa frmFriend và frmGroup
        self.frmList.grid_propagate(0)
        self.frmList.grid(row=0, column=0, rowspan=2, sticky="NSEW")

        self.lblFrameFriend = tk.Label(
            self.frmList,
            bg=self.frmList["bg"],
            fg="white",
            text="----- Friend list -----",
            font=self.lblFrm_font,
        )
        self.lblFrameFriend.grid(row=0, column=0, sticky="N", padx=(0, 30))

        # Khởi tạo frame chứa danh sách bạn bè
        self.frmFriend = ScrollableFrame(
            self.frmList,
            bg=self.frmList["bg"],
            width=220,
            height=300,
            highlightbackground="black",
        )
        self.frmFriend.grid(row=1, column=0, sticky="NSEW")

        self.lblFrameGroup = tk.Label(
            self.frmList,
            bg=self.frmList["bg"],
            fg="white",
            text="----- Group list -----",
            font=self.lblFrm_font,
        )
        self.lblFrameGroup.grid(row=2, column=0, sticky="N", padx=(0, 30))

        # Khởi tạo frame chứa danh sách nhóm
        self.frmGroup = ScrollableFrame(
            self.frmList,
            bg=self.frmList["bg"],
            width=200,
            height=300,
            highlightbackground="black",
        )
        self.frmGroup.grid_propagate(0)
        self.frmGroup.grid(row=3, column=0, sticky="NSEW")

        # Khởi tạo frame chứa thông tin người dùng
        self.frmUser = tk.Frame(
            self.root,
            bg="#292b2f",
            highlightthickness=0,
            highlightbackground="black",
        )
        self.root.grid_rowconfigure(2, weight=1)
        self.frmUser.grid_propagate(0)
        self.frmUser.grid(row=2, column=0, sticky="NSEW")

        # Khởi tạo frame đói tượng chat hiện tại
        self.frmCur = tk.Frame(self.root, bg=self.frmUser["bg"], height=40, width=50)
        self.frmCur.grid_propagate(0)
        self.root.grid_columnconfigure(1, weight=1)
        self.frmCur.grid(row=0, column=1, sticky="NSEW")

        # Khởi tạo frame khung chat
        self.frmChat = ScrollableFrame(self.root, height=600, bg="#36393f")
        self.frmChat.grid_columnconfigure(self.chat_row, weight=1)
        self.frmChat.grid_propagate(0)

        self.root.grid_rowconfigure(1, weight=1)
        self.frmChat.grid(row=1, column=1, sticky="NSEW")

        # Khởi tạo chat input text box
        self.txtSend = PH_Text(
            root=self.root,
            height=2,
            highlightthickness=1,
            highlightcolor="gray",
            highlightbackground="#43454a",
            background="#40444b",
            fg="white",
        )
        self.txtSend.bind("<KeyRelease-Return>", self.SendMessage)
        self.root.grid_rowconfigure(2, weight=1)
        self.txtSend.grid(row=2, column=1, sticky="NSEW")

        Thread(target=self.GetMessage, daemon=True).start()
        Thread(target=self.SetFriend, daemon=True).start()
        Thread(target=self.SetUser, daemon=True).start()
        # for i in range(10):
        #     self.AddFriend(f"Friend {i}", "white")
        # self.SetUser()

        self.root.update()
        self.root.mainloop()

    # Gửi tin nhắn
    def SendMessage(self, event=None):
        text = self.txtSend.get_string()
        self.txtSend.delete(1.0, tk.END)
        if text == "\n":
            return
        text = text.replace("\n", "")
        Message(self.frmChat, text, self, "You", "white")
        self.client.send_messages(text)

        self.frmChat.canvas.yview_moveto("1.0")

    # Nhận tin nhắn từ server
    def GetMessage(self):
        while self.run:
            msg = self.client.receive_messages()

            # Kiểm tra đã xóa đoạn chat cũ chưa
            while self.chat_cleared == False:
                continue

            print(msg)
            split_msg = msg.split(" ")
            if split_msg[0] == "!list":
                if len(split_msg) != 0:
                    self.friend_list = split_msg[1:]

            elif split_msg[0] == "!online_list":
                if len(split_msg) != 0:
                    self.online_friend_list = split_msg[1:]

            elif msg[0] == "?":
                msg_temp = msg[1:]
                msg_list = msg_temp.split("\n")
                for message in msg_list:
                    message_split = message.split(" ")
                    if len(message_split) > 1:
                        Message(
                            root=self.frmChat,
                            text=" ".join(message_split[1:]),
                            ui=self,
                            username=message_split[0][2:-1],
                            color="white",
                        )
                    self.frmChat.canvas.yview_moveto("1.0")
            self.msg_loaded = True

    # Thiết lập danh sách bạn bè
    def SetFriend(self):
        self.client.send_messages("/online_list")
        time.sleep(0.5)
        self.client.send_messages("/list")
        time.sleep(0.5)
        for friend in self.online_friend_list:
            self.AddFriend(friend, color="green")
        for friend in self.friend_list:
            self.AddFriend(friend, color="white")

    # Thêm bạn vào danh sách bạn bè
    def AddFriend(self, username, color):
        friend = Friend(username, self.row_index_friend, self.client, self, color=color)
        friend.Frame.grid(row=self.row_index_friend, column=0, sticky="NSEW", pady=5)
        self.row_index_friend += 1

    # Thêm nhóm vào danh sách nhóm
    def AddGroup(self, username, color):
        group = Group(username, self.row_index_group, self.client, self, color=color)
        group.Frame.grid(row=self.row_index_group, column=0, sticky="NSEW", pady=5)
        self.row_index_group += 1

    # Thiết lập thông tin người dùng
    def SetUser(self):
        while self.client.this_name == "You":
            continue
        global user
        user = User(text=self.client.this_name, frame=self.frmUser)

    def OnClose(self):
        self.run = False
        # self.SendMessage("/quit")
        self.root.destroy()


if __name__ == "__main__":
    ui = UI()
