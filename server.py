import threading
import socket
from functions import *


HEADER = 1024
PORT = 1987
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

def handle_client(conn, addr):
    print(f"[New connection with:] {addr}")
    connected = True
    while connected:
        
        msg = get_a_message(conn)
        if msg == "0":
            connected = False
        print(f"[{addr}] {msg}")                  
        if msg == "1":
            main_registration(conn, addr)
        if msg == "2":
            main_login(conn, addr, threading)
        else:
            connected = False
        
    conn.close()
    print(f"[Number of active clients] {(threading.activeCount() -1 ) - 1}")

def start():
        server.listen()
        print(f"[server is listening on:] {SERVER}")
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[Number of active clients] {threading.activeCount() -1 }")
    
start()