from flask import Blueprint, render_template, flash, redirect, request
from flask.helpers import url_for
from website.models import Voturi
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():

    return render_template("home.html")


@views.route('/voting_public', methods=['GET', 'POST'])
def voting_public():

    if request.method == 'POST':
        vot1 = request.form['echipeA']
        vot2 = request.form['echipeB']

        vot = Voturi(True, vot1, vot2)

        db.session.add(vot)
        db.session.commit()

        flash("GATA AI VOTAT")

        return redirect(url_for('views.results'))

    return render_template("voting_public.html")


@views.route('/voting_jurat', methods=['GET', 'POST'])
def voting_jurat():

    return render_template("voting_jurat.html")

@views.route('/results', methods=['GET', 'POST'])
def results():

    #calculat si afisat rezultatele

    return render_template("results.html")
