import tkinter as tk
from tkinter import ttk
from Signin_UI import Signin_UI
from Signup_UI import Signup_UI
from Avatar_UI import Avatar_UI
from tkinter import messagebox
from threading import Thread

import time
import sys
import os


def raise_frame(frame):
    frame.tkraise()


class Start_UI:
    run = True
    msg = ""
    client = None

    def __init__(self, client):
        self.client = client

        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.OnClose)

        self.signin_ui = Signin_UI(self.root, self)
        self.signup_ui = Signup_UI(self.root, self)
        self.avatar_ui = Avatar_UI(self.root, self)

        self.signin_ui.btnSignup.config(command=self.SwitchToSignup)
        self.signup_ui.btnSignin.config(command=self.SwitchToSignin)
        self.signup_ui.btnSignup.config(command=self.CheckSignupInput)

        self.signin_ui.btnSignin.config(command=self.CheckSigninInput)

        self.avatar_ui.btnContinue.config(command=self.SwitchToSignin)

        self.signup_ui.txtUsername.bind("<KeyRelease-Return>", self.CheckSignupInput)
        self.signup_ui.txtPassword.bind("<KeyRelease-Return>", self.CheckSignupInput)
        self.signup_ui.txtPasswordAgain.bind(
            "<KeyRelease-Return>", self.CheckSignupInput
        )
        self.signin_ui.txtUsername.bind("<KeyRelease-Return>", self.CheckSigninInput)
        self.signin_ui.txtPassword.bind("<KeyRelease-Return>", self.CheckSigninInput)

        self.signin_ui.frame.grid(row=0, column=0, sticky=tk.N)
        self.signup_ui.frame.grid(row=0, column=0, sticky=tk.N)

        self.root.update()
        self.SwitchToSignup()
        self.avatar_ui.frame.grid(row=0, column=0, sticky=tk.N)
        Thread(target=self.GetMessage, daemon=True).start()
        self.root.mainloop()

    def GetMessage(self):
        while self.run:
            if self.client.logged_in:
                break
            self.msg = self.client.receive_messages()
            self.msg = self.msg.decode()
            print(self.msg)
            if self.client.logged_in:
                break

    def SwitchToSignup(self):
        raise_frame(self.signup_ui.frame)
        self.root.geometry(
            f"{self.signup_ui.frame.winfo_width()}x{self.signup_ui.frame.winfo_height()}"
        )

    def SwitchToSignin(self):
        raise_frame(self.signin_ui.frame)
        self.root.geometry(
            f"{self.signin_ui.frame.winfo_width()}x{self.signin_ui.frame.winfo_height()}"
        )

    def SwitchToAvatar(self):
        raise_frame(self.avatar_ui.frame)
        self.root.geometry(
            f"{self.avatar_ui.frame.winfo_width()}x{self.avatar_ui.frame.winfo_height()}"
        )

    def CheckSignupInput(self, event=None):
        # self.SwitchToAvatar()
        self.client.send_messages("/quit")
        time.sleep(0.2)
        username = self.signup_ui.txtUsername.get_string()
        password = self.signup_ui.txtPassword.get_string()
        passwordagain = self.signup_ui.txtPasswordAgain.get_string()

        if len(username) == 0 or len(password) == 0 or len(passwordagain) == 0:
            messagebox.showerror(
                title="Error", message="Please fill in all the infomation"
            )
            return

        if password == passwordagain:
            self.client.send_messages("/register")
            time.sleep(0.2)
            self.client.send_messages(f"/usr {username}")
            time.sleep(0.5)
            if self.client.pwd_confirm == True:
                self.client.send_messages(f"/pwd {password} {passwordagain}")
                self.SwitchToAvatar()
            else:
                messagebox.showerror(title="Warning", message="Username not valid")
        else:
            messagebox.showerror(title="Warning", message="Password not the same")

    def CheckSigninInput(self, event=None):
        username = self.signin_ui.txtUsername.get_string()
        password = self.signin_ui.txtPassword.get_string()
        if len(username) == 0 or len(password) == 0:
            messagebox.showerror(
                title="Error", message="Please fill in all the infomation"
            )
            return
        self.client.send_messages(f"/quit")
        time.sleep(0.5)
        self.client.send_messages(f"/login")
        self.client.send_messages(f"/login {username} {password}")
        time.sleep(0.5)
        if self.client.logged_in == True:
            self.stop = True
            self.root.destroy()
        else:
            messagebox.showerror(title="Error", message="Try again or something")

    def OnClose(self):
        self.run = False
        self.root.destroy()


if __name__ == "__main__":
    ui = Start_UI(213)