from users import User
import sqlite3

def create_table():
    conn = sqlite3.connect("password.db")
    c = conn.cursor()
    
    try:
        c.execute("""CREATE TABLE user(
                    username text,
                    password text
                    )""")
    except Exception as e:
        print("[EXCEPTION]", e)

    conn.commit()
    conn.close()

def exist(person):
    conn = sqlite3.connect("password.db")
    c = conn.cursor()

    c.execute("SELECT * FROM user WHERE EXISTS(SELECT 1 FROM user WHERE username = (?))", (person.username, ))

    statement = True if c.fetchone() else False

    conn.close()

    return statement

def insert(person):
    conn = sqlite3.connect("password.db")
    c = conn.cursor()

    try:
        if not exist(person):
            c.execute("INSERT INTO user VALUES (?, ?)", (person.username, person.password))
        # c.execute("INSERT INTO user VALUES (:username, :password)", {'username': person.username, 'password': person.password})
    except Exception as e:
        print("[EXCEPTION]", e)

    conn.commit()
    conn.close()


def insert_many(List):
    conn = sqlite3.connect("password.db")
    c = conn.cursor()

    try:
        c.executemany("INSERT INTO user VALUES (?, ?)", (List))
    except Exception as e:
        print("[EXCEPTION]", e)

    conn.commit()
    conn.close()

def getall():
    conn = sqlite3.connect("password.db")
    c = conn.cursor()

    c.execute("SELECT * FROM user")
    items = c.fetchall()
    
    conn.close()

    return items


def update_name(old_name, new_name):
    conn = sqlite3.connect("password.db")
    c = conn.cursor()

    try:
        c.execute("UPDATE user SET username = new_name WHERE username = old_name")
    except Exception as e:
        print("[EXCEPTION]", e)

    conn.commit()
    conn.close()


def update_password(old_pass, new_pass):
    conn = sqlite3.connect("password.db")
    c = conn.cursor()

    try:
        c.execute("UPDATE user SET password = (?) WHERE password = (?)", (new_pass, old_pass))
    except Exception as e:
        print("[EXCEPTION]", e)

    conn.commit()
    conn.close()


def show():
    conn = sqlite3.connect("password.db")
    c = conn.cursor()

    c.execute("SELECT * FROM user ORDER BY username")
    items = c.fetchall()

    for item in items:
        print(item)

    conn.close()


def delete(person):
    conn = sqlite3.connect("password.db")
    c = conn.cursor()
    try:
        c.execute("DELETE from user WHERE username = (?) AND password = (?)", (person.username, person.passowrd))
    except Exception as e:
        print("[EXCEPTION]", e)
    
    conn.commit()
    conn.close()

def delete_all():
    conn = sqlite3.connect("password.db")
    c = conn.cursor()
    try:
        c.execute("DELETE from user")
    except Exception as e:
        print("[EXCEPTION]", e)
    
    conn.commit()
    conn.close()


