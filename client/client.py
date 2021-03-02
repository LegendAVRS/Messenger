from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock
from console import Console
import time
import os
import UI

HOST = "localhost"
PORT = 5050
ADDR = (HOST, PORT)
BUFSIZ = 512


client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)
messages = []
lock = Lock()

# COMMAND
CLEAR = "/clear"
CONSOLE = "/console"

# condition to stop asking for messages
stop = False
logged_in = False
console = False


def receive_messages():
    """
    => receive messages from server
    :return: None
    """

    global messages
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode()

            # make sure memory is safe to access
            lock.acquire()
            messages.append(msg)
            lock.release()
        except Exception as e:
            print("[EXCEPTION] ", e)
            break


def send_messages(msg):
    """
    => send messages to server
    :param msg: str
    :return: None
    """

    message = msg.encode("utf8")
    client_socket.send(message)

    # if msg == "/logout":
    #     client_socket.close()


def get_messages():
    """
    => returns a list of str messages
    :return: list[str]
    """

    global messages
    messages_copy = messages[:]

    # make sure memory if safe to access
    lock.acquire()
    messages = []
    lock.release()

    return messages_copy


def disconnect():
    send_messages("{quit}")


def update_messages():
    """
    => updates the local list of messages
    :return: None
    """
    global console
    global stop
    global logged_in

    msgs = []
    run = True
    while run:
        time.sleep(0.1) # update every 1/10 of a second
        new_messages = get_messages() # get any new messages from client
        msgs.extend(new_messages) # add to local list of messages

        for msg in new_messages: # display new messages
            if msg != CLEAR:
                print(msg)    

            if msg == "[SERVER] Correct password.":
                logged_in = True
                stop = True
                time.sleep(1.5)
            
            elif msg == "[SERVER] You have been logged out":
                logged_in = False
                stop = True
                time.sleep(1.5)
            
            elif msg == CLEAR:
                os.system("cls")
            
            elif msg == "{quit}":
                run = False
                break

            elif msg == CONSOLE:
                console = True

  
  
receive_thread = Thread(target = receive_messages)
receive_thread.start()
Thread(target = update_messages).start()

def start_console():
    gui = Console()

def start():

    global stop, console, logged_in

    while True:
        time.sleep(0.5)
        if console == True:
            start_console()
            console = False
        if stop == True:
            stop = False
            time.sleep(2)
        message = input("[COMMAND] ")
        send_messages(message)

start()



