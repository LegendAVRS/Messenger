import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from threading import Thread


"""
    Entry thông thường không có placeholder
    Tạo class entry mới inherit từ ttk.Entry 
    Thiết kế placeholder cho entry này 
"""


class Friend:
    cur_user = None
    cnt = 0

    def __init__(self, username, row, client, ui):
        self.client = client
        self.username = username
        self.ui = ui

        ui.frmFriend.grid_columnconfigure(0, weight=1)
        self.Frame = tk.Frame(
            ui.frmFriend, bg=ui.frmFriend["bg"], height=30, cursor="hand2"
        )
        self.lblUsername = tk.Label(
            self.Frame, text=username, bg=ui.frmFriend["bg"], fg="white"
        )
        self.Frame.bind("<Button-1>", self.SwitchFriend)
        self.Frame.bind("<Enter>", self.FrameEnter)
        self.Frame.bind("<Leave>", self.FrameLeave)

        self.Frame.grid_propagate(0)

        self.lblUsername.grid(row=0, column=0)
        self.Frame.grid(row=row, column=0, sticky="NSEW", pady=5)

    def SwitchFriend(self, event):
        self.ui.txtChat.delete(1.0, tk.END)
        self.client.send_messages("/quit")
        self.client.send_messages(f"/tp {self.username}")

    def FrameEnter(self, event):
        self.Frame["bg"] = "#232529"
        self.lblUsername["bg"] = "#232529"

    def FrameLeave(self, event):
        self.Frame["bg"] = self.ui.frmFriend["bg"]
        self.lblUsername["bg"] = self.ui.frmFriend["bg"]


# Class cho UI chương trình chính
class UI:
    friend_list = []
    row_index = 0

    txtChat_width = 80
    txtChat_height = 36

    txtChat_font = "Arial 10"

    txtSend_font = "Arial 10"
    txtSend_length = 0

    run = True
    # Khởi tạo UI
    def __init__(self, client):
        self.client = client

        # Root
        self.root = tk.Tk()
        self.root.title("Messenger")
        self.root.configure(background="blue")
        self.root.protocol("WM_DELETE_WINDOW", self.OnClose)

        # Khởi tạo frame danh sách bạn bè
        self.frmFriend = tk.Frame(
            self.root,
            background="#1b1c1f",
            width=200,
            highlightthickness=2,
            highlightbackground="black",
        )
        self.frmFriend.grid_propagate(0)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.frmFriend.grid(row=0, column=0, rowspan=2, sticky="NSEW")

        # Khởi tạo frame người dùng

        self.frmUser = tk.Frame(
            self.root,
            background="gray",
            highlightthickness=2,
            highlightbackground="black",
        )
        self.root.grid_rowconfigure(2, weight=1)
        self.frmUser.grid(row=2, column=0, sticky="NSEW")

        # Khởi tạo frame đói tượng chat hiện tại
        self.frmCur = tk.Frame(self.root, background="gray", height=40, width=250)
        self.root.grid_columnconfigure(1, weight=1)
        self.frmCur.grid(row=0, column=1, sticky="NSEW", columnspan=2)

        # Khởi tạo chat text box
        self.txtChat = tk.Text(
            self.root,
            # width=self.txtChat_width,
            height=self.txtChat_height,
            highlightbackground="#313236",
            highlightthickness=1,
            background="#313236",
            fg="white",
        )
        self.root.grid_rowconfigure(1, weight=1)
        self.txtChat.grid(columnspan=2, row=1, column=1, sticky="NSEW")

        self.txtChat.tag_configure("right", justify="right")
        self.txtChat.tag_configure("left", justify="left")
        self.txtChat.tag_configure("bold", font=f"{self.txtChat_font} bold")
        self.txtChat.tag_configure("text_font", font=f"{self.txtChat_font}")

        # Khởi tạo chat input text box
        self.txtSend = tk.Text(
            self.root,
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
        self.root.grid_rowconfigure(2, weight=1)
        self.txtSend.grid(row=2, column=1, sticky="NSEW")

        # Khởi tạo button send
        self.btnSend = ttk.Button(self.root, text="Send", command=self.SendMessage)
        self.root.grid_columnconfigure(2, weight=1)
        self.btnSend.grid(row=2, column=2, ipady=3, sticky="NSEW")

        Thread(target=self.GetMessage).start()
        Thread(target=self.SetFriend).start()
        self.root.mainloop()

    # Chèn string placholder khi txtSend không có focus
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
        self.txtSend.delete(1.0, tk.END)
        if self.txtSend_length == 0 or text == "\n":
            return
        text = text.replace("\n", "")
        # self.txtChat.config(state=tk.NORMAL)
        # self.txtChat.insert("end", f"You: ", "bold")
        # self.txtChat.insert("end", f"{text}", "text_font")
        self.txtChat.insert("end", f"[You] ")
        self.txtChat.insert("end", f"{text}\n")
        # if event == None:
        #     self.txtChat.insert("end", "\n")

        self.client.send_messages(text)
        self.TextLenCount()

        # self.txtChat.config(state=tk.DISABLED)

    def GetMessage(self):
        while self.run:
            msg = self.client.receive_messages()
            msg_split = msg.split(" ")
            if msg_split[0] == "!list":
                self.friend_list = msg_split[1:]
                print(self.friend_list)
            else:
                self.txtChat.insert(tk.END, msg + "\n")

    def SetFriend(self):
        self.client.send_messages("/list")
        while len(self.friend_list) == 0:
            continue
        for friend in self.friend_list:
            self.AddFriend(friend)

    def AddFriend(self, username):
        Friend(username, self.row_index, self.client, self)
        self.row_index += 1

    def OnClose(self):
        self.run = False
        self.SendMessage("/quit")
        self.root.destroy()


if __name__ == "__main__":
    ui = UI()
    ui.root.mainloop()
