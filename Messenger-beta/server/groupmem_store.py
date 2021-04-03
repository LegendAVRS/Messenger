import sqlite3

mainpath = __file__[:-17] + "group_chat\\"
path = mainpath

def create_table():
    conn = sqlite3.connect(path)
    c = conn.cursor()

    try:
        c.execute("""CREATE TABLE groupmem(
                    member text,      
                    role text            
                    )""")
    except Exception as e:
        print("[EXCEPTION]", e)

    conn.commit()
    conn.close()


def showall():
	conn = sqlite3.connect(path)
	c = conn.cursor()

	c.execute("SELECT * FROM groupmem")

	members = c.fetchall()
	if not members:
		return 
	for member in members:
		print(member)

	conn.commit()
	conn.close()


def show():
	conn = sqlite3.connect(path)
	c = conn.cursor()

	c.execute("SELECT * FROM groupmem")

	members = c.fetchall()

	conn.commit()
	conn.close()
	
	return members


def exist(name):
    conn = sqlite3.connect(path)
    c = conn.cursor()

    c.execute("SELECT * FROM groupmem WHERE EXISTS(SELECT 1 FROM groupmem WHERE member = (?))", (name, ))

    statement = True if c.fetchone() else False

    conn.close()

    return statement


def insert(name, role = "MEMBER"):

    conn = sqlite3.connect(path)
    c = conn.cursor()

    try:
        if not exist(name):
            c.execute("INSERT INTO groupmem VALUES (?, ?)", (name, role))
        # c.execute("INSERT INTO user VALUES (:username, :password)", {'username': person.username, 'password': person.password})
        else:
            print(f"{name} has already existed")
    except Exception as e:
        print("[EXCEPTION]", e)

    conn.commit()
    conn.close()


def clear():
	conn = sqlite3.connect(path)
	c = conn.cursor()

	c.execute("DELETE FROM groupmem")

	conn.commit()
	conn.close()


def change_role(name):
    conn = sqlite3.connect(path)
    c = conn.cursor()

    if not exist(name):
        print(f"{name} does not exist")
        return
    
    c.execute("SELECT * FROM groupmem WHERE member = (?)", (name, ))
    now_role = c.fetchone()
    if not now_role:
        print("The member list is empty")
        return
    
    now_role = now_role[1]
    now_role = "MEMBER" if now_role == "ADMIN" else "ADMIN"
    # print(now_role)
    c.execute("UPDATE groupmem SET role = (?) WHERE member = (?)", (now_role, name))

    conn.commit()
    conn.close()

# path = mainpath + "tsutaya" + "_mem" + ".db"
# print(path)
# create_table()
# clear()
# showall()









