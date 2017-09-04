# -*- coding: utf-8 -*-
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, login_user, logout_user
from forms import *
from models import *
from apps.auth import auth
import hashlib


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        m = hashlib.md5()
        m.update(request.form['password'])
        user = User.query.filter_by(username=request.form['username'], password=m.hexdigest()).first()
        if user:
            login_user(user)
            flash('登录成功!')
            return redirect(url_for('index'))
        else:
            flash('用户名或密码不对!')
    form = LoginForm()
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已成功退出!')
    return redirect(url_for('auth.login'))


@auth.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = NewUserForm()
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        userlist = User.query.paginate(page, 10, False).items
        pagination = User.query.paginate(page, 10, True)
        return render_template('auth/users.html', userlist=userlist, form=form, pagination=pagination)
    else:
        if form.validate_on_submit():
            m = hashlib.md5()
            m.update(form.password.data)
            user = User(form.username.data, m.hexdigest(), form.role.data)
            db.session.add(user)
            db.session.commit()
            flash('您添加了一个新用户!')
        else:
            flash(form.errors)
        return redirect(url_for('auth.index'))


@auth.route('/delete/<int:id>')
@login_required
def delete(id):
    user = User.query.filter_by(id=id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    flash('您成功删除一个新用户!')
    return redirect(url_for('auth.index'))


@auth.route('/change/<int:id>', methods=['GET', 'POST'])
@login_required
def change(id):
    form = ChangeUserForm()
    if request.method == 'GET':
        user = User.query.filter_by(id=id).first_or_404()
        form.username.data = user.username
        form.password.data = user.password
        form.role.data = str(user.role)
        return render_template('auth/modify.html', form=form)
    else:
        if form.validate_on_submit():
            m = hashlib.md5()
            user = User.query.filter_by(id=id).first_or_404()
            user.username = form.username.data
            m.update(form.password.data)
            user.password = m.hexdigest()
            user.role = form.role.data
            db.session.commit()
            flash('您修改了一个用户!')
        else:
            flash(form.errors)
        return redirect(url_for('auth.index'))
