from runpages import db


# from datetime import datetime

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=1)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    phone = db.Column(db.String(200))
    email = db.Column(db.String(200))

    def __init__(self, id, firstname, lastname, phone, email):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.email = email

    def __repr__(self):
        return '[%s,%s,%s,%s,%s]' % (self.id, self.firstname, self.lastname, self.phone, self.email)


class Todolist(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=1)
    user_id = db.Column(db.Integer)
    title = db.Column(db.String(1024))
    status = db.Column(db.Integer)
    create_time = db.Column(db.Integer)
