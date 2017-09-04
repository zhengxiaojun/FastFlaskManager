# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 24)], render_kw={"placeholder": "请输入用户名"})
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 24)], render_kw={"placeholder": "请输入密码"})
    submit = SubmitField('登录')


class NewUserForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 24)], render_kw={"placeholder": "请输入用户名"})
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 24)], render_kw={"placeholder": "请输入密码"})
    role = RadioField('是否管理员', validators=[DataRequired()], choices=[("1", '是'), ("0", '否')])
    submit = SubmitField('注册')


class ChangeUserForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 24)], render_kw={'readonly': True})
    password = PasswordField('新密码', validators=[DataRequired(), Length(1, 24)], render_kw={"placeholder": "请输入新密码"})
    role = RadioField('是否管理员', validators=[DataRequired()], choices=[("1", '是'), ("0", '否')])
    submit = SubmitField('更新密码')


class ContactlistForm(FlaskForm):
    firstname = StringField('名', validators=[DataRequired(), Length(1, 50)], render_kw={"placeholder": "请输入名"})
    lastname = StringField('姓', validators=[DataRequired(), Length(1, 50)], render_kw={"placeholder": "请输入姓"})
    phone = StringField('电话', validators=[Length(0, 200)], render_kw={"placeholder": "请输入电话"})
    email = StringField('邮箱', validators=[Length(0, 200)], render_kw={"placeholder": "请输入邮箱"})
    submit = SubmitField('提交')


class TodoListForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(1, 64)])
    status = RadioField('是否完成', validators=[DataRequired()], choices=[("1", '是'), ("0", '否')])
    submit = SubmitField('提交')
