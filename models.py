# -*- coding: UTF-8 -*-
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.inspection import inspect
from itsdangerous import TimedJSONWebSignatureSerializer as SerializerToken, BadSignature, SignatureExpired
import time, os, hashlib, random

db = SQLAlchemy()


class Serializer(object):
    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serializelist(cols):
        return [m.serialize() for m in cols]


class Contacts(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(200), nullable=True)

    def __init__(self, firstname, lastname, phone, email):
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.email = email

    def __repr__(self):
        return '[%s,%s,%s,%s,%s]' % (self.id, self.firstname, self.lastname, self.phone, self.email)


class User(UserMixin, db.Model, Serializer):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(24), nullable=False)
    password = db.Column(db.String(24), nullable=False)
    role = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.String(50), nullable=True)

    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role
        self.create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def serialize(self):
        d = Serializer.serialize(self)
        del d['password']  # 不显示密码
        return d

    def verify_password(self, password):
        if password == self.password:
            return True
        else:
            return False

    def generate_auth_token(self, expiration=600):
        s = SerializerToken("produce token", expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = SerializerToken("produce token")
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user


class Todolist(db.Model):
    __tablename__ = 'todolist'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(1024), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.String(50), nullable=False)

    def __init__(self, user_id, title, status):
        self.user_id = user_id
        self.title = title
        self.status = status
        self.create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


class Serverlist(db.Model):
    __tablename__ = 'serverlist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024), nullable=False)
    path = db.Column(db.String(1024), nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.String(50), nullable=False)
    update_time = db.Column(db.String(50), nullable=False)

    def __init__(self, name, path, description, status):
        self.name = name
        self.path = path
        self.description = description
        self.status = status
        self.create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


class Filelist(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(1024), nullable=False)
    md5_filename = db.Column(db.String(1024), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    path = db.Column(db.String(1024), nullable=False)
    url = db.Column(db.String(1024), nullable=False)
    create_time = db.Column(db.String(50), nullable=False)

    def __init__(self, filename, md5_filename, path, url):
        self.filename = filename
        self.md5_filename = md5_filename
        self.path = path
        self.url = url
        self.size = self.get_FileSize(path)
        self.create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def get_FileSize(self, filePath):
        filePath = unicode(filePath, 'utf8')
        fsize = os.path.getsize(filePath)
        fsize = fsize / float(1024 * 1024)
        return round(fsize, 2)

    @staticmethod
    def get_md5_filename(filename):
        ext = os.path.splitext(filename)[1]
        m = hashlib.md5()
        m.update(filename + str(random.randint(0, 99)))
        filename = m.hexdigest() + ext
        return filename

# if __name__ == '__main__':
#     db.create_all()
