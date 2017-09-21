# -*- coding: utf-8 -*-
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models import *
from forms import *
from apps.service import svm

import time, subprocess


@svm.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = ServerListForm()
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        svlists = Serverlist.query.paginate(page, 10, False).items
        pagination = Serverlist.query.paginate(page, 10, True)
        return render_template('service/index.html', svlists=svlists, form=form, pagination=pagination)
    else:
        if form.validate_on_submit():
            svl = Serverlist(form.name.data, form.path.data, form.description.data, 0)  # status : 0 未运行,1 在运行
            db.session.add(svl)
            db.session.commit()
            flash('您添加了一个服务!')
            Notifications.notify(current_user.username, u"服务", u"添加了一个新服务")
        else:
            flash(form.errors)
            Notifications.notify(current_user.username, u"服务", u"添加服务错误: " + str(form.errors))
        return redirect(url_for('svm.index'))


@svm.route('/change/<int:id>', methods=['GET', 'POST'])
@login_required
def change(id):
    form = ServerListForm()
    if request.method == 'GET':
        svl = Serverlist.query.filter_by(id=id).first_or_404()
        form.name.data = svl.name
        form.path.data = svl.path
        form.description.data = svl.description
        return render_template('service/modify.html', form=form)
    else:
        if form.validate_on_submit():
            svl = Serverlist.query.filter_by(id=id).first_or_404()
            svl.name = form.name.data
            svl.path = form.path.data
            svl.description = form.description.data
            svl.update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            db.session.commit()
            flash('您修改了一个服务!')
            Notifications.notify(current_user.username, u"服务", u"修改了一个服务")
        else:
            flash(form.errors)
            Notifications.notify(current_user.username, u"服务", u"修改服务错误: " + str(form.errors))
        return redirect(url_for('svm.index'))


@svm.route('/delete/<int:id>')
@login_required
def delete(id):
    svl = Serverlist.query.filter_by(id=id).first_or_404()
    db.session.delete(svl)
    db.session.commit()
    flash('您成功删除一个服务!')
    Notifications.notify(current_user.username, u"服务", u"删除了一个服务")
    return redirect(url_for('svm.index'))


@svm.route('/start/<int:id>', methods=['GET'])
@login_required
def start(id):
    svl = Serverlist.query.filter_by(id=id).first_or_404()
    cmd = svl.path
    cmd = "bash " + str(cmd) + " start"

    try:
        result = subprocess.check_output(cmd, shell=True)
        svl.status = 1
        db.session.commit()
    except Exception as err:
        result = str(err)
    finally:
        flash(result)
        Notifications.notify(current_user.username, u"服务", str(result))

    return redirect(url_for('svm.index'))


@svm.route('/stop/<int:id>', methods=['GET'])
@login_required
def stop(id):
    svl = Serverlist.query.filter_by(id=id).first_or_404()
    cmd = svl.path
    cmd = "bash " + str(cmd) + " stop"

    try:
        result = subprocess.check_output(cmd, shell=True)
        svl.status = 0
        db.session.commit()
    except Exception as err:
        result = str(err)
    finally:
        flash(result)
        Notifications.notify(current_user.username, u"服务", str(result))

    return redirect(url_for('svm.index'))
