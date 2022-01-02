from flask import Blueprint, render_template, request, redirect, flash, url_for, session
from .models import Ip
from . import db
import time
import sys

auth = Blueprint('auth', __name__)

#Se genereaza n ID-uri si parole (n=nr de jurati)
@auth.route('/login_jury', methods=['GET', 'POST'])
def login_jury():

    jurati = {"NumePrenume1" : "parola1", "NumePrenume2": "parola2"} #se pot pune intr o baza de date

    if request.method == 'POST':
            id_juriu = request.form.get('id_juriu')
            parola_jurat = request.form.get('password')

            if id_juriu in jurati and jurati[id_juriu] == parola_jurat:
                return redirect(url_for('views.voting_jurat'))
            else:
                flash('Incorrect password, try again.', category='error')

    return render_template("login_jury.html")


#Publicul care este pe live. Se va retine ip-ul intr o baza de date, astfel putand sa voteze doar o singura data
@auth.route('/login_public_online', methods = ['GET', 'POST'])
def login_public_online():

    # verificam daca nu e in baza de date
    # daca nu e, poti trece la votat, si apoi il adaugam
    # daca este, nu poti trece la votat 

    # if request.method == 'POST':
    #     return redirect(url_for('views.voting_public'))

    # curr_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    # session['ip_address'] = curr_ip
    # curr_voter = Ip.query.filter_by(ip_address=curr_ip).first()
    # if curr_voter:
    #     flash("Ai votat deja")
    # else:
    #     return redirect("views.voting_public")

    return render_template("login_public_online.html")


# Publicul care este in sala. Va primi parola la intrare in sala. Se vor genera ininte un numar n de parole
# plus una speciala pentru orice eventualitate (de preferat n > nr de persoane din sala)
@auth.route('/login_public', methods = ['GET', 'POST'])
def login_public():

    parole = open('parole.txt', 'r')
    content_parole = parole.read() #parolele se pot pune intr o baza de date

    parole_folosite = []

    if request.method == 'POST':
            password_public = request.form.get('password_public')

            if password_public in content_parole and password_public not in parole_folosite:
                parole_folosite += password_public
                return redirect(url_for('views.voting_public'))
            else:
                flash('Incorrect password, try again.', category='error')

    return render_template("login_public.html")
