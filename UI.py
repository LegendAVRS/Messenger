import tkinter as tk


class UI:
    root_width = 500
    root_height = 400

    txtChat_width = 43
    txtChat_height = 20

    def __init__(self):
        # Khởi tạo window
        self.root = tk.Tk()
        self.root.geometry(f"{self.root_height}x{self.root_width}")

        # Khởi tạo chat text box
        self.txtChat = tk.Text(
            self.root, width=self.txtChat_width, height=self.txtChat_height
        )
        self.txtChat.grid(columnspan=4, row=0, column=0, pady=30, padx=30)
        self.txtChat.tag_configure("right", justify="right")
        self.txtChat.tag_configure("left", justify="left")

        # Khởi tạo button file
        self.btnFile = tk.Button(self.root, text="File", width=6)
        self.btnFile.grid(row=1, column=0, padx=5)

        # Khởi tạo chat input text box
        self.txtSend = tk.Text(
            self.root,
            width=self.txtChat_width - 10,
            height=self.btnFile.winfo_height() + 1,
        )
        # self.txtSend.bind("<KeyRelease-Return>", self.SendMessage)
        self.txtSend.grid(row=1, column=1)

        # Khởi tạo button send
        self.btnSend = tk.Button(
            self.root, text="Send", width=6, command=self.SendMessage
        )
        self.btnSend.grid(row=1, column=2)

        # Mainloop
        self.root.mainloop()

    # Gửi tin nhắn
    def SendMessage(self, event=None):
        self.txtChat.config(state=tk.NORMAL)
        txt = self.txtSend.get(1.0, tk.END)
        if txt == "\n":
            return
        self.txtChat.insert("end", f"{txt}", "right")
        self.txtChat.insert("end", f"{txt}", "left")
        self.txtSend.delete(1.0, tk.END)
        self.txtChat.config(state=tk.DISABLED)


ui = UI()