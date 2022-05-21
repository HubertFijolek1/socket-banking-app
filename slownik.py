import random
import string
import json
from os import listdir
from sys import exit

def unpack_dict(login, imie, nazwisko, pesel, nr_konta, saldo):
    return (login, imie, nazwisko, pesel, nr_konta, saldo)

def jakie_mamy_nr_konta():
    print('\nOto spis uzytkownikow oraz ich kont, ktore mamy w systemie.')
    dirs = listdir('uzytkownicy/')
    for file in dirs:
        with open(f'uzytkownicy/{file}') as file:
            js=json.loads(file.read())
            login_nr_konta = {}
            for i in js:
                if i == 'login':
                    login_nr_konta[js[i]] =  js['nr_konta']  
                    print(login_nr_konta)  
                
def tworzenie_konta(numery_konta):
    login2 = {}
    login2['login'] = input('Podaj nazwę użytkownika: ')
    login2['imie'] = input('Podaj swoje imię: ')
    login2['nazwisko'] = input('Podaj swoje nazwisko: ')
    login2['pesel'] = input('Podaj swój PESEL: ')
    login2['nr_konta'] = numery_konta.pop()
    login2['saldo'] = 0
    with open(f'uzytkownicy/{login2["login"]}.txt', 'w') as file:
        file.write(json.dumps(login2, indent = 4))
        login, imie, nazwisko, pesel, nr_konta, saldo=unpack_dict(**login2)
    print('\nBrawo! Wlasnie utworzyles konto w naszym serwisie. Oto twoje dane: \n')
    print(f'Login: {login} \nImie: {imie} \nNazwisko: {nazwisko} \nPESEL: {pesel}')
    print(f'Wygenerowany unikalny nr konta: {nr_konta} \nSaldo: {saldo}')

    konto(login, imie, nazwisko, pesel, nr_konta, saldo)

def zmiana_salda(login, imie, nazwisko, pesel, nr_konta, saldo):
    login2 = {}
    login2['login'] = login
    login2['imie'] = imie
    login2['nazwisko'] = nazwisko
    login2['pesel'] = pesel
    login2['nr_konta'] = nr_konta
    login2['saldo'] = saldo
    with open(f'uzytkownicy/{login}.txt', 'w') as file:
        file.write(json.dumps(login2, indent = 4))
        login, imie, nazwisko, pesel, nr_konta, saldo=unpack_dict(**login2)



def konto(login, imie, nazwisko, pesel, nr_konta, saldo):
    wybor = input('\nCo zamierzasz zrobic? \n0 - Wyjdz \n1 - przelew na inne konto \n2 - wyplacenie środków \n3 - dokonanie wpłaty \n4 - sprawdzenie stanu konta\n5 - sprawdzenie danych uzytkownika\n')
    while True:
        if wybor =='0':
            print("Milego dnia :)")
            exit()
        elif wybor =='1':
            print(f'{login} twój aktualny stan konta wynosi {saldo}zł. ')
            if saldo == 0:
                print("Niestety nie masz wystarczających srodkow na koncie, aby przelac komus pieniądze.")
            else:
                jakie_mamy_nr_konta()
                uzytkownik2 = input('Komu chcesz przesłać pieniądze?')
                dirs = listdir('uzytkownicy/')
                lista_uzytkownikow = []
                for file in dirs:
                    lista_uzytkownikow.append(file[:-4])                  
                if uzytkownik2 not in lista_uzytkownikow:
                    print('\nNiestety nie mamy takiego uzytkownika w naszej bazie uzytkownikow.\n')
                    konto(login, imie, nazwisko, pesel, nr_konta, saldo)
                if login == uzytkownik2:
                    print('Nie możesz przelać pieniądzy samemu sobie!')
                    konto(login, imie, nazwisko, pesel, nr_konta, saldo)
                else:
                    try:
                        przelew = int(input('Ile pieniedzy chcesz przelac?\n'))
                        if przelew <= 0:
                            print('Przelanie takiej ilości pieniędzy jest niemożliwe')
                    except:
                        print('Prosze nastepnym razem podaj liczbe :)')
                        konto(login, imie, nazwisko, pesel, nr_konta, saldo)    
                    if przelew > saldo :
                        print('Niestety, nie masz wystarczajacych srodkow na koncie')
                        konto(login, imie, nazwisko, pesel, nr_konta, saldo)
                    elif przelew <= saldo and przelew > 0:
                        saldo = saldo - przelew
                        zmiana_salda(login, imie, nazwisko, pesel, nr_konta, saldo)
                        print(f'Brawo! Udalo ci sie pomyslnie przelac pieniądze. Twoj obecny stan konta to {saldo}zł')
                        with open(f'uzytkownicy/{uzytkownik2}.txt') as file:
                            js=json.loads(file.read())    
                            login2, imie2, nazwisko2, pesel2, nr_konta2, saldo2=unpack_dict(**js)
                            saldo2 = saldo2 + przelew
                            zmiana_salda(login2, imie2, nazwisko2, pesel2, nr_konta2, saldo2)
                            print(f'\n{login2} pomyślnie otrzymał twój przelew. Jego stan konta zwiększył się o {przelew}zł')
                        konto(login, imie, nazwisko, pesel, nr_konta, saldo)
        elif wybor == '2':
            print(f'{login} twój aktualny stan konta wynosi {saldo}zł. ')
            try:
                wyplata = int(input('Ile pieniedzy chcesz wyplacic? (0 - Wyjdz)\n'))
            except:
                print('Prosze nastepnym razem podaj liczbe :)')
                konto(login, imie, nazwisko, pesel, nr_konta, saldo)
                exit()
            if wyplata > saldo :
                print('Niestety, nie masz wystarczajacych srodkow na koncie')
                konto(login, imie, nazwisko, pesel, nr_konta, saldo)
            elif wyplata < saldo and wyplata > 0:
                saldo = saldo - wyplata
                zmiana_salda(login, imie, nazwisko, pesel, nr_konta, saldo)
                print(f'Brawo! Udalo ci sie wyplacic pomyslnie pieniadze. Twoj obecny stan konta to {saldo}zł')
                konto(login, imie, nazwisko, pesel, nr_konta, saldo)
            elif wyplata < 0:
                print('Nie można wypłacić mniej niż zero ;)')
            else:
                konto(login, imie, nazwisko, pesel, nr_konta, saldo)
        elif wybor == '3':
            print(f'{login} twój aktualny stan konta wynosi {saldo}zł. ')
            try:
                wplata = int(input('Ile pieniedzy chcesz wplacic? (0 - Wyjdz)\n'))
            except:
                print('Prosze nastepnym razem podaj liczbe :)')
                konto(login, imie, nazwisko, pesel, nr_konta, saldo)
            if wplata > 0:
                saldo = saldo + wplata
                zmiana_salda(login, imie, nazwisko, pesel, nr_konta, saldo)
                print(f'Brawo! Udalo ci sie wplacic pomyslnie pieniadze. Twoj obecny stan konta to {saldo}zł')
                konto(login, imie, nazwisko, pesel, nr_konta, saldo)
            elif wplata < 0:
                print('Nie można wpłacić mniej niż zero ;)')
            else:
                konto(login, imie, nazwisko, pesel, nr_konta, saldo)
        elif wybor == '4':
            print(f'{login} twój aktualny stan konta wynosi {saldo}zł. ')
            konto(login, imie, nazwisko, pesel, nr_konta, saldo)
        elif wybor == '5':
            print('Oto twoje dane: \n')
            print(f'Login: {login} \nImie: {imie} \nNazwisko: {nazwisko} \nPESEL: {pesel}')
            print(f'Wygenerowany unikalny nr konta: {nr_konta} \nSaldo: {saldo}zł')
            konto(login, imie, nazwisko, pesel, nr_konta, saldo)  
        else:
            print('Stosuj sie do instrukcji :)')
            konto(login, imie, nazwisko, pesel, nr_konta, saldo)
def tworzenie_nr_kont():
    '''tworzymy liste przechowujące unikalne numery konta'''
    numery_konta = []
    for i in range(100):
        liczba=''.join(random.choices(string.digits, k=8))
        '''sprawdzamy czy wygenerowana liczba nie jest juz dodana do naszej listy'''
        if liczba not in numery_konta:
            numery_konta.append(liczba)
    return numery_konta

def main():
    numery_konta=tworzenie_nr_kont()
    lista = [f[:-4] for f in listdir('uzytkownicy/')]
    login = input('Podaj nazwe uzytkownika: ')
    if login in lista:
        print(f'\nWitaj {login}. Oto twoje dane:')
        with open(f'uzytkownicy/{login}.txt') as file:
            js=json.loads(file.read())
            for i in js:
                print(i +": " +  str(js[i]))
            login, imie, nazwisko, pesel, nr_konta, saldo=unpack_dict(**js)
            konto(login, imie, nazwisko, pesel, nr_konta, saldo)   
    else:
        while True:
            odp = input('Wygląda na to, że nie masz jeszcze u nas konta. \nCzy chcesz je stworzyć? tak/nie : ')
            if odp == 'tak':
                tworzenie_konta(numery_konta)    
            elif odp == 'nie':
                print('No dobra to nara.')
            else:
                print("Udziel poprawnej odpowiedzi :) ")

if __name__ == "__main__":
    main()