import random
import os.path
import json
import random
import string
import json
import threading

HEADER = 1024
PORT = 1987
FORMAT = 'utf-8'

#Functions

def unpack_dict(imie, nazwisko, haslo, pesel, numer_klienta, saldo):
    return (imie, nazwisko, haslo, pesel, numer_klienta, saldo)

def creating_account_numbers():
    '''we create a list storing unique account numbers'''
    numery_konta = []
    for _ in range(100):
        liczba=''.join(random.choices(string.digits, k=8))
        '''we check if the generated number is already added to our list'''
        if liczba not in numery_konta:
            numery_konta.append(liczba)
    return numery_konta

def save_to_file(dane_konta, nr_konta):
    with open(f'uzytkownicy/{nr_konta}.txt', 'w') as file:
            file.write(json.dumps(dane_konta, indent = 4))
        
def get_file_content(nr_konta):
    with open(f'uzytkownicy/{nr_konta}.txt') as file:
        output=json.loads(file.read())    
    return output

def create_account(imie, nazwisko, haslo, pesel, nr_konta, saldo):
    dane_konta = {"imie": imie, "nazwisko": nazwisko, "haslo": haslo, "pesel": pesel, "numer_klienta": nr_konta, "saldo": saldo}
    save_to_file(dane_konta, nr_konta)

def register(imie, nazwisko, haslo, pesel, saldo):
    numery_klienta = creating_account_numbers()
    numer_klienta = numery_klienta.pop()
    create_account(imie, nazwisko, haslo, pesel, numer_klienta, saldo)
    return numer_klienta

def login(nr_konta, haslo):
    if os.path.isfile(f"uzytkownicy/{nr_konta}.txt"):
        dane_z_pliku = get_file_content(nr_konta)
        if dane_z_pliku["haslo"] == haslo:
            return "Successfully logged in"
        else:
            return "Wrong password!"
    else:
        return "Wrong number of customer account"

def check_saldo(nr_konta):
    dane = get_file_content(nr_konta)
    saldo = dane["saldo"]
    return saldo

def change_saldo(imie, nazwisko, haslo, pesel, numer_klienta, saldo):
    'the function of changing the balance used during the deposit, withdrawal or money transfer'
    dane_konta = {}
    dane_konta['imie'] = imie
    dane_konta['nazwisko'] = nazwisko
    dane_konta['haslo'] = haslo
    dane_konta['pesel'] = pesel
    dane_konta['numer_klienta'] = numer_klienta
    dane_konta['saldo'] = saldo
    with open(f'uzytkownicy/{numer_klienta}.txt', 'w') as file:
        file.write(json.dumps(dane_konta, indent = 4))

def pay_in(nr_konta, kwota_zasilenia):
    imie, nazwisko, haslo, pesel, numer_klienta, saldo=unpack_dict(**get_file_content(nr_konta))
    if kwota_zasilenia > 0:
        saldo = saldo + kwota_zasilenia
        change_saldo(imie, nazwisko, haslo, pesel, numer_klienta, saldo)
        return "The account has been funded"
    elif kwota_zasilenia <= 0:
        return "The top-up amount is too low, please try again with a different amount"
    
def withdraw_money(nr_konta, kwota_wyplaty):
    imie, nazwisko, haslo, pesel, numer_klienta, saldo=unpack_dict(**get_file_content(nr_konta))
    saldo = int(saldo)
    if kwota_wyplaty < saldo:
        saldo = saldo - kwota_wyplaty
        change_saldo(imie, nazwisko, haslo, pesel, numer_klienta, saldo)
        return "Funds have been paid out"
    elif kwota_wyplaty > saldo:
        return "Insufficient funds in the bank account"
    else:
        return "Such funds cannot be withdrawn"

def bank_transfer(senders_account_number, recipients_account_number, liczba_srodkow):
    if recipients_account_number != senders_account_number:
        dane = get_file_content(senders_account_number)
        saldo = int(dane["saldo"])
        liczba_srodkow = int(liczba_srodkow)
        if saldo >= liczba_srodkow:
            if os.path.isfile(f"uzytkownicy/{recipients_account_number}.txt"):
                dane['saldo'] = dane['saldo'] - liczba_srodkow
                save_to_file(dane, senders_account_number)
                dane_odbiorcy = get_file_content(recipients_account_number)
                saldo_odbiorcy = int(dane_odbiorcy["saldo"])
                dane_odbiorcy["saldo"] = liczba_srodkow + saldo_odbiorcy
                save_to_file(dane_odbiorcy, recipients_account_number)
                return "The transfer has been made, you can select operations again."
            else:
                return "The recipient does not exist, you can select operations again."
        else:
            return "Insufficient funds on your account, you can select operations again."
    else:
        return "You cannot send money to your account"

def get_a_message(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        return msg

def enter_to_log(conn):
    conn.send("Enter the account number for logging in: ".encode(FORMAT))
    numer_konta = get_a_message(conn)

    conn.send("Enter the password: ".encode(FORMAT))
    haslo = get_a_message(conn)
    return numer_konta, haslo

def main_registration(conn, addr):
    print(f"[{addr}] The customer has selected registrations.")
    conn.send("Enter your first name: ".encode(FORMAT))
    imie = get_a_message(conn)
    conn.send("The name can only consist of letters. Please try again ".encode(FORMAT))
    conn.send('Enter your surname: '.encode(FORMAT))
    nazwisko = get_a_message(conn)
    conn.send('Enter your password: '.encode(FORMAT))
    password = get_a_message(conn)
    conn.send('Emter your Pesel:'.encode(FORMAT))
    pesel = get_a_message(conn)
    saldo = 0
    print(f"[{addr}] The customer entered the following data: ")
    print(f"""
                Firstname: {imie} 
                Surname: {nazwisko}
                Password: {password}
                Pesel: {pesel}
                Saldo: 0
                """)

    numer_klienta = register(imie, nazwisko, password, pesel, saldo)
    conn.send(f"Your customer number: {numer_klienta}. Please enter 2 to log in".encode(FORMAT))
    print(f"[{addr}] After registration, the customer got the following account number: {numer_klienta}")
    msg = get_a_message(conn)
    if msg == "2":
        main_login(conn,addr, threading)
    else:
        print("The user has decided to stop using of the program")
        exit()

def main_login(conn, addr, threading):
    print(f"[{addr}] The customer chose to login.")
    numer_konta, haslo = enter_to_log(conn)
    wynik_logowania = login(numer_konta, haslo)
    conn.send(wynik_logowania.encode(FORMAT))
    if wynik_logowania == "Successfully logged in":
        print(f"[{addr}] The customer logged in to the account number: {numer_konta}.")
        attr = True
        while attr:
            msg = get_a_message(conn)
            if msg == "1":
                conn.send(f"Your account balance is: {check_saldo(numer_konta)}".encode(FORMAT))
                saldo = check_saldo(numer_konta)
                print(f"[{addr}] {numer_konta} checked the account balance which is {saldo}")
            
            elif msg == "2":
                print(f"[{addr}] {numer_konta} chose the payment to the account.")
                conn.send("Please provide the amount of the payment:".encode(FORMAT))
                msg = get_a_message(conn)
                kwota_zasilenia = int(msg)
                msg_do_klienta = pay_in(numer_konta, kwota_zasilenia)
                conn.send(msg_do_klienta.encode(FORMAT))
                print(f"[{addr}] {numer_konta} the account is credited with the amount {kwota_zasilenia}")
            
            elif msg == "3":
                print(f"[{addr}] {numer_konta} chose to pay out funds")
                conn.send("Please enter your withdrawal amount: ".encode((FORMAT)))
                kwota_wyplaty = int(get_a_message(conn))
                msg_do_klienta = withdraw_money(numer_konta, kwota_wyplaty)
                conn.send(f"{msg_do_klienta}".encode(FORMAT))
                print(f"[{addr}] {numer_konta} withdrawn {kwota_wyplaty} from the account")
            
            elif msg == "4":
                print(f"[{addr}] {numer_konta} have chosen a transfer to another account.")
                conn.send("Please enter the account number to which you want to transfer funds: ".encode(FORMAT))
                numer_konta_odbiorcy = get_a_message(conn)
                conn.send("please provide the amount of the transfer ".encode(FORMAT))
                kwota_przelewu = get_a_message(conn)
                msg_do_klienta = bank_transfer(numer_konta, numer_konta_odbiorcy, kwota_przelewu)
                conn.send(msg_do_klienta.encode(FORMAT))
                print(f"[{addr}] {numer_konta} transfer {kwota_przelewu} to the account {numer_konta_odbiorcy}")

            else:
                print(f"[{addr}] The user has decided to stop using of the program")
                print(f"[Number of active clients] {(threading.activeCount() -1 ) - 1}")
                conn.send("0".encode(FORMAT))
                attr = False
                exit()

