import sqlite3

mainpath = __file__[:-18] + "group_name\\"
path = mainpath + "Group_name.db"

def create_table():
    conn = sqlite3.connect(path)
    c = conn.cursor()

    try:
        c.execute("""CREATE TABLE groupname(
                    name text                  
                    )""")
    except Exception as e:
        print("[EXCEPTION]", e)

    conn.commit()
    conn.close()


def showall():
	conn = sqlite3.connect(path)
	c = conn.cursor()

	c.execute("SELECT * FROM groupname")

	names = c.fetchall()
	if not names:
		return 
	for name in names:
		print(name[0])

	conn.commit()
	conn.close()


def show():
	conn = sqlite3.connect(path)
	c = conn.cursor()

	c.execute("SELECT * FROM groupname")

	names = c.fetchall()

	conn.commit()
	conn.close()
	
	return names


def exist(name):
    conn = sqlite3.connect(path)
    c = conn.cursor()

    c.execute("SELECT * FROM groupname WHERE EXISTS(SELECT 1 FROM groupname WHERE name = (?))", (name, ))

    statement = True if c.fetchone() else False

    conn.close()

    return statement


def insert(name):
    conn = sqlite3.connect(path)
    c = conn.cursor()

    try:
        if not exist(name):
            c.execute("INSERT INTO groupname VALUES (?)", (name, ))
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

	c.execute("DELETE FROM groupname")

	conn.commit()
	conn.close()


def delete(name):
    conn = sqlite3.connect(path)
    c = conn.cursor()

    try:
        c.execute("DELETE from groupname WHERE name = (?)", (name, ))
    except Exception as e:
        print("[EXCEPTION]", e)

    conn.commit()
    conn.close()


def delete_all():
    conn = sqlite3.connect(path)
    c = conn.cursor()

    try:
        c.execute("DELETE from groupname")
    except Exception as e:
        print("[EXCEPTION]", e)
        
    conn.commit()
    conn.close()






