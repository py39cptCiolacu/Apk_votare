
from os import error
from flask import Blueprint, render_template, request, redirect, flash, url_for, session, Flask
from sqlalchemy.sql.expression import select
from . import db
from .models import Ora, Voturi
from datetime import datetime
import contextlib
from sqlalchemy import MetaData


auth = Blueprint('auth', __name__)

#Se genereaza n ID-uri si parole (n=nr de jurati)
@auth.route('/login_jury', methods=['GET', 'POST'])
def login_jury():

    jurati = {"NumePrenume1" : "parola1", "NumePrenume2": "parola2", "NumePrenume3": "parola3"} 

    if request.method == 'POST':
            id_juriu = request.form.get('id_juriu')
            parola_jurat = request.form.get('password')
            if id_juriu in jurati and jurati[id_juriu] == parola_jurat:
                session['jurat'] = id_juriu
                return redirect(url_for('views.voting_jurat'))
            else:
                flash('Incorrect password, try again.', category='error')

    return render_template("login_jury.html")


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
            elif parola == "adminSetareTimp":
                return redirect(url_for('auth.adminCPT'))
            elif parola == "adminResetareBaza":
                return redirect(url_for('auth.adminCPT2'))
            else:
                flash('Parola incorecta, incearca din nou', category='error')

    return render_template("login_public.html")

@auth.route('/adminCPT', methods = ['GET', 'POST'])
def adminCPT():

    #voi avea un buton pentru a afisa rezultatele
    #voi seta timpul maxim de votare

    if request.method == 'POST':
        db.session.add(Ora(ora = request.form.get('ora')))
        db.session.commit()

    max_time = Ora.query.all()

    try:
        max_time = max_time[-1]
        max_time = max_time.ora
    except IndexError:
        max_time = "nu ai setat nimic"
 

    return render_template('admin.html', x=max_time)


@auth.route('/adminCPT2', methods = ['GET', 'POST'])
def adminCPT2():

    if request.method == 'POST':
        resetare = request.form.get('resetare')
        if resetare == "RESETEAZA-BAZA":
            Voturi.query.delete()
            db.session.commit()
        else:
            flash('Ai introdus gresit', category='error')    

    return render_template('admin2.html')

