import tkinter as tk
from tkinter import ttk
from Widget import PH_Entry
from tkinter import messagebox
from Signin_UI import Signin_UI

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
        self.txtPasswordAgain.grid(row=3, column=0, ipady=10, padx=20, pady=(0, 20))
        self.btnSignup.grid(row=4, column=0, pady=0)
        self.btnSignin.grid(row=5, column=0, pady=20)

        self.txtUsername.lift()
        self.txtPassword.lift()
        self.txtPasswordAgain.lift()
        self.btnSignup.lift()
        self.btnSignin.lift()
