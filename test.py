import tkinter as tk


class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self, *args, **kwargs, highlightthickness=0)

        scrollbar = tk.Scrollbar(
            self, orient="vertical", command=self.canvas.yview, width=12
        )
        self.canvas.bind("<Enter>", self.BindWheel)
        self.canvas.bind("<Leave>", self.UnbindWheel)

        self.scrollable_frame = tk.Frame(self.canvas, *args, **kwargs)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        # canvas.pack(side="left", fill="both", expand=True)
        # scrollbar.pack(side="right", fill="y")
        # self.grid_rowconfigure(0, weight=1)
        self.canvas.grid(row=0, column=0, sticky="NSWE")
        scrollbar.grid(row=0, column=1, sticky="NSEW")

    def OnMouseWheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def BindWheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self.OnMouseWheel)

    def UnbindWheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")


class ui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("200x400")

        self.frmFriend = ScrollableFrame(
            self.root,
            background="#1b1c1f",
            # bg="green",
            width=200,
            # height=400,
            highlightbackground="black",
        )

        self.frmFriend.grid_propagate(0)
        self.root.grid_columnconfigure(0, weight=1)
        self.frmFriend.update()
        print(self.frmFriend.winfo_height())
        print(self.frmFriend.scrollable_frame.winfo_height())
        self.frmFriend.grid(row=0, column=0, sticky="NSEW")

        self.lblFrame = tk.Label(
            self.frmFriend.scrollable_frame,
            bg=self.frmFriend["bg"],
            fg="white",
            text="------ User list ------",
            # font=self.lblFrm_font,
        )
        self.lblFrame.grid(row=0, column=0, sticky="NSEW")
        for i in range(1, 15):
            lbl = tk.Label(self.frmFriend.scrollable_frame, text="friend" + str(i))
            lbl.grid(row=i, column=0, sticky="nsew")

        self.root.mainloop()


ui = ui()