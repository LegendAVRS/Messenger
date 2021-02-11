import tkinter as tk


class UI:
    txtChat_width = 30
    txtChat_height = 25

    txtChat_font = "Helvatica 10"

    txtSend_font = "Helvatica 10"
    txtSend_length = 0
    # Khởi tạo UI
    def __init__(self):
        # Root
        self.root = tk.Tk()

        # Khởi tạo chat text box
        self.txtChat = tk.Text(
            self.root,
            width=self.txtChat_width,
            height=self.txtChat_height,
            highlightbackground="gray",
            highlightthickness=1,
        )
        self.txtChat.grid(columnspan=3, row=0, column=0, pady=30, padx=30)
        self.txtChat.tag_configure("right", justify="right")
        self.txtChat.tag_configure("left", justify="left")
        self.txtChat.tag_configure("bold", font=f"{self.txtChat_font} bold")
        self.txtChat.tag_configure("text_font", font=f"{self.txtChat_font}")
        self.txtChat.config(state=tk.DISABLED)

        # Khởi tạo button file
        self.btnFile = tk.Button(
            self.root,
            text="File",
            width=6,
        )
        self.btnFile.grid(row=1, column=0, pady=(0, 10), padx=(10, 0))

        # Khởi tạo chat input text box
        self.txtSend = tk.Text(
            self.root,
            width=self.txtChat_width,
            height=self.btnFile.winfo_height() + 1,
            font=self.txtSend_font,
            highlightthickness=1,
            highlightcolor="#5ea9ff",
            highlightbackground="gray",
        )
        self.txtSend.bind("<KeyRelease-Return>", self.SendMessage)
        self.txtSend.bind("<FocusOut>", self.InsertPlaceHolder)
        self.txtSend.bind("<Button-1>", self.DeletePlaceHolder)
        self.txtSend.bind("<KeyRelease>", self.TextLenCount)
        self.txtSend.tag_configure("gray", foreground="gray")
        self.InsertPlaceHolder()
        self.txtSend.grid(row=1, column=1, pady=(0, 10), padx=10)

        # Khởi tạo button send
        self.btnSend = tk.Button(
            self.root, text="Send", width=6, command=self.SendMessage
        )
        self.btnSend.grid(row=1, column=2, pady=(0, 10), padx=(0, 10))

        # Mainloop
        self.root.mainloop()

    # Chèn string placholder khi txtSend không có focus
    def InsertPlaceHolder(self, event=None):
        if self.txtSend_length == 0:
            self.txtSend.insert(1.0, "Type text here...", "gray")

    # Xóa string placholder khi txtSend không có focus
    def DeletePlaceHolder(self, event):
        if self.txtSend_length == 0:
            self.txtSend.delete(1.0, tk.END)

    # Đếm độ dài xâu hiện có trong txtSend
    def TextLenCount(self, event=None):
        self.txtSend_length = len(self.txtSend.get(1.0, tk.END))
        if self.txtSend.get(1.0, tk.END) == "\n":
            self.txtSend_length -= 1

    # Gửi tin nhắn
    def SendMessage(self, event=None):
        txt = self.txtSend.get(1.0, tk.END)
        if self.txtSend_length == 0 or txt == "\n":
            return

        self.txtChat.config(state=tk.NORMAL)
        self.txtChat.insert("end", f"You: ", "bold")
        self.txtChat.insert("end", f"{txt}", "text_font")
        if event == None:
            self.txtChat.insert("end", "\n")

        self.txtSend.delete(1.0, tk.END)
        self.TextLenCount()
        self.txtChat.config(state=tk.DISABLED)


if __name__ == "__main__":
    ui = UI()
