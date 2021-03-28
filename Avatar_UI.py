import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image, ImageDraw, ImageOps
from tkinter import filedialog as fd


class Avatar_UI:
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
        size = (298, 298)
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + mask.size, fill=255)

        self.img = Image.open("D:\Python\Messenger\suisei1.png")
        self.output = ImageOps.fit(self.img, size, centering=(0.5, 0.5))
        self.output.putalpha(mask)

        self.output.save("D:\Python\Messenger\output.png")

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

        size = (298, 298)
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + mask.size, fill=255)

        self.img = Image.open(filename)
        self.output = ImageOps.fit(self.img, size, centering=(0.5, 0.5))
        self.output.putalpha(mask)

        self.output.save("D:\Python\Messenger\output.png")

        self.new_img = ImageTk.PhotoImage(self.output)

        self.lblImage = tk.Label(self.frmAva, bg=self.frmAva["bg"])
        self.lblImage["image"] = self.new_img
        self.lblImage.grid(row=0, column=0, columnspan=2, pady=50)
