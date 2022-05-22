import socket as s
import threading

'''Tworzymy zmienne z naszym ip oraz portem
   Funkcja gethostbyname() zwraca nam nasz adres ip''' 
HOST = s.gethostbyname(s.gethostname())
PORT = 33000
'''Buffer jest to ilosc bitow z jaką odbieramy wiadomość.
   Jezeli przekroczymy buffer po prostu utnie nam wiadomosc.'''
BUFFER = 1024
MSG_DISCONNECT = 'KONIEC'
def handle_client(conn, addr):
   print(f'Nowe połączenie : {addr}')

   connected = True
   while connected:
      msg = conn.recv(BUFFER).decode('utf8')
      if msg ==MSG_DISCONNECT:
         connected = False

      print(f'[{addr}] {msg}')
      msg = f"Otrzymana wiadomosc: {msg}"
      conn.send(msg.encode('utf8'))
   
   conn.close()

def main():

   print('Uruchomienie serwera')

   '''tworzymy obiekt socket z argumentami - AF-INET(jest to rodzina adresow ipv4)
      oraz SOCK_STREAM(jes to strumien przesylu danych dla socketa)'''
   server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)

   '''funckja bind() łączy gniazdo z jego adresem lokalnym.
   Jako argument dajemy krotke(tuple), ktora przechowuje nasze IP oraz PORT '''
   server_socket.bind((HOST, PORT))

   '''Dzieki tej funkcji serwer nasluchuje przychodzacych polaczen.'''
   server_socket.listen(2)
   print(f'Serwer nasluchuje na {HOST}:{PORT}')

   while True:
      '''Dzieki funkcji accept(), akceptujemy przychodzace polaczenie od klienta.
         To polaczenie przypisujemy do zmiennej 'clien_socket' natomiast adres do
         zmiennej 'address' '''
      client_socket, address = server_socket.accept()
      thread = threading.Thread(target=handle_client, args=(client_socket, address))
      thread.start()
      print(f'AKTYWNE POŁĄCZENIA : {threading.active_count() - 1}')


if __name__ == '__main__':
   main()