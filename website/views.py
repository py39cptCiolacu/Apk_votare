from flask import Blueprint, render_template, flash, redirect, request
from flask.helpers import url_for
from website.models import Voturi
from . import db 

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():

    return render_template("home.html")


@views.route('/voting_public_sala', methods=['GET', 'POST'])
def voting_public_sala():

    if request.method == 'POST':
        vot1 = request.form['echipeA']
        vot2 = request.form['echipeB']

        vot = Voturi('sala', vot1, vot2)

        db.session.add(vot)
        db.session.commit()

        flash("GATA AI VOTAT")

        return redirect(url_for('views.results'))

    return render_template("voting.html")

    
@views.route('/voting_public_online', methods=['GET', 'POST'])
def voting_public_online():

    if request.method == 'POST':
        vot1 = request.form['echipeA']
        vot2 = request.form['echipeB']

        vot = Voturi('online', vot1, vot2) #aici mai pun si IP-ul


        db.session.add(vot)
        db.session.commit()

        flash("GATA AI VOTAT")

        return redirect(url_for('views.results'))

    return render_template("voting.html")


@views.route('/voting_jurat', methods=['GET', 'POST'])
def voting_jurat():

    if request.method == 'POST':
        vot1 = request.form['echipeA']
        vot2 = request.form['echipeB']

        vot = Voturi('jurat', vot1, vot2) #aici mai pun si IP-ul

        #daca vot.ip nu se gaseste in baza de date, si nu e diferit de 'NU', voteaza si il adauga in baza de date
        db.session.add(vot)
        db.session.commit()

        flash("GATA AI VOTAT")

        return redirect(url_for('views.results'))

    return render_template("voting.html")

@views.route('/results', methods=['GET', 'POST'])
def results():


    return render_template("results.html", x=1, y=2, z=3, t=4)
