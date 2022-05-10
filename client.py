import socket as s

'''tworzymy zmienne przechowujace ip oraz port zeby polaczyc sie z serwerem'''
HOST = s.gethostbyname(s.gethostname())
PORT = 33000

'''Bufer jest to ilosc bitow z jaką odbieramy wiadomość.
   Jezeli przekroczymy bufer po prostu utnie nam wiadomosc.'''
BUFFER = 1024

MSG_DISCONNECT = 'KONIEC'


def main():
   client = s.socket(s.AF_INET, s.SOCK_STREAM)
   client.connect((HOST, PORT))
   print(f'Klient połączył się z serwerem ({HOST}:{PORT})')

   connected = True
   while connected:
      msg = input("> ")
      client.send(msg.encode('utf8'))
      
      if msg == MSG_DISCONNECT:
         connected = False
      else:
         msg = client.recv(BUFFER).decode('utf8')
         print(f'Serwer: {msg}')
if __name__ == "__main__":
   main()

# '''tworzymy obiekt socket z argumentami - AF-INET(jest to rodzina adresow ipv4)
#    oraz SOCK_STREAM(jes to strumien przesylu danych dla socketa)'''
# client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)

# '''connect() sluzy do laczenia ze zdalnym adresem serwera'''
# client_socket.connect((HOST,PORT))

# '''tworzymy zmienna ktora bedzie przechowywac imie klienta.
#    Informacje przekazywane przez sockety trzeba zakodowac w jakims formacie.
#    W naszym przypadku jest to utf-8'''
# name = input('Twoje imie: ').encode("utf8")

# '''Wysylamy nazwe klienta do serwera'''
# client_socket.send(name)

# '''Otrzymujemy wiadomosc zwrotna od serwera'''
# print(client_socket.recv(BUFFER).decode("utf8"))