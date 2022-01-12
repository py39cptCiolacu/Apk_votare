from functools import cache
from flask import Blueprint, render_template, request, redirect, flash, url_for, session, Flask
from . import db


auth = Blueprint('auth', __name__)

#Se genereaza n ID-uri si parole (n=nr de jurati)
@auth.route('/login_jury', methods=['GET', 'POST'])
def login_jury():

    jurati = {"NumePrenume1" : "parola1", "NumePrenume2": "parola2"} 

    if request.method == 'POST':
            id_juriu = request.form.get('id_juriu')
            parola_jurat = request.form.get('password')
            if id_juriu in jurati and jurati[id_juriu] == parola_jurat:
                session['jurat'] = id_juriu
                return redirect(url_for('views.voting_jurat'))
            else:
                flash('Incorrect password, try again.', category='error')

    return render_template("login_jury.html")


#Publicul care este pe live. Se va retine ip-ul intr o baza de date, astfel putand sa voteze doar o singura data
@auth.route('/login_public_online', methods = ['GET', 'POST'])
def login_public_online():
    
    #redirectionarea se face din html

    return render_template("login_public_online.html")


# Publicul care este in sala. Va primi parola la intrare in sala. Se vor genera ininte un numar n de parole
# plus una speciala pentru orice eventualitate (de preferat n > nr de persoane din sala)
@auth.route('/login_public', methods = ['GET', 'POST'])
def login_public():

    parole = open('parole.txt', 'r')
    content_parole = parole.read() #parolele se pot pune intr o baza de date

    if request.method == 'POST':
            parola = request.form.get('password_public')
            if parola in content_parole:
                session['parola'] = parola
                return redirect(url_for('views.voting_public_sala'))
            elif parola == "suntADMIN89":
                return redirect(url_for('auth.adminCPT'))
            else:
                flash('Parola incorecta, incearca din nou', category='error')

    return render_template("login_public.html")

@auth.route('/adminCPT', methods = ['GET', 'POST'])
def adminCPT():

    #voi avea un buton pentru a afisa rezultatele
    #voi seta timpul maxim de votare

    if request.method == 'POST':
        ora = request.form.get('ora')
        session['ora'] = ora

    return render_template('admin.html')
