import info_database as db
from users import User
from threading import Thread

def function():
    x = int(input("Enter a number: "))
    if x < 0:
        print("Cannot insert negative numbers")
        function()
        return 0
    return x


Thread(target=function).start()

