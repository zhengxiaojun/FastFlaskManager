# -*- coding: UTF-8 -*-
from flask import Flask, g
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_socketio import SocketIO
from models import User
import os

cPath = os.path.abspath('.')

db = SQLAlchemy()
login_manager = LoginManager()

app = Flask(__name__, template_folder=os.path.join(cPath, 'templates'))
bootstrap = Bootstrap(app)

app.secret_key = "this is my page"

# 数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/mypage.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 文件上传
myfile = UploadSet('MYFILE', IMAGES)
app.config['UPLOADED_MYFILE_DEST'] = os.path.join(os.path.dirname(__file__), 'uploads')
# app.config['UPLOADED_MYFILE_ALLOW'] = IMAGES

configure_uploads(app, myfile)

# 数据初始化
db.init_app(app)

# 登录管理
login_manager.init_app(app)
login_manager.login_view = "auth.login"

# 消息
socketio = SocketIO(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()
