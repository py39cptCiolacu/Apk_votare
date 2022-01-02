from . import db

class Ip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(150), unique=True)

class Voturi(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    pub_jur = db.Column(db.Boolean)
    vot1 = db.Column(db.String(150))
    vot2 = db.Column(db.String(150))

    def __init__(self, pub_jur, vot1, vot2):
        self.pub_jur = pub_jur
        self.vot1 = vot1
        self.vot2 = vot2
