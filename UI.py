import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# import client
from threading import Thread

correct_pass_msg = "[SERVER] Correct password."

"""
    Entry thông thường không có placeholder
    Tạo class entry mới inherit từ ttk.Entry 
    Thiết kế placeholder cho entry này 
"""


class Friend:
    cur_user = None

    def __init__(self, username, row):
        ui.frmFriend.grid_columnconfigure(0, weight=1)
        self.Frame = tk.Frame(ui.frmFriend, bg="grey", height=30)
        self.lblUsername = tk.Label(self.Frame, text=username, bg="grey")

        self.Frame.grid_propagate(0)

        self.lblUsername.grid(row=0, column=0)
        self.Frame.grid(row=row, column=0, sticky="NSEW", pady=5)


# Class cho UI chương trình chính
class UI:
    txtChat_width = 80
    txtChat_height = 36

    txtChat_font = "Arial 10"

    txtSend_font = "Arial 10"
    txtSend_length = 0
    # Khởi tạo UI
    def __init__(self):
        # Root
        self.root = tk.Tk()
        self.root.title("Messenger")
        self.root.configure(background="blue")

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

        self.txtChat.config(state=tk.NORMAL)
        self.txtChat.insert("end", f"You: ", "bold")
        self.txtChat.insert("end", f"{text}", "text_font")
        if event == None:
            self.txtChat.insert("end", "\n")

        self.TextLenCount()
        Friend.cur_user.chat += "\n" + text
        # self.txtChat.config(state=tk.DISABLED)

    def UserAdd(self, username, chat):
        Friend(username, chat)


if __name__ == "__main__":
    ui = UI()
    ui.UserAdd("AVRS", 0)
    ui.UserAdd("Sora", 1)
    ui.UserAdd("Quantical", 2)
    ui.root.mainloop()
