import socket
from functions import *
from sys import exit

welcome_menu = """Welcome to the best bank. How can i help you?
    0 - Exit(Wyjscie)
    1 - Sign Up(Zarejestruj sie)
    2 - Sign In(Zaloguj sie) 
    """

client_menu = """Select what you want to do:
    0 - Disconnect
    1 - Bank balance 
    2 - Pay in money
    3 - Withdraw money
    4 - Tranfer money to another account 
    """


FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "0"
HEADER = 1024
PORT = 1987
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
logged_in = False



client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    msg_server = client.recv(2048).decode(FORMAT)
    print(msg_server)
    if msg_server == "Successfully logged in":
        print(client_menu)
    
disconnect = True

print(welcome_menu)
while  disconnect:
    
    msg = input(">>>:")
    if msg == "0":
        disconnect = False
        send("The user has decided to stop using of the program")
        exit()
    else:
        send(msg)
