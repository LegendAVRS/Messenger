import tkinter as tk
from tkinter import filedialog, Text, messagebox, filedialog, Label, Button, Tk
from PIL import Image, ImageTk
import os
import cv2
import threading
import signal
import time



# def openfilename(): 
  
#     # open file dialog box to select image 
#     # The dialogue box has a title "Open" 
#     filename = filedialog.askopenfilename(initialdir="/", title="Select File",
#                                         filetypes=(("png type", "*.png"), ("jpeg type", "*.jpeg"), ("all", "*.*"))) 
#     return filename 


# def open_img(): 
#     # Select the Imagename  from a folder  
#     x = openfilename() 
  
#     # opens the image 
#     img = Image.open(x) 
      
#     # resize the image and apply a high-quality down sampling filter 
#     img = img.resize((250, 250), Image.ANTIALIAS) 
  
#     # PhotoImage class is used to add image to widgets, icons etc 
#     img = ImageTk.PhotoImage(img) 
   
#     # create a label 
#     panel = Label(root, image = img) 
      
#     # set the image as img  
#     panel.image = img 
#     panel.grid(row = 2) 


# # Create a window
# root = Tk() 
  
# # Set Title as Image Loader 
# root.title("Image Loader") 
  
# # Set the resolution of window 
# root.geometry("550x300") 
  
# # Allow Window to be resizable 
# root.resizable(width = True, height = True) 
  
# # Create a button and place it into the window using grid layout 
# btn = Button(root, text ='open image', command = open_img).grid( 
#                                         row = 1, columnspan = 4) 
# root.mainloop()

	
# statement = messagebox.askyesno(title="AVATAR", message="Do you want to set your AVATAR")
# if statement == True:
#     filename = filedialog.askopenfilename(initialdir="/", title="Select Your Avatar",
#                                         filetypes=(("png files", "*.png"), ("jpeg files", "*.jpeg"), ("jpg files", "*.jpg")))
#     img = cv2.imread(filename)
#     cv2.imshow("Image", img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

# from shutil import copyfile

# img_path = r"D:\Python\VLC\My project\server\default-profile.jpg"
# dir_path = r"D:\Python\VLC\My project\server\avatar\my.png"
# copyfile(img_path, dir_path)


exit_event = threading.Event()

def run():
    for i in range(1, 31):
        print(f"{i} of 30 iterations")
        time.sleep(1)

        if exit_event.is_set():
            break
    print(f"{i} iterations completed before exiting")

def signal_handle(signum, frame):
    exit_event.set()

signal.signal(signal.SIGINT, signal_handle)
th = threading.Thread(target=run)
th.start()
th.join()