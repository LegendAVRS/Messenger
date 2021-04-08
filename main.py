from Start_UI import Start_UI
import sys
from UI import UI

# path leading to client file
client_path = __file__[:-7] + "Messenger-beta\\client\\"

sys.path.insert(0, client_path)
from client import Client

new_client = Client()

start_ui = Start_UI(new_client)
if new_client.logged_in:
    ui = UI(new_client)
