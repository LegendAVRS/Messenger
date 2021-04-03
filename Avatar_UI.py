import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image, ImageDraw, ImageOps
from tkinter import filedialog as fd
import os
from Widget import DrawMask


class Avatar_UI:
    size = (294, 294)

    def __init__(self, root, start_ui):
        self.start_ui = start_ui
        self.frame = tk.Frame(master=root)
        self.style = ttk.Style()

        lblIntro = tk.Label(
            self.frame,
            text="------ Select your avatar ------",
            bg=self.frame["bg"],
            font=("Arial", 15, "bold"),
        )

        lblIntro.grid(row=0, column=0, columnspan=2, sticky="n")

        self.frmAva = tk.Frame(master=self.frame, bg="#36393f")
        self.frmAva.grid(row=1, column=0, columnspan=2, pady=30)

        self.LoadDefaultAvatar()

        self.style.configure(
            "btnSelectAvatar.TButton",
            font=("Arial", 10),
            foreground="blue",
            background="blue",
        )

        self.style.configure(
            "btnContinue.TButton",
            font=("Arial", 10),
            foreground="green",
            background="green",
        )

        self.btnSelectAvatar = ttk.Button(
            self.frame,
            text="Select an image",
            style="btnSelectAvatar.TButton",
            width=14,
            command=self.LoadSelectedAvatar,
        )

        self.btnContinue = ttk.Button(
            self.frame,
            text="Continue",
            style="btnContinue.TButton",
            width=14,
        )

        self.btnSelectAvatar.grid(
            row=2,
            column=0,
            sticky="w",
            padx=(10, 0),
            pady=(0, 10),
        )
        self.btnContinue.grid(
            row=2,
            column=1,
            sticky="e",
            padx=(0, 10),
            pady=(0, 10),
        )

    def LoadDefaultAvatar(self):
        path = os.path.dirname(os.path.realpath(__file__)) + "\\ava_mask.png"
        if not os.path.exists(path):
            DrawMask(self.size, path)
        self.mask = Image.open(path)

        # load ảnh tạm thời
        temp_img_path = __file__[:-12] + "suisei1.png"
        
        self.img = Image.open(temp_img_path)
        self.output = ImageOps.fit(self.img, self.size, centering=(0.5, 0.5))
        self.output.putalpha(self.mask)

        # self.output.save("D:\Python\Messenger\output.png")

        self.new_img = ImageTk.PhotoImage(self.output)

        self.lblImage = tk.Label(self.frmAva, bg=self.frmAva["bg"])
        self.lblImage["image"] = self.new_img
        self.lblImage.grid(row=0, column=0, pady=50)

    def LoadSelectedAvatar(self):
        filetypes = (("image files", "*.png"), ("image files", "*.jpg"))
        filename = fd.askopenfilename(
            title="Select an image", initialdir="/", filetypes=filetypes
        )
        if len(filename) == 0:
            return

        self.img = Image.open(filename)
        self.output = ImageOps.fit(self.img, self.size, centering=(0.5, 0.5))
        self.output.putalpha(self.mask)

        out_img_path = __file__[:-12] + "output.png"
        self.output.save(out_img_path)

        self.new_img = ImageTk.PhotoImage(self.output)

        self.lblImage = tk.Label(self.frmAva, bg=self.frmAva["bg"])
        self.lblImage["image"] = self.new_img
        self.lblImage.grid(row=0, column=0, columnspan=2, pady=50)
