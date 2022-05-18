import random
import string
import json
from os import listdir

'''tworzymy liste przechowujące unikalne numery konta'''
numery_konta = []
for i in range(100):
    liczba=''.join(random.choices(string.digits, k=8))
    '''sprawdzamy czy wygenerowana liczba nie jest juz dodana do naszej listy'''
    if liczba not in numery_konta:
        numery_konta.append(liczba)

lista = [f[:-4] for f in listdir('uzytkownicy/')]

login = input('Podaj nazwe uzytkownika: ')
if login in lista:
    print(f'\noWitaj {login}. Oto twoje dane:')
    with open(f'uzytkownicy/{login}.txt') as file:
        js=json.loads(file.read())
        for i in js:
            print(i +": " +  str(js[i]))
        wybor = input('\nCo zamierzasz zrobic?  \n1 - przelew na inne konto (jeśli ma środki i nr konta docelowego istnieje  \n2 - wyplacenie środków \n3 - dokonanie wpłaty \n4 - sprawdzenie stanu konta')
        if wybor == 1:
            # przelew na inne konto (jeśli ma środki i nr konta docelowego istnieje),
            pass
        if wybor == 2:
            pass
            # wypłacić środki (jeśli są dostępne),
        if wybor == 3:
            pass
            # dokonać wpłaty (po prostu zwiększa saldo),
        if wybor == 4:
            pass
            ## sprawdzić stan konta (czyli odczytać saldo).
            
else:
    odp = input('Wygląda na to, że nie masz jeszcze u nas konta. \
    Czy chcesz je stworzyć? tak/nie : ')
    if odp == 'tak':
        login2 = {}
        login2['login'] = input('Podaj nazwę użytkownika: ')
        login2['imie'] = input('Podaj swoje imię: ')
        login2['nazwisko'] = input('Podaj swoje nazwisko: ')
        login2['PESEL'] = input('Podaj swój PESEL: ')
        login2['nr_konta'] = numery_konta.pop()
        login2['saldo'] = 0
        with open(f'uzytkownicy/{login}.txt', 'w') as file:
            file.write(json.dumps(login2, indent = 4))
    elif odp == 'nie':
        print('No dobra to nara.')

