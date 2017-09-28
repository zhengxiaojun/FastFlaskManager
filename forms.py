# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import RadioField, SubmitField, StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length
from ext import myfile


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
    title = StringField('标题', validators=[DataRequired(), Length(1, 64)], render_kw={"placeholder": "请输入标题"})
    status = RadioField('是否完成', validators=[DataRequired()], choices=[("1", '是'), ("0", '否')])
    submit = SubmitField('提交')


class ServerListForm(FlaskForm):
    name = StringField('名称', validators=[DataRequired(), Length(1, 64)], render_kw={"placeholder": "请输入名称"})
    path = StringField('路径', validators=[DataRequired(), Length(1, 64)], render_kw={"placeholder": "请输入路径"})
    description = TextAreaField('描述', validators=[Length(1, 64)], render_kw={"placeholder": "请输入描述"})
    submit = SubmitField('提交')


class UploadForm(FlaskForm):
    file = FileField('请上传', validators=[FileRequired(), FileAllowed(myfile, '文件格式不对!')])
    submit = SubmitField('上传')


class NotifyForm(FlaskForm):
    n_type = StringField('类别', render_kw={'readonly': True})
    content = TextAreaField('内容', render_kw={'readonly': True})
