# -*- coding: UTF-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models import User
import os

cPath = os.path.abspath('.')

db = SQLAlchemy()
login_manager = LoginManager()

app = Flask(__name__, template_folder=os.path.join(cPath, 'templates'))
bootstrap = Bootstrap(app)

app.secret_key = "this is my page"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/mypage.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()
