# -*- coding: utf-8 -*-
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models import *
from forms import *
from apps.todo import todo


# get 方法刷新页面表格分页
@todo.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = TodoListForm()
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        todolists = Todolist.query.paginate(page, 10, False).items
        pagination = Todolist.query.paginate(page, 10, True)
        return render_template('todo/todolist.html', todolists=todolists, form=form, pagination=pagination)
    else:
        if form.validate_on_submit():
            todo = Todolist(current_user.id, form.title.data, form.status.data)
            db.session.add(todo)
            db.session.commit()
            flash('您添加了一个事件!')
        else:
            flash(form.errors)
        return redirect(url_for('todo.index'))


@todo.route('/delete/<int:id>')
@login_required
def delete(id):
    todolist = Todolist.query.filter_by(id=id).first_or_404()
    db.session.delete(todolist)
    db.session.commit()
    flash('您成功删除一个事件!')
    return redirect(url_for('todo.index'))


@todo.route('/change/<int:id>', methods=['GET', 'POST'])
@login_required
def change(id):
    if request.method == 'GET':
        todolist = Todolist.query.filter_by(id=id).first_or_404()
        form = TodoListForm()
        form.title.data = todolist.title
        form.status.data = str(todolist.status)
        return render_template('todo/modify.html', form=form)
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
        return redirect(url_for('todo.index'))
