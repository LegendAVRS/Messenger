import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# import client
from threading import Thread

correct_pass_msg = "[SERVER] Correct password."


def raise_frame(frame):
    frame.tkraise()


"""
    Entry thông thường không có placeholder
    Tạo class entry mới inherit từ ttk.Entry 
    Thiết kế placeholder cho entry này 
"""


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


class Friend:
    cur_user = None

    def __init__(self, username, chat="None"):
        self.username = username
        self.lblUsername = tk.Label(ui.frmFriend, text=username)
        self.chat = chat
        self.lblUsername.bind("<Button-1>", self.ShowChat)

        Friend.cur_user = self
        self.lblUsername.pack()

    def ShowChat(self, event):
        ui.txtChat.delete(1.0, tk.END)
        ui.txtChat.insert(tk.END, self.chat)
        Friend.cur_user = self


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
        self.root.configure(background="#242526")

        # Khởi tạo frame danh sách bạn bè
        self.frmFriend = tk.Frame(
            self.root,
            background="#1b1c1f",
            height=625,
            width=250,
            highlightthickness=2,
            highlightbackground="black",
        )
        self.frmFriend.grid(row=0, column=0, sticky=tk.N, rowspan=2)

        # Khởi tạo frame người dùng
        self.frmUser = tk.Frame(
            self.root,
            background="gray",
            height=40,
            width=250,
            highlightthickness=2,
            highlightbackground="black",
        )
        self.frmUser.grid(row=2, column=0, sticky=tk.N)

        # Khởi tạo frame đói tượng chat hiện tại
        self.frmCur = tk.Frame(self.root, background="gray", height=40, width=645)
        self.frmCur.grid(row=0, column=1, sticky=tk.NW, columnspan=2)

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
        # self.txtChat.config(state=tk.DISABLED)

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


# Class cho UI phần đăng nhập tài khoản
class Signin_UI:
    lbl_font = "Arial 20"
    entry_font = "Arial 12"
    btn_font = "Arial 11"

    def __init__(self, root, start_root):
        # self.root.title("Messenger")
        self.start_root = start_root
        self.frame = tk.Frame(root)
        self.style = ttk.Style()

        # Khởi tạo style cho các widget
        self.style.configure(
            "btnSignup.TButton",
            font=self.btn_font,
            foreground="green",
            background="green",
        )
        self.style.configure(
            "btnSignin.TButton",
            font=self.btn_font,
            background="blue",
            foreground="blue",
        )

        # Khởi tạo label tiêu đề
        self.lblTop = tk.Label(self.frame, text="Sign in", font=self.lbl_font)
        self.lblTop.grid(row=0, column=0, pady=20)

        # Khởi tạo entry tên người dùng
        self.txtUsername = PH_Entry(
            self.frame, placeholder="Username", width=28, font=self.entry_font
        )
        self.txtUsername.grid(row=1, column=0, ipady=10, padx=20)

        # Khởi tạo entry mật khẩu
        self.txtPassword = PH_Entry(
            self.frame, placeholder="Password", width=28, font=self.entry_font
        )
        self.txtPassword.grid(row=2, column=0, ipady=10, padx=20, pady=20)

        # Khởi tạo button đăng nhập
        self.btnSignin = ttk.Button(
            self.frame,
            text="Sign in",
            style="btnSignin.TButton",
            command=self.CheckInput,
        )
        self.btnSignin.grid(row=3, column=0, ipadx=80, ipady=10, padx=20)

        # Khởi tạo button đăng ký
        self.btnSignup = ttk.Button(
            self.frame,
            text="Create an account",
            style="btnSignup.TButton",
            command=self.CloseUI,
        )
        self.btnSignup.grid(row=4, column=0, ipadx=65, ipady=10, pady=20)

        # client.send_messages("/login")
        # Thread(target=self.GetMessage).start()
        # self.root.mainloop()

    # def GetMessage(self):
    #     while True:
    #         if client.logged_in == True:
    #             self.root.destroy()

    def SendMessage(self):
        # client.send_messages(
        #     f"/login {self.txtUsername.get()} {self.txtPassword.get()}"
        # )
        pass

    def CloseUI(self):
        raise_frame(self.start_root.signup_ui.frame)
        self.start_root.root.geometry(
            f"{self.start_root.signup_ui.frame.winfo_width()}x{self.start_root.signup_ui.frame.winfo_height()}"
        )

    def CheckInput(self):
        username = self.txtUsername.get_string()
        password = self.txtPassword.get_string()
        if len(username) == 0 or len(password) == 0:
            messagebox.showerror(
                title="Error", message="Please fill in all the infomation"
            )
            return


"""
    Class cho UI đăng ký tài khoản
    Inherit từ Signin_UI
"""


class Signup_UI(Signin_UI):
    def __init__(self, root, start_root):
        super().__init__(root, start_root)
        self.lblTop["text"] = "Sign up"
        self.txtPasswordAgain = PH_Entry(
            self.frame,
            width=28,
            placeholder="Type your password again",
            font=self.entry_font,
        )
        self.btnSignup.config(command=self.CheckInput)
        self.btnSignin.config(command=self.CloseUI)
        self.txtPasswordAgain.grid(row=3, column=0, ipady=10, padx=20, pady=(0, 20))
        self.btnSignup.grid(row=4, column=0, pady=0)
        self.btnSignin.grid(row=5, column=0, pady=20)

    def CheckInput(self):
        username = self.txtUsername.get_string()
        password = self.txtPassword.get_string()
        passwordagain = self.txtPasswordAgain.get_string()

        if len(username) == 0 or len(password) == 0 or len(passwordagain) == 0:
            messagebox.showerror(
                title="Error", message="Please fill in all the infomation"
            )
            return

        if password == passwordagain:
            self.root.destroy()
        else:
            messagebox.showerror(title="Warning", message="Password not the same")

    def CloseUI(self):
        raise_frame(self.start_root.login_ui.frame)
        self.start_root.root.geometry(
            f"{self.start_root.login_ui.frame.winfo_width()}x{self.start_root.login_ui.frame.winfo_height()}"
        )


class Start_UI:
    def __init__(self):
        self.root = tk.Tk()
        self.login_ui = Signin_UI(self.root, self)
        self.signup_ui = Signup_UI(self.root, self)
        self.login_ui.frame.grid(row=0, column=0, sticky=tk.N)
        self.signup_ui.frame.grid(row=0, column=0, sticky=tk.N)
        self.root.update()
        self.root.mainloop()


if __name__ == "__main__":
    start_ui = Start_UI()
# login_ui = Signin_UI()
# signup_ui = Signup_UI()
# login_ui.frame.grid(row=0, column=0)
# raise_frame(login_ui.frame)
# login_ui.root.mainloop()

# ui = UI()
# ui.root.mainloop()
