from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
import sys
import os


HOST = "localhost"
PORT = 5050
ADDR = (HOST, PORT)
BUFSIZ = 512


client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)
lock = Lock()


class Client:
    # COMMAND
    CLEAR = "/clear"
    CONSOLE = "/console"

    # MARK
    ERROR = "ERROR"
    CODE_NAME = "#NAME#"

    # SERVER'S COMMAND
    password_instruction = (
        "Insert and confirm password with [/pwd <password> <password>]"
    )

    # Boolean
    stop = False
    logged_in = False
    console = False
    close = False
    pwd_confirm = False

    # Variables
    messages = []
    UI_messages = []

    this_name = "You"

    # cmdConsole = CommandConsole()

    def __init__(self):
        # receive_thread = Thread(target=self.receive_messages)
        # receive_thread.start()
        update_thread = Thread(target=self.update_messages, daemon=True)
        update_thread.start()

    def send_messages(self, msg):
        """
        => send messages to server
        :param msg: str
        :return: None
        """

        message = msg.encode("utf8")
        client_socket.send(message)

        # if msg == "/logout":
        #     client_socket.close()

    # Changed
    def receive_messages(self):
        """
        => receive messages from server
        :return: None
        """

        try:
            msg = client_socket.recv(BUFSIZ).decode()
            # make sure memory is safe to access
            lock.acquire()
            self.messages.append(msg)
            lock.release()
            return msg
        except Exception as e:
            print("[EXCEPTION in RECEIVE] ", e)
            return

    def get_messages(self):
        """
        => returns a list of str messages
        :return: list[str]
        """

        messages_copy = self.messages[:]

        # make sure memory if safe to access
        lock.acquire()
        self.messages = []
        lock.release()

        return messages_copy

    def disconnect(self):
        self.send_messages("{quit}")

    def update_messages(self):
        """
        => updates the local list of messages
        :return: None
        """

        msgs = []
        run = True
        while run:

            if self.close == True:
                return

            time.sleep(0.1)  # update every 1/10 of a second
            new_messages = self.get_messages()  # get any new messages from client
            msgs.extend(new_messages)  # add to local list of messages

            for msg in new_messages:  # display new messages
                # print(msg)

                if self.close == True:
                    return

                self.UI_messages.append(msg)

                if msg == self.ERROR:
                    messagebox.showwarning(title="Warning", message=self.ERROR)
                    continue

                if len(msg) > 6 and msg[:6] == self.CODE_NAME:
                    self.this_name = msg[6:]
                    # self.cmdConsole.this_name = self.this_name
                    continue

                type = 1

                if msg[0] == "!":  # type with name
                    type = 2

                elif msg[0] == "?":  # type with no name
                    type = 3

                if msg != self.CLEAR:
                    if type == 2:
                        msg = msg[1:]
                        name = msg.split()[0]
                        msg = msg[len(name) + 1 :] + "\n"
                        # self.cmdConsole.InsertMessage(msg, 2, name)

                    elif type == 3:
                        msg = msg[1:]
                        # self.cmdConsole.InsertMessage(msg, 3)

                if msg == "Correct password.":
                    self.logged_in = True
                    self.stop = True
                    time.sleep(1.5)

                elif msg == "You have been logged out":
                    self.logged_in = False
                    self.stop = True
                    time.sleep(1.5)

                elif msg == "{quit}":
                    run = False
                    break

                elif msg == self.CONSOLE:
                    self.console = True

                elif msg == self.password_instruction:
                    print("yes")
                    self.pwd_confirm = True

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.close = True
            client_socket.close()
            # self.cmdConsole.root.destroy()

    # def start(self):

    # self.cmdConsole.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    # self.cmdConsole.root.mainloop()


# start()
