from . import db

class Voturi(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_type = db.Column(db.String(50))
    vot1 = db.Column(db.String(150))
    vot2 = db.Column(db.String(150))
    ip = db.Column(db.String(150))

    def __init__(self, user_type, vot1, vot2, ip='NU'):
        self.user_type = user_type
        self.vot1 = vot1
        self.vot2 = vot2
        self.ip = ip

