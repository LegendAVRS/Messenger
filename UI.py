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
    lbl_font = "Arial 10 bold"

    def __init__(self, username, row, client, ui):
        self.client = client
        self.username = username
        self.ui = ui

        ui.frmFriend.grid_columnconfigure(0, weight=1)
        self.Frame = tk.Frame(
            ui.frmFriend, bg=ui.frmFriend["bg"], height=30, cursor="hand2"
        )
        self.lblUsername = tk.Label(
            self.Frame,
            text=username,
            bg=ui.frmFriend["bg"],
            fg="white",
            font=self.lbl_font,
        )

        self.Frame.bind("<Button-1>", self.SwitchFriend)
        self.Frame.bind("<Enter>", self.FrameEnter)
        self.Frame.bind("<Leave>", self.FrameLeave)

        self.Frame.grid_propagate(0)

        self.lblUsername.grid(row=0, column=0)
        self.Frame.grid(row=row, column=0, sticky="NSEW", pady=5)

    def SwitchFriend(self, event):
        # self.ui.txtChat.config(state=tk.NORMAL)
        # self.ui.txtChat.delete(1.0, tk.END)
        self.client.send_messages("/quit")
        self.client.send_messages(f"/tp {self.username}")

        for widget in self.ui.frmCur.winfo_children():
            widget.destroy()
        lblCur = tk.Label(
            self.ui.frmCur,
            text=self.username,
            fg="white",
            bg=self.ui.frmCur["bg"],
            font=("Arial", 12, "bold"),
        )

        lblCur.grid(row=0, column=0)
        self.ui.chat_row = 0

        for widget in self.ui.frmChat.scrollable_frame.winfo_children():
            widget.destroy()

        self.frmChat.canvas.yview_moveto("1.0")

    def FrameEnter(self, event):
        self.Frame["bg"] = "#232529"
        self.lblUsername["bg"] = "#232529"

    def FrameLeave(self, event):
        self.Frame["bg"] = self.ui.frmFriend["bg"]
        self.lblUsername["bg"] = self.ui.frmFriend["bg"]


class Message(tk.Frame):
    row = 0

    def __init__(self, root, text, ui, username, color):
        self.ui = ui
        super().__init__(
            root.scrollable_frame,
            bg=ui.frmChat["bg"],
            # bg="black",
            width=root.winfo_width(),
            height=(len(text) * 5 / ui.frmChat.winfo_width() + 2) * 20,
        )
        self.bind("<Enter>", self.FrameEnter)
        self.bind("<Leave>", self.FrameLeave)

        self.grid(row=ui.chat_row, column=0, sticky="NSWE", pady=(0, 8))
        ui.chat_row += 1

        self.grid_propagate(0)
        self.update()

        self.txtName = tk.Text(
            self,
            bg=ui.frmChat["bg"],
            fg=color,
            font=("Arial", 11, "bold"),
            borderwidth=0,
            width=len(username) + 1,
            height=1,
        )
        self.txtName.insert(tk.END, username)
        self.txtName.grid(row=0, column=0, sticky="W")
        self.txtName.config(state=tk.DISABLED)

        self.txtText = tk.Text(
            self,
            bg=ui.frmChat["bg"],
            fg="white",
            font=("Arial", 11),
            borderwidth=0,
            width=len(text),
        )

        self.txtText.insert(tk.END, text)
        self.txtText.grid(row=1, column=0, sticky="W")
        self.txtText.config(state=tk.DISABLED)

        Message.row += 1

    def FrameEnter(self, event):
        color = "#414247"
        self["bg"] = color
        self.txtText["bg"] = color
        self.txtName["bg"] = color

    def FrameLeave(self, event):
        color = self.ui.frmChat["bg"]
        self["bg"] = color
        self.txtText["bg"] = color
        self.txtName["bg"] = color


class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self, *args, **kwargs, highlightthickness=0)

        scrollbar = tk.Scrollbar(
            self, orient="vertical", command=self.canvas.yview, width=12
        )
        self.canvas.bind("<Enter>", self.BindWheel)
        self.canvas.bind("<Leave>", self.UnbindWheel)

        self.scrollable_frame = tk.Frame(self.canvas, *args, **kwargs)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        # canvas.pack(side="left", fill="both", expand=True)
        # scrollbar.pack(side="right", fill="y")
        # self.grid_rowconfigure(0, weight=1)
        self.canvas.grid(row=0, column=0, sticky="NSWE")
        scrollbar.grid(row=0, column=1, sticky="NSEW")

    def OnMouseWheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def BindWheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self.OnMouseWheel)

    def UnbindWheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")


# Class cho UI chương trình chính
class UI:
    friend_list = []
    row_index = 1
    cur_friend = ""

    txtChat_width = 80
    txtChat_height = 36
    chat_row = 0

    txtChat_font = ("Comic Sans MS", 10)

    txtSend_font = "Arial 10"
    txtSend_length = 0

    lblFrm_font = "Arial 12 bold"

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
        self.lblFrame = tk.Label(
            self.frmFriend,
            bg=self.frmFriend["bg"],
            fg="white",
            text="------ User list ------",
            font=self.lblFrm_font,
        )
        self.lblFrame.grid(row=0, column=0)
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
        self.frmCur = tk.Frame(self.root, background="gray", height=40, width=100)
        self.frmCur.grid_propagate(0)
        self.root.grid_columnconfigure(1, weight=1)
        self.frmCur.grid(row=0, column=1, sticky="NSEW", columnspan=2)

        # Khởi tạo chat frame
        self.frmChat = ScrollableFrame(self.root, height=600, bg="#313236")
        self.frmChat.grid_columnconfigure(self.chat_row, weight=1)
        self.frmChat.grid_propagate(0)

        self.root.grid_rowconfigure(1, weight=1)
        self.frmChat.grid(columnspan=2, row=1, column=1, sticky="NSEW")

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
        self.root.update()
        self.root.mainloop()

    # Chèn string placholder khi txtSend không có focus
    def InsertPlaceHolder(self, event=None):
        # self.txtChat.focus_set()
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
        # new_msg = Message(self.frmChat, text, self)
        # new_msg.grid(row=self.chat_row, column=0, sticky="EWNS")
        Message(self.frmChat, text, self, "AdamAV", "white")
        # self.chat_row += 1

        # self.txtChat.config(state=tk.NORMAL)
        # self.txtChat.insert("end", f"[You] ", "chat_font_bold")
        # self.txtChat.insert("end", f"{text}\n")
        # if event == None:
        #     self.txtChat.insert("end", "\n")

        self.client.send_messages(text)
        self.TextLenCount()

        self.frmChat.canvas.yview_moveto("1.0")
        # self.txtChat.config(state=tk.DISABLED)

    def GetMessage(self):
        while self.run:
            # self.txtChat.config(state=tk.DISABLED)
            msg = self.client.receive_messages()
            # self.txtChat.config(state=tk.NORMAL)
            msg_split = msg.split(" ")
            if msg_split[0] == "!list":
                self.friend_list = msg_split[1:]
            else:
                line_list = msg.split("\n")
                for line in line_list:
                    text = line.split(" ")
                    # self.frmChat.insert(tk.END, text[0] + " ", "chat_font_bold")
                    # self.frmChat.insert(tk.END, " ".join(text[1:]) + "\n")
                    if text[0][1:-1] == "You":
                        Message(
                            self.frmChat,
                            " ".join(text[1:]),
                            self,
                            text[0][1:-1],
                            "white",
                        ).grid(row=self.chat_row, column=0)
                    else:
                        Message(
                            self.frmChat,
                            " ".join(text[1:]),
                            self,
                            text[0][1:-1],
                            "green",
                        ).grid(row=self.chat_row, column=0)

                    self.chat_row += 1
            self.frmChat.canvas.yview_moveto("1.0")

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
