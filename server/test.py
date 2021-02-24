import info_database as db
from users import User
from threading import Thread
import os
import time

dic = {}

dic[1] = 'a'
dic[2] = 'b'
dic[3] = 'c'
print(dic)

dic.pop(4)
print(dic)

# try:
#     dic.pop(4)
# except Exception as e:
#     print(e)