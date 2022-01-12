from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

from flask_sqlalchemy.utils import parse_version


db = SQLAlchemy()
DB_NAME = "baza2.db"

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ApK-VoTaRe-DeBaTeX'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import Voturi

    create_database(app)
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')



