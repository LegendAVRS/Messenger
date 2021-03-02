import tkinter as tk
from tkinter import ttk

font = "Arial 10"

class Console:
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

# def loop(num):
#     if num == 21:
#         return
#     textChat['state'] = tk.NORMAL
#     textChat.insert("end", str(num) + ' ')
#     textChat['state'] = tk.DISABLED
#     root.after(100, lambda: loop(num + 1))

# def sayHello():
#     textChat['state'] = tk.NORMAL
#     textChat.insert("end", "Hello\n", "bold")
#     textChat['state'] = tk.DISABLED