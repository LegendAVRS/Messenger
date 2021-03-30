import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image, ImageDraw, ImageOps
from math import ceil
import os

# Entry có placeholder
class PH_Entry(ttk.Entry):
    def __init__(
        self,
        master=None,
        placeholder="PLACEHOLDER",
        color="grey",
        width=28,
        font="Arial 12",
    ):
        super().__init__(master, width=width, font=font)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self["foreground"]

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self["foreground"] = self.placeholder_color

    def foc_in(self, *args):
        print(self["foreground"])
        if self["foreground"] == self.placeholder_color:
            self.delete(0, tk.END)
            self["foreground"] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()

    def get_string(self):
        if self["foreground"] == self.default_fg_color:
            return self.get()
        else:
            return ""


# Text box có placeholder
class PH_Text(tk.Text):
    font = ("Arial", "10")

    def __init__(
        self,
        root,
        height,
        highlightthickness,
        highlightcolor,
        highlightbackground,
        background,
        fg,
    ):
        super().__init__(
            master=root,
            height=height,
            highlightthickness=highlightthickness,
            highlightcolor=highlightcolor,
            highlightbackground=highlightbackground,
            background=background,
            fg=fg,
            font=self.font,
        )
        self.placeholder = "Type your message here..."
        self.placeholder_color = "gray"
        self.default_fg_color = self["fg"]

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(1.0, self.placeholder)
        self["foreground"] = self.placeholder_color

    def foc_in(self, *args):
        print(self["foreground"])
        if self["foreground"] == self.placeholder_color:
            self.delete(1.0, tk.END)
            self["foreground"] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get(1.0, tk.END):
            self.put_placeholder()

    def get_string(self):
        if self["foreground"] == self.default_fg_color:
            return self.get(1.0, tk.END)
        else:
            return ""


# Thông tin người dùng
class User:
    def __init__(self, text, frame):
        self.text = text
        self.frame = frame
        self.LoadName()
        self.LoadAvatar()

    def LoadName(self):
        self.lblUsername = tk.Label(
            self.frame,
            text=self.text,
            font=("Arial", "10", "bold"),
            bg=self.frame["bg"],
            fg="white",
        )
        self.lblUsername.grid(row=0, column=1)

    def LoadAvatar(self):
        size = (25, 25)
        path = os.path.dirname(os.path.realpath(__file__)) + "\\friend_mask.png"
        if not os.path.exists(path):
            DrawMask(size, path)

        mask = Image.open(path)
        self.img = Image.open("D:\Python\Messenger\suisei1.png")
        self.output = ImageOps.fit(self.img, size, centering=(0.5, 0.5))
        self.output.putalpha(mask)

        self.output.save("D:\Python\Messenger\output.png")

        self.new_img = ImageTk.PhotoImage(self.output)

        self.lblImage = tk.Label(self.frame, bg=self.frame["bg"])
        self.lblImage["image"] = self.new_img

        self.lblImage.grid(row=0, column=0, sticky="w", padx=5, pady=5)


# Frame cuộn được
class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self, *args, **kwargs, highlightthickness=0)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Vertical.TScrollbar",
            gripcount=0,
            background="#36393f",
            darkcolor="#36393f",
            lightcolor="#36393f",
            troughcolor="#36393f",
            bordercolor="#36393f",
            arrowcolor="#36393f",
            highlightbackground="#36393f",
            arrowsize=8,
        )

        self.scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview,
            style="Vertical.TScrollbar",
        )
        self.canvas.bind("<Enter>", self.BindWheel)
        self.canvas.bind("<Leave>", self.UnbindWheel)

        self.scrollable_frame = tk.Frame(self.canvas, *args, **kwargs)
        self.scrollable_frame.bind("<Configure>", self.Check)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
            add="+",
        )

        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # self.canvas.pack(side="top", fill="both", expand=True)
        # scrollbar.pack(side="right", fill="y")
        self.grid_rowconfigure(0, weight=1)
        self.canvas.grid(row=0, column=0, sticky="NSWE")

    def OnMouseWheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def BindWheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self.OnMouseWheel)

    def UnbindWheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def Check(self, event):
        if event.height > 616:
            self.scrollbar.grid(row=0, column=1, sticky="NSWE")
            self.scrollable_frame.unbind("Configure")
            self.scrollable_frame.bind(
                "<Configure>",
                lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
            )


# Thông tin tin nhắn
class Message(tk.Frame):
    row = 0

    def __init__(self, root, text, ui, username, color=None, avatar=None):
        self.ui = ui
        self.root = root
        self.username = username
        self.color = color
        self.text = text

        super().__init__(
            root.scrollable_frame,
            bg=ui.frmChat["bg"],
            # bg="black",
            width=root.winfo_width(),
            height=(len(text) * 5 / ui.frmChat.winfo_width() + 2) * 20 + 40,
        )

        self.grid(row=ui.chat_row, column=0, sticky="NSWE", pady=(0, 8))
        ui.chat_row += 1

        self.grid_propagate(0)
        self.update()

        self.LoadAvatar()
        self.LoadName()
        self.LoadText()

        self.bind("<Enter>", self.FrameEnter)
        self.bind("<Leave>", self.FrameLeave)

        Message.row += 1

    # Đổi màu khi vào frame
    def FrameEnter(self, event):
        color = "#414247"
        self["bg"] = color
        self.txtText["bg"] = color
        self.txtName["bg"] = color
        self.lblImage["bg"] = color

    # Đổi màu khi ra frame
    def FrameLeave(self, event):
        color = self.ui.frmChat["bg"]
        self["bg"] = color
        self.txtText["bg"] = color
        self.txtName["bg"] = color
        self.lblImage["bg"] = color

    # Hiển thị avatar người nhắn
    def LoadAvatar(self):
        size = (40, 40)
        path = os.path.dirname(os.path.realpath(__file__)) + "\msg_mask.png"
        if not os.path.exists(path):
            DrawMask(size, path)

        mask = Image.open(path)
        self.img = Image.open("D:\Python\Messenger\suisei1.png")
        self.output = ImageOps.fit(self.img, size, centering=(0.5, 0.5))
        self.output.putalpha(mask)

        self.output.save("D:\Python\Messenger\output.png")

        self.new_img = ImageTk.PhotoImage(self.output)

        self.lblImage = tk.Label(self, bg=self["bg"])
        self.lblImage["image"] = self.new_img
        self.lblImage.grid(row=0, column=0, sticky="w")

    # Hiển thị tên người nhắn
    def LoadName(self):
        self.txtName = tk.Text(
            self,
            bg=self.ui.frmChat["bg"],
            # fg=self.color,
            font=("Arial", 11, "bold"),
            borderwidth=0,
            width=len(self.username)
            + ceil(self.username.count("m"))
            + ceil(self.username.count("w"))
            + ceil(self.username.count("b"))
            + 1,
            height=1,
        )
        self.txtName.insert(tk.END, self.username)
        self.txtName.config(state=tk.DISABLED)
        self.txtName.grid(row=0, column=0, sticky="wn", padx=(50, 0), pady=(15, 0))

    # Hiển thị tin nhắn
    def LoadText(self):
        self.txtText = tk.Text(
            self,
            bg=self.ui.frmChat["bg"],
            fg="white",
            font=("Arial", 11),
            borderwidth=0,
        )

        # Kiểm tra nếu tin nhắn đủ dài để xuống dòng
        if len(self.text) * 10 > self.winfo_width():
            self.txtText["width"] = self.winfo_width() // 10
        else:
            space_cnt = self.text.count(" ")
            db_count = (
                self.text.count("w") + self.text.count("m") + self.text.count("b")
            )
            self.txtText["width"] = (
                len(self.text) - ceil(space_cnt * 0.8) + ceil(db_count * 0.8)
            )

        self.txtText.insert(tk.END, self.text)
        self.txtText.grid(row=1, column=0, sticky="w", padx=(50, 0))
        self.txtText.config(state=tk.DISABLED)


# Thông tin bạn bè
class Friend:
    cur_user = None
    cnt = 0
    lbl_font = "Arial 10 bold"
    clicked_friend = None

    def __init__(self, username, row, client, ui, color="white"):
        self.client = client
        self.username = username
        self.ui = ui
        self.color = color

        ui.frmFriend.grid_columnconfigure(0, weight=1)
        self.Frame = tk.Frame(
            ui.frmFriend.scrollable_frame,
            bg=ui.frmFriend["bg"],
            height=30,
            width=200,
            cursor="hand2",
        )

        self.LoadAvatar()
        self.LoadName()

        self.Frame.bind("<Button-1>", self.SwitchFriend)
        self.Frame.bind("<Enter>", self.FrameEnter)
        self.Frame.bind("<Leave>", self.FrameLeave)
        self.lblUsername.bind("<Button-1>", self.SwitchFriend)
        self.lblUsername.bind("<Enter>", self.FrameEnter)
        self.lblUsername.bind("<Leave>", self.FrameLeave)

        self.Frame.grid_propagate(0)

    # Chuyển đổi đối tượng chat
    def SwitchFriend(self, event):
        # Kiểm tra đoạn chat hiện tại đã hoàn thành load chưa
        if self.ui.msg_loaded == False or Friend.clicked_friend == self.username:
            return

        self.client.send_messages("/quit")
        self.client.send_messages(f"/tp {self.username}")

        # Xóa thông tin đối tượng chat cũ
        for widget in self.ui.frmCur.winfo_children():
            widget.destroy()

        self.ui.chat_row = 0

        # Xóa các tin nhắn cũ
        for widget in self.ui.frmChat.scrollable_frame.winfo_children():
            widget.destroy()

        color = self.ui.frmFriend["bg"]
        for widget in self.ui.frmFriend.scrollable_frame.winfo_children():
            widget["bg"] = color
            for item in widget.winfo_children():
                item["bg"] = color

        global cur
        cur = User(text=self.username, frame=self.ui.frmCur)

        self.FrameClicked()

        self.ui.chat_cleared = True
        self.ui.frmChat.canvas.yview_moveto("0.0")

    def ChangeColor(self, color):
        self.Frame["bg"] = color
        self.lblUsername["bg"] = color
        self.lblImage["bg"] = color

    def FrameClicked(self):
        self.ChangeColor("#393c43")
        Friend.clicked_friend = self.username

    def FrameEnter(self, event):
        if Friend.clicked_friend != self.username:
            self.ChangeColor("#34373c")

    def FrameLeave(self, event=None):
        if Friend.clicked_friend != self.username:
            self.ChangeColor(self.ui.frmFriend["bg"])

    def LoadName(self):
        self.lblUsername = tk.Label(
            self.Frame,
            text=self.username,
            bg=self.ui.frmFriend["bg"],
            fg=self.color,
            font=self.lbl_font,
        )
        self.lblUsername.grid(row=0, column=1)

    def LoadAvatar(self):
        size = (25, 25)
        path = os.path.dirname(os.path.realpath(__file__)) + "\\friend_mask.png"
        if not os.path.exists(path):
            DrawMask(size, path)

        mask = Image.open(path)
        self.img = Image.open("D:\Python\Messenger\suisei1.png")
        self.output = ImageOps.fit(self.img, size, centering=(0.5, 0.5))
        self.output.putalpha(mask)

        self.output.save("D:\Python\Messenger\output.png")

        self.new_img = ImageTk.PhotoImage(self.output)

        self.lblImage = tk.Label(self.Frame, bg=self.Frame["bg"])
        self.lblImage["image"] = self.new_img
        self.lblImage.grid(row=0, column=0, sticky="w", padx=5)


# Thông tin nhóm
class Group(Friend):
    def __init__(self, username, row, client, ui, color="white"):
        super().__init__(username, row, client, ui, color="white")
        self.client = client
        self.username = username
        self.ui = ui
        self.color = color

        ui.frmFriend.grid_columnconfigure(0, weight=1)
        self.Frame = tk.Frame(
            ui.frmGroup.scrollable_frame,
            bg=ui.frmFriend["bg"],
            height=30,
            width=200,
            cursor="hand2",
        )
        self.lblUsername = tk.Label(
            self.Frame,
            text=username,
            bg=ui.frmFriend["bg"],
            fg=self.color,
            font=self.lbl_font,
        )

        self.Frame.bind("<Button-1>", self.SwitchFriend)
        self.Frame.bind("<Enter>", self.FrameEnter)
        self.Frame.bind("<Leave>", self.FrameLeave)

        self.Frame.grid_propagate(0)

        self.lblUsername.grid(row=0, column=0)


# Vẽ mask thích hợp cho từng loại avatar
def DrawMask(size, path):
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + mask.size, fill=255)
    mask.save(path)
