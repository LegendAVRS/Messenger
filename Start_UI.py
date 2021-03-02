import tkinter as tk
from tkinter import ttk
from Signin_UI import Signin_UI
from Signup_UI import Signup_UI


def raise_frame(frame):
    frame.tkraise()


class Start_UI:
    def __init__(self):
        self.root = tk.Tk()
        self.signin_ui = Signin_UI(self.root, self)
        self.signup_ui = Signup_UI(self.root, self)

        self.signin_ui.btnSignup.config(command=self.SwitchToSignup)
        self.signup_ui.btnSignin.config(command=self.SwitchToSignin)
        self.signup_ui.btnSignup.config(command=self.CheckSignupInput)

        self.signin_ui.frame.grid(row=0, column=0, sticky=tk.N)
        self.signup_ui.frame.grid(row=0, column=0, sticky=tk.N)
        self.root.update()
        self.root.mainloop()

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

    def CheckSignupInput(self):
        username = self.signup_ui.txtUsername.get_string()
        password = self.signup_ui.txtPassword.get_string()
        passwordagain = self.signup_ui.txtPasswordAgain.get_string()

        if len(username) == 0 or len(password) == 0 or len(passwordagain) == 0:
            messagebox.showerror(
                title="Error", message="Please fill in all the infomation"
            )
            return

        if password == passwordagain:
            self.SwitchToSignin()
        else:
            messagebox.showerror(title="Warning", message="Password not the same")