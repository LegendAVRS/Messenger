import tkinter as tk
from tkinter import ttk
import sqlite3
import sys
import UI


# # Class cho UI chương trình chính
# class UI:
#     txtChat_width = 80
#     txtChat_height = 36

#     txtChat_font = "Arial 10"

#     txtSend_font = "Arial 10"
#     txtSend_length = 0
#     # Khởi tạo UI
#     def __init__(self):
#         # Root
#         self.root = tk.Tk()
#         self.root.title("Messenger")
#         self.root.configure(background="#242526")

#         # Khởi tạo chat text box
#         self.txtChat = tk.Text(
#             self.root,
#             width=self.txtChat_width,
#             height=self.txtChat_height,
#             highlightbackground="#313236",
#             highlightthickness=1,
#             background="#313236",
#             fg="white",
#         )
#         self.txtChat.grid(columnspan=2, row=1, column=1, sticky=tk.NW)

#         self.txtChat.tag_configure("right", justify="right")
#         self.txtChat.tag_configure("left", justify="left")
#         self.txtChat.tag_configure("bold", font=f"{self.txtChat_font} bold")
#         self.txtChat.tag_configure("text_font", font=f"{self.txtChat_font}")
#         self.txtChat.config(state=tk.DISABLED)



# mainpath = "D:\\Python\\VLC\\My project\\server\\client_chat" + "\\bot.db"
# path = mainpath
# print(path)

# def create_table():
#     conn = sqlite3.connect(path)
#     c = conn.cursor()
    
#     try:
#         c.execute("""CREATE TABLE chat(
#                     username text,
#                     conversation text
#                     )""")
#     except Exception as e:
#         print("[EXCEPTION]", e)

#     conn.commit()
#     conn.close()

# # def show():
# # 	conn = sqlite3.connect(path)
# # 	c = conn.cursor()

# # 	c.execute("SELECT * FROM user")
# # 	# c.execute("SELECT * FROM user WHERE username LIKE 'so%'")

# # 	items = c.fetchall()
# # 	for item in items:
# # 		print(item)

# # 	conn.close()


# def exist(name):
# 	conn = sqlite3.connect(path)
# 	c = conn.cursor()

# 	c.execute("SELECT * FROM chat WHERE EXISTS(SELECT 1 FROM chat WHERE username = (?))", (name, ))

# 	statement = True if c.fetchone() else False

# 	conn.close()

# 	return statement

# def update_chat(name, msg):
# 	conn = sqlite3.connect(path)
# 	c = conn.cursor()

# 	if not exist(name):
# 		c.execute("INSERT INTO chat VALUES (?, ?)", (name, ""))

# 	c.execute("SELECT * FROM chat WHERE username = (?)", (name, ))
# 	text = c.fetchone()[1] + msg
# 	c.execute("UPDATE chat SET conversation = (?) WHERE username = (?)", (text, name))
# 	conn.commit()
# 	conn.close()

# def show(name):
# 	if not exist(name):
# 		print("Wrong name")
# 		return -1


# 	conn = sqlite3.connect(path)
# 	c = conn.cursor()

# 	c.execute("SELECT * FROM chat WHERE username = (?)", (name, ))
# 	text = c.fetchone()[1]
# 	print(text)

# 	conn.commit()
# 	conn.close()

# 	return text
	


UI.run()

    
