from PIL import Image, ImageOps, ImageDraw, ImageTk
import tkinter as tk

root = tk.Tk()


size = (40, 40)
mask = Image.new("L", size, 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((0, 0) + size, fill=255)

im = Image.open("D:\Python\Messenger\lan1.png")

output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
output.putalpha(mask)

# output.save("D:\Python\Messenger\output.png")
new_img = ImageTk.PhotoImage(output)

label = tk.Label(root, image=new_img)
label.pack()
root.mainloop()