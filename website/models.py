from . import db

class Ora(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    ora = db.Column(db.String(150))

    def __init__(self, ora):
        self.ora = ora


class Voturi(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_type = db.Column(db.String(50))
    alegere =db.Column(db.String(150))
    ip = db.Column(db.String(150))
    parola = db.Column(db.String(150))
    jurat = db.Column(db.String(150))
    timp = db.Column(db.String(150))

    def __init__(self, user_type = '0', alegere= '0', ip='NU', parola='NU', jurat='NU', timp='0'):
        self.user_type = user_type
        self.alegere = alegere
        self.ip = ip
        self.parola = parola
        self.jurat = jurat
        self.timp = timp

class Participanti(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    participanti = db.Column(db.String(300))

    def __init__(self, participanti):
        self.participanti = participanti


