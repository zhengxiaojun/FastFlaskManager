# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 24)])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 24)])
    submit = SubmitField('登录')


class ContactlistForm(FlaskForm):
    firstname = StringField('名', validators=[DataRequired(), Length(1, 50)])
    lastname = StringField('姓', validators=[DataRequired(), Length(1, 50)])
    phone = StringField('电话', validators=[Length(1, 200)])
    email = StringField('邮箱', validators=[Length(1, 200)])
    submit = SubmitField('提交')


class TodoListForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(1, 64)])
    status = RadioField('是否完成', validators=[DataRequired()], choices=[("1", '是'), ("0", '否')])
    submit = SubmitField('提交')
