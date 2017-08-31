# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from mypagination import my_pagination, my_talbe
from models import *

import sys

reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__, template_folder='/Users/jack/PycharmProjects/studyflask/mypage/')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/easyUI'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# @app.route('/', methods=["GET"])
@app.route('/user/page/', methods=["GET"])
@app.route('/user/page/<int:page>', methods=["GET"])
def users(page=1):
    PER_PAGE = 6
    users = Users.query.paginate(page, PER_PAGE, False).items
    pagination = Users.query.paginate(page, PER_PAGE, True)

    return render_template("users.html", users=users, pagination=pagination)


@app.route('/', methods=["GET"])
def index():
    return render_template("newusers.html")


@app.route('/getusers', methods=["POST"])
def getusers():
    page = int(request.form.get('page', 1))
    PER_PAGE = int(request.form.get('per_page', 3))
    users = Users.query.paginate(page, PER_PAGE, False).items
    pagination = Users.query.paginate(page, PER_PAGE, True)

    cols = ["id", "firstname", "lastname", "phone", "email"]
    result_table = my_talbe(cols, users)

    result_page = my_pagination(pagination, "queryUsers", PER_PAGE)
    result = result_table + result_page
    return result


@app.route('/gettodolist', methods=["POST"])
def gettodolist():
    page = int(request.form.get('page', 1))
    PER_PAGE = int(request.form.get('per_page', 3))
    todolists = Todolist.query.paginate(page, PER_PAGE, False).items
    pagination = Todolist.query.paginate(page, PER_PAGE, True)

    cols = ["id", "user_id", "title", "status", "create_time"]
    result_table = my_talbe(cols, todolists)

    result_page = my_pagination(pagination, "queryTodolist", PER_PAGE)
    result = result_table + result_page
    return result


if __name__ == '__main__':
    app.run(debug=True)
