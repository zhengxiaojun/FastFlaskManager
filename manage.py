# -*- coding: utf-8 -*-
from flask_script import Manager, Server
from run import app
from models import db, User

manager = Manager(app)
manager.add_command("127.0.0.1", Server())


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User)


if __name__ == '__main__':
    manager.run()
