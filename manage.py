# -*- coding: utf-8 -*-
from flask_script import Manager, Server
from run import app
from models import *

manager = Manager(app)
manager.add_command("127.0.0.1", Server())


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, Filelist=Filelist)


if __name__ == '__main__':
    manager.run()


# run cmd in shell

# python manage.py shell

# sqlite commands

# sqlite3 ./database/mypage.db
# .databases
# .tables
# .schema <table>
# .quit
