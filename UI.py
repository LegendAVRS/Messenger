from tkinter import *


class UI:
    root_width = 400
    root_height = 300

    txtChat_width = 30
    txtChat_height = 15

    def __init__(self):
        # Khởi tạo window
        self.root = Tk()
        self.root.geometry(f"{self.root_height}x{self.root_width}")

        # Khởi tạo chat text box
        self.txtChat = Text(
            self.root, width=self.txtChat_width, height=self.txtChat_height
        )
        self.txtChat.grid(columnspan=4, row=0, column=0, pady=30, padx=30)
        # Khởi tạo button file
        self.btnFile = Button(self.root, text="File", width=6)
        self.btnFile.grid(row=1, column=0, padx=5)

        # Khởi tạo chat input text box
        self.txtSend = Text(
            self.root,
            width=20,
            height=self.btnFile.winfo_height(),
        )
        self.txtSend.grid(row=1, column=1)

        # Khởi tạo button send
        self.btnSend = Button(self.root, text="Send", width=6)
        self.btnSend.grid(row=1, column=2)

        self.root.mainloop()


ui = UI()