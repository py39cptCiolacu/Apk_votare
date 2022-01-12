import random

litere = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
        'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
        'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
cifre = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

def generator():
    parole = open('parole.txt', 'w+')

    numar_parole =  20

    parola = ''
    for i in range(numar_parole):
        for j in range(5):
            parola += random.choice(litere)
        for j in range(3):
            parola += random.choice(cifre)
        
        parole.write(parola + "\n")
        parola = ''
    
    return "GATA PAROLELE"

generator()