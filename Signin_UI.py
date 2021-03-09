import tkinter as tk
from tkinter import ttk
from Widget import PH_Entry
from tkinter import messagebox

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
            self.frame, text="Sign in", style="btnSignin.TButton"
        )
        self.btnSignin.grid(row=3, column=0, ipadx=80, ipady=10, padx=20)

        # Khởi tạo button đăng ký
        self.btnSignup = ttk.Button(
            self.frame, text="Create an account", style="btnSignup.TButton"
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
