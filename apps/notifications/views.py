# -*- coding: utf-8 -*-
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required
from models import *
from forms import *
from apps.notifications import ntfy


@ntfy.route('/index', methods=['GET'])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    notfys = Notifications.query.order_by(db.desc(Notifications.create_time)).paginate(page, 10, False).items
    pagination = Notifications.query.order_by(db.desc(Notifications.create_time)).paginate(page, 10, True)

    return render_template('notifications/index.html', notfys=notfys, pagination=pagination)


@ntfy.route('/viewfile/<int:id>', methods=['GET'])
@login_required
def viewfile(id):
    form = NotifyForm()
    notfy = Notifications.query.filter_by(id=id).first_or_404()
    form.n_type.data = notfy.n_type
    form.content.data = notfy.content

    notfy.is_read = 1
    db.session.commit()

    return render_template('notifications/notify.html', form=form)


@ntfy.route('/delete/<int:id>')
@login_required
def delete(id):
    notfy = Notifications.query.filter_by(id=id).first_or_404()
    db.session.delete(notfy)
    db.session.commit()
    flash('您成功删除一个消息!')
    return redirect(url_for('ntfy.index'))


@ntfy.route('/poll', methods=['POST'])
@login_required
def poll():
    notfys = Notifications.query.filter_by(is_read=0).order_by(db.desc(Notifications.create_time)).all()
    total = str(len(notfys))
    if total == "0":
        ntfy_view = total
    else:
        ntfy_view = "<a href='#' class='dropdown-toggle' data-toggle='dropdown'>"
        ntfy_view += "<i class='fa fa-bell-o'></i>"
        ntfy_view += "<span class='label label-warning'>" + total + "</span></a>"
        ntfy_view += "<ul class='dropdown-menu'>"
        ntfy_view += "<li class='header'>您有 " + total + " 条未读通知!</li>"
        ntfy_view += "<li>"
        ntfy_view += "<!-- inner menu: contains the actual data -->"
        ntfy_view += "<ul class='menu'>"

        for notfy in notfys:
            ntfy_view += "<li>"
            ntfy_view += "<a href='" + str(url_for("ntfy.viewfile", id=notfy.id)) + "'>"
            ntfy_view += "<i class='fa fa-user text-aqua'></i> " + notfy.content
            ntfy_view += "</a>"
            ntfy_view += "</li>"
        ntfy_view += "</ul>"
        ntfy_view += "</li>"
        ntfy_view += "<li class='footer'><a href='" + str(url_for("ntfy.index")) + "'>查看全部</a></li>"
        ntfy_view += "</ul>"

    return ntfy_view
