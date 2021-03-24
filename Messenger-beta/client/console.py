import tkinter as tk
from tkinter import ttk
from threading import Thread
import time

font = "Arial 10"

class ChatConsole:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Chat room")
        self.root.configure(background="#242526")

        self.textChat = tk.Text(
            self.root,
            width=36,
            height=80,
            highlightbackground="#313236",
            highlightthickness=1,
            background="#313236",
            fg="white",
        )

        self.textChat.tag_configure("right", justify="right")
        self.textChat.tag_configure("left", justify="left")
        self.textChat.tag_configure("bold", font=f"{font} bold")
        self.textChat.tag_configure("text_font", font=f"{font}")

        self.textChat['state'] = tk.DISABLED
        self.textChat.grid(row=0, column=0, columnspan=2)

    def send(self, msg):
        self.textChat['state'] = tk.NORMAL
        self.textChat.insert("end", "You: ", "bold")
        self.textChat.insert("end", msg + '\n', "text_font")
        self.textChat['state'] = tk.DISABLED


class CommandConsole():
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
        self.txtSend.delete(1.0, tk.END)
        if self.txtSend_length == 0 or text == "\n":
            return

        self.txtChat.config(state=tk.NORMAL)
        self.txtChat.insert("end", f"You: ", "bold")
        self.txtChat.insert("end", f"{text}", "text_font")
        self.currentText = text
        if event == None:
            self.txtChat.insert("end", "\n")

        self.TextLenCount()
        self.txtChat.config(state=tk.DISABLED)

    def InsertMessage(self, msg):
        self.txtChat['state'] = tk.NORMAL
        self.txtChat.insert("end", "Command: ", "bold")
        self.txtChat.insert("end", msg + '\n', "text_font")
        self.txtChat['state'] = tk.DISABLED

    def Clear(self):
        self.txtChat['state'] = tk.NORMAL
        self.txtChat.delete("1.0", tk.END)
        self.txtChat['state'] = tk.DISABLED


cmd = CommandConsole()

cmd.InsertMessage("Hello")
cmd.InsertMessage("my friend")
cmd.Clear()

cmd.root.mainloop()