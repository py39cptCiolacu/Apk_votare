from flask import Blueprint, render_template, flash, redirect, request, session
from flask.helpers import url_for
from website.models import Voturi, Participanti
import datetime
from . import db
from .models import Ora
import time

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():

    return render_template("home.html")


@views.route('/voting_public_sala', methods=['GET', 'POST'])
def voting_public_sala():

    part = Participanti.query.all()
    try:
        part = part[-1]
        part = part.participanti
        part = part.split('/')
        m1e1 = part[0]
        m2e1 = part[1]
        m3e1 = part[2]
        m1e2 = part[3]
        m2e2 = part[4]
        m3e2 = part[5]
    except IndexError:
        m1e1 = 'membru 1'
        m2e1 = 'membru 2'
        m3e1 = 'membru 3'
        m1e2 = 'membru 1'
        m2e2 = 'membru 2'
        m3e2 = 'membru 3'


    return render_template("voting_try.html", m1e1=m1e1, m2e1=m2e1, m3e1=m3e1, m1e2=m1e2, m2e2=m2e2, m3e2=m3e2)


@views.route('/voting_public_online', methods=['GET', 'POST'])
def voting_public_online():

    part = Participanti.query.all()
    try:
        part = part[-1]
        part = part.participanti
        part = part.split('/')
        m1e1 = part[0]
        m2e1 = part[1]
        m3e1 = part[2]
        m1e2 = part[3]
        m2e2 = part[4]
        m3e2 = part[5]
    except IndexError:
        m1e1 = 'membru 1'
        m2e1 = 'membru 2'
        m3e1 = 'membru 3'
        m1e2 = 'membru 1'
        m2e2 = 'membru 2'
        m3e2 = 'membru 3'



    return render_template("voting_try.html", m1e1=m1e1, m2e1=m2e1, m3e1=m3e1, m1e2=m1e2, m2e2=m2e2, m3e2=m3e2)


@views.route('/voting_jurat', methods=['GET', 'POST'])
def voting_jurat():

    part = Participanti.query.all()
    try:
        part = part[-1]
        part = part.participanti
        part = part.split('/')
        m1e1 = part[0]
        m2e1 = part[1]
        m3e1 = part[2]
        m1e2 = part[3]
        m2e2 = part[4]
        m3e2 = part[5]
    except IndexError:
        m1e1 = 'membru 1'
        m2e1 = 'membru 2'
        m3e1 = 'membru 3'
        m1e2 = 'membru 1'
        m2e2 = 'membru 2'
        m3e2 = 'membru 3'


    return render_template("voting_try.html", m1e1=m1e1, m2e1=m2e1, m3e1=m3e1, m1e2=m1e2, m2e2=m2e2, m3e2=m3e2)

@views.route('/voting_echipa1', methods=['GET', 'POST'])
def voting_echipa1():

    t = time.localtime()
    now = time.strftime("%H:%M:%S", t)
    now = str(now)

    if 'jurat' in session:
        jurat = session['jurat']
        parola = 'NU'
        ip = 'NU'
    elif 'parola' in session:
        jurat = 'NU'
        parola = session['parola']
        ip = 'NU'
    else:
        jurat = 'NU'
        parola = 'NU'
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

    if jurat != 'NU':
        user_type = 'jurat'
    if parola != 'NU':
        user_type = 'sala'
    if ip != 'NU':
        user_type = 'online'

    verificare = Voturi.query.filter_by(user_type = user_type, ip=ip, parola = parola, jurat = jurat).first()
    if verificare:
        flash("------------------------------> Ai Votat Deja", category='error')
        # session.clear()
        return redirect(url_for('views.results_loading'))
    else:
        vot = Voturi(user_type = user_type, ip=ip, parola = parola, jurat = jurat, alegere = '1', timp =now)
        db.session.add(vot)
        db.session.commit()
        flash("------------------------------> Mulțumim Pentru Vot", category='succes')
        # session.clear()
        return redirect(url_for('views.results_loading'))


@views.route('/voting_echipa2', methods=['GET', 'POST'])
def voting_echipa2():

    t = time.localtime()
    now = time.strftime("%H:%M:%S", t)
    now = str(now)

    if 'jurat' in session:
        jurat = session['jurat']
        parola = 'NU'
        ip = 'NU'
    elif 'parola' in session:
        jurat = 'NU'
        parola = session['parola']
        ip = 'NU'
    else:
        jurat = 'NU'
        parola = 'NU'
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

    if jurat != 'NU':
        user_type = 'jurat'
    elif parola != 'NU':
        user_type = 'sala'
    else:
        user_type = 'online'

    verificare = Voturi.query.filter_by(user_type = user_type, ip=ip, parola = parola, jurat = jurat).first()
    if verificare:
        flash("------------------------------> Ai Votat Deja", category='error')
        # session.clear()
        return redirect(url_for('views.results_loading'))
    else:
        vot = Voturi(user_type = user_type, ip=ip, parola = parola, jurat = jurat, alegere = '2', timp =now)
        db.session.add(vot)
        db.session.commit()
        flash("------------------------------> Mulțumim Pentru Vot", category='succes')
        # session.clear()
        return redirect(url_for('views.results_loading'))


@views.route('/results_loading', methods=['GET', 'POST'])
def results_loading():

    session.clear()

    t = time.localtime()
    now = time.strftime("%H:%M:%S", t)
    now = str(now)

    max_time = Ora.query.all()
    try:
        max_time = max_time[-1]
        max_time = max_time.ora
    except IndexError:
        max_time = "00:00:00"


    if verificare_ora(now) == False:
        return redirect(url_for('views.results'))

    return render_template("results_loading.html", x= max_time)

@views.route('/results', methods=['GET', 'POST'])
def results():

    session.clear()

    t = time.localtime()
    now = time.strftime("%H:%M:%S", t)
    now = str(now)

    voturi_public_sala = Voturi.query.filter_by(user_type='sala').all()
    voturi_public_online = Voturi.query.filter_by(user_type = 'online').all()
    voturi_jurat = Voturi.query.filter_by(user_type = 'jurat').all()

    rezultat_echipa1_public = 0
    rezultat_echipa2_public = 0
    rezultat_echipa1_jurati = 0
    rezultat_echipa2_jurati = 0
    nr_voturi_public = 0
    nr_voturi_jurati = 0

    for vps in voturi_public_sala:
        if vps.alegere == '1' and verificare_ora(vps.timp) == True:
            rezultat_echipa1_public += 1
            nr_voturi_public += 1
        elif verificare_ora(vps.timp) == True:
            rezultat_echipa2_public +=1
            nr_voturi_public += 1

    for vpo in voturi_public_online:
        if vpo.alegere == '1'and verificare_ora(vpo.timp) == True:
            nr_voturi_public += 1
            rezultat_echipa1_public += 1
        elif verificare_ora(vpo.timp) == True:
            rezultat_echipa2_public +=1
            nr_voturi_public += 1

    for vj in voturi_jurat:
        nr_voturi_jurati += 1
        if vj.alegere == '1':
            rezultat_echipa1_jurati += 1
        else:
            rezultat_echipa2_jurati += 1

    try:
        rp1 = (rezultat_echipa1_public/nr_voturi_public)
        rp1 = round(rp1,2) * 50
    except ZeroDivisionError:
        rp1 = 0.0


    try:
        rj1 = (rezultat_echipa1_jurati/nr_voturi_jurati)
        rj1 = round(rj1,2) * 50
    except ZeroDivisionError:
        rj1 = 0.0

    try:
        rp2 = (rezultat_echipa2_public/nr_voturi_public)
        rp2 = round(rp2,2) * 50
    except ZeroDivisionError:
        rp2 = 0.0

    try:
        rj2 = (rezultat_echipa2_jurati/nr_voturi_jurati)
        rj2 = round(rj2,2) * 50
    except ZeroDivisionError:
         rj2 = 0.0

    rt1 = rj1+rp1
    rt2 = rj2+rp2

    return render_template("results.html", rj1=rj1, rp1=rp1, rt1=rt1, rj2=rj2, rp2=rp2, rt2=rt2 )

def verificare_ora(vot_time):

    max_time = Ora.query.all()
    try:
        max_time = max_time[-1]
        max_time = max_time.ora
    except IndexError:
        max_time = "00:00:00"


    ora_vot = (int(vot_time[0:2])+2)%24
    min_vot = (int(vot_time[3:5])+2)%24
    sec_vot = (int(vot_time[6:8])+2)%60
    ora_max = (int(max_time[0:2])+2)%60
    min_max = (int(max_time[3:5])+2)%60
    sec_max = (int(max_time[6:8])+2)%60


    vot_time = datetime.time(ora_vot, min_vot, sec_vot)
    max_time = datetime.time(ora_max, min_max, sec_max)

    if vot_time <= max_time:
        return True
    else:
        return False
