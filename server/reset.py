import groupchat_store
import groupmem_store
import groupname_store
import chat_store
import info_database

import os

# xóa mọi tài khoản
info_database.delete_all()

# xóa mọi cuộc hội thoại
path = __file__[:-8] + "client_chat"
for f in os.listdir(path):
    os.remove(os.path.join(path, f))

# xóa tên các nhóm
groupname_store.delete_all()

# xóa các đoạn chat và các thành viên của các nhóm
path = __file__[:-8] + "group_chat"
for f in os.listdir(path):
    os.remove(os.path.join(path, f))