from socket import AF_INET, SOCK_STREAM, socket, gethostname, gethostbyname
from threading import Thread
import time
import datetime
import os # for opening cmd

from users import User
import info_database as db

# opening cmd
# os.system("start cmd")


"""

    COMMANDS:
        /SERVER
        /list: list all usernames stored in the server
        /online_list: list all usernames now are online
        /tp <name/SERVER>: change to a person or SERVER
        /location: show the location of the client

"""

# SERVER COMMUNICATION
login_instruction = "[SERVER] Inset [/login <username> <password>]"
error = "[SERVER] Unvalid Command."
username_error = "[SERVER] Username not valid."
password_error = "[SERVER] Wrong password."

# GLOBAL CONSTANTS
PORT = 5050
BUFSIZ = 512
HOST = "localhost"
# HOST = gethostbyname(gethostname())
ADDR = (HOST, PORT)
MAX_CONNECTION = 15

# GLOBAL VARIABLES
client_connection = {} # store the address by the client's name
client_info = {} # clients' usernmae and password

"""========================================================================================================"""

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR) # set up new server

def get_messages(client):
    """
    => Get messages from client
    :param client: connection
    :return: str if there is a message 
           : False if there is not any message
    """

    try:
        message = client.recv(BUFSIZ).decode()
        return message
    except Exception as e:
        print("[EXCEPTION]", e)
        return False



def client_chat(client):
    """
    => Process client messages
    :param client: connection
    :return: None
    """

    sender = get_messages(client)
    receiver = get_messages(client)
    while True:
        msg = get_messages
        print(f"[{sender} -> {receiver}] {msg}")
    client.close()


def client_login(client):
    """
    => Client's login sites
    :param client: connection
    :return: None
    """

    client.send(bytes("[SERVER] LOGIN PAGE", "utf8"))
    time.sleep(0.1)

    try:
        while True:
            client.send(bytes(login_instruction, "utf8"))
            try:
                msg = get_messages(client)

                if msg == False:
                    client.send(bytes(error, "utf8"))
                    continue

                temp = msg.split()

                if len(temp) == 1 or len(temp) == 2:
                    client.send(bytes(error, "utf8"))
                    continue

                cmd, username, password = temp
                if cmd != "/login":
                    client.send(bytes(error, "utf8"))
                    continue

                if username not in client_info:
                    client.send(bytes(username_error, "utf8"))
                    continue
                if password != client_info[username]:
                    client.send(bytes(password_error, "utf8"))
                    continue

                client.send(bytes("[SERVER] Correct password.", "utf8"))
                client.send(bytes(f"""
                            ======================================
                            \t\tWelcome back {username}
                            ======================================""", "utf8"))

                return username
                
            except Exception as e:
                print("[EXCEPTION]", e)
                return -1
    except Exception as e:
        print("[EXCEPTION]", e)
        return -1


def client_register(client):
    return -1


def client_and_server(client):
    client.send(bytes("[SERVER] Welcome back to VLC chat room!!!", "utf8"))
    client.send(bytes("[SERVER] Use '/login' to login or '/register' to register", "utf8"))
    time.sleep(0.1)

    while True:
        msg = get_messages(client)
        if msg == "/register":
            command = client_register(client)
            if command == "/quit":
                continue
            client.send(bytes("[SERVER] Please login again.", "utf8"))
            time.sleep(0.3)
        elif msg == "/login":
            client_login(client)


        
            


def connection():
    """
    => Wait for connection from new clients, start new thread once connected
    :return: None
    """


    while True:
        try:
            client, addr = SERVER.accept()
            print(f"[CONNECTION] Connection from {addr}")

            Thread(target=client_and_server, args=(client, )).start()
        except Exception as e:
            print("[EXCEPTION]", e)
            break
    print("[END] The server has been crashed!!!")


def get_info():
    """
    => get client's username and password
    :return: a dictionary stores the username and password
    """

    account = dict(db.getall())
    return account

if __name__ == "__main__":
    # get all username and password 
    client_info = get_info()
    print(client_info)

    # open server with some connections
    print("[LISTENING] Server is starting...")
    SERVER.listen(MAX_CONNECTION)

    # start the server
    server_thread = Thread(target=connection)
    server_thread.start()
    server_thread.join()
    SERVER.close()

