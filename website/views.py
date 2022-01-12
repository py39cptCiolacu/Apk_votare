from flask import Blueprint, render_template, flash, redirect, request, session
from flask.helpers import url_for
from flask.scaffold import _matching_loader_thinks_module_is_package
from website.models import Voturi
from datetime import datetime
from . import db 

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():

    if 'ora' in session:
        ora = session['ora']
    else:
        ora = "00:00:00"

    return render_template("home.html", x=ora)


@views.route('/voting_public_sala', methods=['GET', 'POST'])
def voting_public_sala():   

    now = str(datetime.now().time())

    if 'parola' in session:
        parola = session['parola']

    #cumva el aici trebuie sa ajunga cu parola cu care s a logat ca sa o pot pasa bazei de data
    #si sa o puna ca folosita

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

    now = str(datetime.now().time())
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

    now = str(datetime.now().time())
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


    return render_template("voting.html",x=now)

@views.route('/results_loading', methods=['GET', 'POST'])
def results_loading():
    now = str(datetime.now().time())

    if 'ora' in session:
        ora = session['ora'] 

    if verificare_ora(now) == False:
        return redirect(url_for('views.results'))

    return render_template("results_loading.html", x= ora)

@views.route('/results', methods=['GET', 'POST'])
def results():

    now = str(datetime.now().time())

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
        if vj.alegere == '1' and verificare_ora(vj.timp) == True:
            rezultat_echipa1_jurati += 1
        elif verificare_ora(vj.timp) == True:
            rezultat_echipa2_jurati += 1

    try:
        rezultate_echipa1 = (rezultat_echipa1_public/nr_voturi_public)*5 + (rezultat_echipa1_jurati/nr_voturi_jurati)*5
        rezultate_echipa2 = (rezultat_echipa2_public/nr_voturi_public)*5 + (rezultat_echipa2_jurati/nr_voturi_jurati)*5
    except ZeroDivisionError:
        rezultate_echipa1 = 0
        rezultate_echipa2 = 0
    
    return render_template("results.html", z=rezultate_echipa1, t=rezultate_echipa2, x=now)

def verificare_ora(timp):
    if 'ora' in session:
        ora = session['ora']
    else:
        ora = '00:00:00'

    if int(timp[0:2]) < int(ora[0:2]):
        return True
    elif int(timp[0:2]) == int(ora[0:2]):
        if int(timp[3:5]) < int(ora[3:5]):
            return True
        elif int(timp[3:5]) == int(ora[3:5]):
            if int(timp[6:8]) <= int(ora[6:8]):
                return True
    else:
        return False


    return True