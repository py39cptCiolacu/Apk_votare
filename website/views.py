from flask import Blueprint, render_template, flash, redirect, request, session
from flask.helpers import url_for
from flask.scaffold import _matching_loader_thinks_module_is_package
from website.models import Voturi
import datetime
from . import db 
from .models import Ora

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():

    return render_template("home.html")


@views.route('/voting_public_sala', methods=['GET', 'POST'])
def voting_public_sala():   

    now = str(datetime.datetime.now().time())

    if 'parola' in session:
        parola = session['parola']


    if request.method == 'POST':
        alegere = request.form['echipeA']
        vot = Voturi(user_type='sala', alegere=alegere, parola=parola, timp=now) #aici pun si parola

        verificare = Voturi.query.filter_by(parola=parola).first()
        if verificare and verificare != 'NU':
            flash("AI VOTAT DEJA", category='error')
        else:
            db.session.add(vot)
            db.session.commit()
            flash("GATA AI VOTAT")
        if verificare_ora(now) == False:
            return redirect(url_for('views.results'))
        else:  
            return redirect(url_for('views.results_loading'))

    return render_template("voting.html")

    
@views.route('/voting_public_online', methods=['GET', 'POST'])
def voting_public_online():

    now = str(datetime.datetime.now().time())

    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

    if request.method == 'POST':
        alegere = request.form['echipeA']

        vot = Voturi(user_type='online', alegere = alegere, ip=ip, timp=now) 
        verificare = Voturi.query.filter_by(ip=ip).first()
        if verificare and verificare != 'NU':
            flash("AI VOTAT DEJA", category='error')
        else:
            db.session.add(vot)
            db.session.commit()
            flash("GATA AI VOTAT")
        if verificare_ora(now) == False:
            return redirect(url_for('views.results'))
        else:  
            return redirect(url_for('views.results_loading'))

    return render_template("voting.html")


@views.route('/voting_jurat', methods=['GET', 'POST'])
def voting_jurat():

    now = str(datetime.datetime.now().time())

    if 'jurat' in session:
        jurat = session['jurat']


    if request.method == 'POST':
        alegere = request.form['echipeA']

        vot = Voturi(user_type='jurat', alegere = alegere, jurat = jurat, timp=now)
        verificare = Voturi.query.filter_by(jurat=jurat).first()
        if verificare and verificare != 'NU':
            flash("AI VOTAT DEJA", category='error')
        else:
            db.session.add(vot)
            db.session.commit()
            flash("GATA AI VOTAT")
        if verificare_ora(now) == False:
            return redirect(url_for('views.results'))
        else:  
            return redirect(url_for('views.results_loading'))


    return render_template("voting.html")

@views.route('/results_loading', methods=['GET', 'POST'])
def results_loading():

    now = str(datetime.datetime.now().time())

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

    now = str(datetime.datetime.now().time())

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
        nr_voturi_public += 1
        if vps.alegere == '1' and verificare_ora(vps.timp) == True:
            rezultat_echipa1_public += 1
        elif verificare_ora(vps.timp) == True:
            rezultat_echipa2_public +=1

    for vpo in voturi_public_online:
        nr_voturi_public += 1
        if vpo.alegere == '1'and verificare_ora(vpo.timp) == True:
            rezultat_echipa1_public += 1
        elif verificare_ora(vpo.timp) == True:
            rezultat_echipa2_public +=1

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

    vot_timeL = vot_time.split(":")
    max_timeL = max_time.split(":")

    vot_time = datetime.time(int(vot_time[0:2]), int(vot_time[3:5]), int(vot_time[6:8]))
    max_time = datetime.time(int(max_time[0:2]), int(max_time[3:5]), int(max_time[6:8]))

    if vot_time <= max_time:
        return True
    else:
        return False  