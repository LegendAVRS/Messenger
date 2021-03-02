import tkinter as tk
from tkinter import ttk


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
        self.txtChat.config(state=tk.DISABLED)

ui = UI()
ui.root.mainloop()
ui.txtChat.insert("end", f"You: ", "bold")
ui.txtChat.insert("end", "Hello", "text_font")