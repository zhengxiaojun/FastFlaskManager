# -*- coding: UTF-8 -*-
from ext import db
from flask_login import UserMixin
import time


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


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False)
    password = db.Column(db.String(24), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password


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
