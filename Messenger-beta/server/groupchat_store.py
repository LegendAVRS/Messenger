import sqlite3

mainpath = __file__[:-18] + "group_chat\\"
path = mainpath

def create_table():
    conn = sqlite3.connect(path)
    c = conn.cursor()

    try:
        c.execute("""CREATE TABLE groupchat(
                    conversation text                  
                    )""")
    except Exception as e:
        print("[EXCEPTION]", e)

    conn.commit()
    conn.close()


def showall():
	conn = sqlite3.connect(path)
	c = conn.cursor()

	c.execute("SELECT * FROM groupchat")

	text = c.fetchone()
	if not text:
		text = ""
	else:
		text = text[0]
	print(text)

	conn.commit()
	conn.close()


def show():
	conn = sqlite3.connect(path)
	c = conn.cursor()

	c.execute("SELECT * FROM groupchat")

	text = c.fetchone()

	conn.commit()
	conn.close()
	
	return text[0]


def update_chat(msg):
	conn = sqlite3.connect(path)
	c = conn.cursor()

	c.execute("SELECT * FROM groupchat")
	text = c.fetchone()
	if not text:
		text = ""
		c.execute("INSERT INTO groupchat VALUES (?)", (text, ))
	else:
		text = text[0]
	text = text + msg
	c.execute("UPDATE groupchat SET conversation = (?)", (text, ))

	conn.commit()
	conn.close()


def clear():
	conn = sqlite3.connect(path)
	c = conn.cursor()

	c.execute("DELETE FROM groupchat")

	conn.commit()
	conn.close()

# path = mainpath + "tsutaya" + "_chat" + ".db"
# print(path)
# create_table()
# # update_chat("[sora] Hello")
# showall()









