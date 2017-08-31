# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from mypagination import my_pagination
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

    result_table = ""
    result_table += "<table class='table table-hover'>"
    result_table += "<thead>"
    result_table += "<tr class='info'>"
    result_table += "<th>id</th>"
    result_table += "<th>firstname</th>"
    result_table += "<th>lastname</th>"
    result_table += "<th>phone</th>"
    result_table += "<th>email</th>"
    result_table += "</tr>"
    result_table += "</thead>"
    result_table += "<tbody>"
    for user in users:
        result_table += "<tr>"
        result_table += "<td>" + str(user.id) + "</td>"
        result_table += "<td>" + str(user.firstname) + "</td>"
        result_table += "<td>" + str(user.lastname) + "</td>"
        result_table += "<td>" + str(user.phone) + "</td>"
        result_table += "<td>" + str(user.email) + "</td>"
        result_table += "</tr>"
    result_table += "</tbody>"
    result_table += "</table>"

    result_page = my_pagination(pagination, "queryUsers", PER_PAGE)
    result = result_table + result_page
    return result


@app.route('/gettodolist', methods=["POST"])
def gettodolist():
    page = int(request.form.get('page', 1))
    PER_PAGE = int(request.form.get('per_page', 3))
    todolists = Todolist.query.paginate(page, PER_PAGE, False).items
    pagination = Todolist.query.paginate(page, PER_PAGE, True)

    result_table = ""
    result_table += "<table class='table table-hover'>"
    result_table += "<thead>"
    result_table += "<tr class='info'>"
    result_table += "<th>id</th>"
    result_table += "<th>user_id</th>"
    result_table += "<th>title</th>"
    result_table += "<th>status</th>"
    result_table += "<th>create_time</th>"
    result_table += "</tr>"
    result_table += "</thead>"
    result_table += "<tbody>"
    for todo in todolists:
        result_table += "<tr>"
        result_table += "<td>" + str(todo.id) + "</td>"
        result_table += "<td>" + str(todo.user_id) + "</td>"
        result_table += "<td>" + str(todo.title) + "</td>"
        result_table += "<td>" + str(todo.status) + "</td>"
        result_table += "<td>" + str(todo.create_time) + "</td>"
        result_table += "</tr>"
    result_table += "</tbody>"
    result_table += "</table>"

    result_page = my_pagination(pagination, "queryTodolist", PER_PAGE)
    result = result_table + result_page
    return result


if __name__ == '__main__':
    app.run(debug=True)
