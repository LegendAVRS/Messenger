import sqlite3

mainpath = __file__[:-13] + "client_chat\\"
path = mainpath
print(path)

def create_table():
    conn = sqlite3.connect(path)
    c = conn.cursor()
    
    try:
        c.execute("""CREATE TABLE chat(
                    username text,
                    conversation text
                    )""")
    except Exception as e:
        print("[EXCEPTION]", e)

    conn.commit()
    conn.close()

def showall():
	conn = sqlite3.connect(path)
	c = conn.cursor()

	c.execute("SELECT * FROM user")
	# c.execute("SELECT * FROM user WHERE username LIKE 'so%'")

	items = c.fetchall()
	for item in items:
		print(item)

	conn.close()


def exist(name):
	conn = sqlite3.connect(path)
	c = conn.cursor()

	c.execute("SELECT * FROM chat WHERE EXISTS(SELECT 1 FROM chat WHERE username = (?))", (name, ))

	statement = True if c.fetchone() else False

	conn.close()

	return statement

def update_chat(name, msg):
	conn = sqlite3.connect(path)
	c = conn.cursor()

	if not exist(name):
		c.execute("INSERT INTO chat VALUES (?, ?)", (name, ""))

	c.execute("SELECT * FROM chat WHERE username = (?)", (name, ))
	text = c.fetchone()[1] + msg
	c.execute("UPDATE chat SET conversation = (?) WHERE username = (?)", (text, name))
	
	conn.commit()
	conn.close()

def show(name):
	if not exist(name):
		print("Wrong name")
		return -1


	conn = sqlite3.connect(path)
	c = conn.cursor()

	c.execute("SELECT * FROM chat WHERE username = (?)", (name, ))
	text = c.fetchone()[1]
	# print(text)

	conn.commit()
	conn.close()

	return text
	

def clear(name):

    conn = sqlite3.connect(path)
    c = conn.cursor()

    c.execute("UPDATE chat SET conversation = (?) WHERE username = (?)", ("", name))

    conn.commit()
    conn.close()

# path = mainpath + "sora.db"
# msg = show("bot")
# print(msg)


# print("\n\n\n")

# path = mainpath + "bot.db"
# show("sora")