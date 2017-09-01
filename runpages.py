# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_login import login_required, login_user, logout_user, current_user
from ext import db, login_manager
from mypagination import my_pagination, my_talbe
from models import *
from forms import *

import sys

reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__, template_folder='/Users/jack/PycharmProjects/studyflask/mypage/templates')
bootstrap = Bootstrap(app)

app.secret_key = "this is my page"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/easyUI'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"


@app.route('/', methods=["GET"])
@app.route('/index', methods=["GET"])
@login_required
def index():
    return render_template("index.html")


@app.route('/contacts', methods=["GET", "POST"])
@login_required
def contacts():
    form = ContactlistForm()
    if request.method == 'GET':
        return render_template("contacts.html", form=form)
    else:
        if form.validate_on_submit():
            newcontact = Contacts(form.firstname.data, form.lastname.data, form.phone.data, form.email.data)
            db.session.add(newcontact)
            db.session.commit()
            flash('您成功添加一个联系.')
        else:
            flash(form.errors)
        return redirect(url_for('contacts'))


# ajax-post 方法不刷新页面表格分页
@app.route('/getcontacts', methods=["POST"])
def getcontacts():
    page = int(request.form.get('page', 1))
    PER_PAGE = int(request.form.get('per_page', 5))
    kword = request.form.get('kword', None)

    cols = ["id", "firstname", "lastname", "phone", "email"]

    if kword == None or kword == '':
        contacts = Contacts.query.paginate(page, PER_PAGE, False).items
        pagination = Contacts.query.paginate(page, PER_PAGE, True)
        result_table = my_talbe(cols, contacts)

        result_page = my_pagination(pagination, "queryContacts", PER_PAGE)
        result = result_table + result_page
        return result
    else:
        contacts = Contacts.query.filter(
            (Contacts.firstname.like('%' + kword + '%')) | (Contacts.lastname.like('%' + kword + '%')) | (
                Contacts.phone.like('%' + kword + '%')) | (Contacts.email.like('%' + kword + '%')))
        result_table = my_talbe(cols, contacts)
        result = result_table
        return result


# get 方法刷新页面表格分页
@app.route('/todolist', methods=['GET', 'POST'])
@login_required
def todolist():
    form = TodoListForm()
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        todolists = Todolist.query.paginate(page, 10, False).items
        pagination = Todolist.query.paginate(page, 10, True)
        return render_template('todolist.html', todolists=todolists, form=form, pagination=pagination)
    else:
        if form.validate_on_submit():
            todolist = Todolist(current_user.id, form.title.data, form.status.data)
            db.session.add(todolist)
            db.session.commit()
            flash('您添加了一个事件!')
        else:
            flash(form.errors)
        return redirect(url_for('todolist'))


@app.route('/todolist/delete/<int:id>')
@login_required
def delete_todo_list(id):
    todolist = Todolist.query.filter_by(id=id).first_or_404()
    db.session.delete(todolist)
    db.session.commit()
    flash('您成功删除一个事件!')
    return redirect(url_for('todolist'))


@app.route('/todolist/change/<int:id>', methods=['GET', 'POST'])
@login_required
def change_todo_list(id):
    if request.method == 'GET':
        todolist = Todolist.query.filter_by(id=id).first_or_404()
        form = TodoListForm()
        form.title.data = todolist.title
        form.status.data = str(todolist.status)
        return render_template('modify.html', form=form)
    else:
        form = TodoListForm()
        if form.validate_on_submit():
            todolist = Todolist.query.filter_by(id=id).first_or_404()
            todolist.title = form.title.data
            todolist.status = form.status.data
            db.session.commit()
            flash('您修改了一个事件!')
        else:
            flash(form.errors)
        return redirect(url_for('todolist'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username'], password=request.form['password']).first()
        if user:
            login_user(user)
            flash('登录成功!')
            return redirect(url_for('index'))
        else:
            flash('用户名或密码不对!')
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已成功退出!')
    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()


if __name__ == '__main__':
    app.run(debug=True)
