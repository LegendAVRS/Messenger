from Start_UI import Start_UI
import sys
from UI import UI

sys.path.insert(0, "D:\Python\Messenger\Messenger-beta\client")
from client import Client

new_client = Client()

start_ui = Start_UI(new_client)
if new_client.logged_in:
    ui = UI(new_client)
