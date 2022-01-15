from flask import Blueprint, render_template, request, redirect, flash, url_for, session
from . import db
from .models import Ora, Voturi, Participanti



auth = Blueprint('auth', __name__)

#Se genereaza n ID-uri si parole (n=nr de jurati)
@auth.route('/login_jury', methods=['GET', 'POST'])
def login_jury():

    jurati = {"IoanaBarbu" : "ioanabarbu10", "TeodorGrama": "teodorgrama20", "EduardUngureanu": "eduardungureanu30"}

    if request.method == 'POST':
            id_juriu = request.form.get('id_juriu')
            parola_jurat = request.form.get('password')
            if id_juriu in jurati and jurati[id_juriu] == parola_jurat:
                session['jurat'] = id_juriu
                return redirect(url_for('views.voting_jurat'))
            else:
                flash('------------------------> Parola incorecta, incearca din nou', category='error')

    return render_template("login_jury.html")


# Publicul care este in sala. Va primi parola la intrare in sala. Se vor genera ininte un numar n de parole
# plus una speciala pentru orice eventualitate (de preferat n > nr de persoane din sala)
@auth.route('/login_public', methods = ['GET', 'POST'])
def login_public():

    content_parole = ['vpvjo251',
'asxaz599',
'eldif721',
'pymzn767',
'sdwmn820',
'vpirk660',
'xaowz993',
'znmpy969',
'qifzw924',
'jdbdo201',
'fegtv866',
'jvejb928',
'nagin471',
'svlcx512',
'axpew074',
'dgyvr803',
'knaxc584',
'ueugq334',
'glyyi652',
'rwxhg701',
'ewlcz739',
'zmndo932',
'uucgn551',
'gcogk010',
'cvfzc758',
'tcmut585',
'ebwha027',
'aotjg540',
'gbrsc710',
'jobxj559',
'mmuvn500',
'jkdtb429',
'uscjf718',
'mxcmz857',
'annpz975',
'aqcxf402',
'rwrzk899',
'pptcd621',
'rkizp001',
'tgcpp784',
'cfwvf623',
'ihvlp255',
'jgtmr236',
'jxmwh791',
'olfjw498',
'ptvwl214',
'oahga193',
'jfmgp566',
'onumh047',
'pvpwu389'
]

    if request.method == 'POST':
            parola = request.form.get('password_public')
            if parola in content_parole:
                session['parola'] = parola
                return redirect(url_for('views.voting_public_sala'))
            elif parola == "adminSetareTimp":
                return redirect(url_for('auth.adminCPT'))
            elif parola == "adminResetareBaza":
                return redirect(url_for('auth.adminCPT2'))
            elif parola == "adminSetareNume":
                return redirect(url_for('auth.adminCPT3'))
            else:
                flash('------------------------> Parola incorecta, incearca din nou', category='error')

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
        max_time = "Nu ai setat nimic"


    return render_template('admin.html', x=max_time)


@auth.route('/adminCPT2', methods = ['GET', 'POST'])
def adminCPT2():

    if request.method == 'POST':
        resetare = request.form.get('resetare')
        if resetare == "RESETEAZA-BAZA":
            Voturi.query.delete()
            db.session.commit()
            flash('------------------------> Baza resetata', categoty='succes')
        else:
            flash('------------------------> Ai introdus gresit', category='error')

    return render_template('admin2.html')


@auth.route('/adminCPT3', methods = ['GET', 'POST'])
def adminCPT3():

    if request.method == 'POST':
        participanti = request.form.get('participanti')
        db.session.add(Participanti(participanti = participanti))
        db.session.commit()
    flash('------------------------> Nume actualizate', categoty='succes')

    return render_template('admin3.html')






