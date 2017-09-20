# -*- coding: utf-8 -*-
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required
from forms import *
from models import *
from mypagination import *
from apps.contact import contact


@contact.route('/index', methods=["GET", "POST"])
@login_required
def index():
    form = ContactlistForm()
    if request.method == 'GET':
        return render_template("contact/index.html", form=form)
    else:
        if form.validate_on_submit():
            print form.email.data
            newcontact = Contacts(form.firstname.data, form.lastname.data, form.phone.data, form.email.data)
            db.session.add(newcontact)
            db.session.commit()
            flash('您成功添加一个联系.')
        else:
            flash(form.errors)
        return redirect(url_for('contact.index'))


# ajax-post 方法不刷新页面表格分页
@contact.route('/getcontacts', methods=["POST"])
def getcontacts():
    page = int(request.form.get('page', 1))
    PER_PAGE = int(request.form.get('per_page', 10))
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


@contact.route('/delete/<int:id>')
@login_required
def delete(id):
    ct = Contacts.query.filter_by(id=id).first_or_404()
    db.session.delete(ct)
    db.session.commit()
    flash('您成功删除一个联系人!')
    return redirect(url_for('contact.index'))


@contact.route('/change/<int:id>', methods=['GET', 'POST'])
@login_required
def change(id):
    if request.method == 'GET':
        ct = Contacts.query.filter_by(id=id).first_or_404()
        form = ContactlistForm()
        form.firstname.data = ct.firstname
        form.lastname.data = ct.lastname
        form.phone.data = ct.phone
        form.email.data = ct.email
        return render_template('contact/modify.html', form=form)
    else:
        form = ContactlistForm()
        if form.validate_on_submit():
            ct = Contacts.query.filter_by(id=id).first_or_404()
            ct.firstname = form.firstname.data
            ct.lastname = form.lastname.data
            ct.phone = form.phone.data
            ct.email = form.email.data
            db.session.commit()
            flash('您修改了一个联系人!')
        else:
            flash(form.errors)
        return redirect(url_for('contact.index'))
