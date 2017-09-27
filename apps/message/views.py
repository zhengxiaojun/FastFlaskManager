# -*- coding: utf-8 -*-
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from forms import *
from models import *
from mypagination import *
from flask_socketio import emit, disconnect
from ext import socketio
from apps.message import msg

import time

namespace = '/msg/test'


@msg.route('/index')
@login_required
def index():
    return render_template('message/index.html')


@socketio.on('my event', namespace=namespace)
def test_message(message):
    emit('my response', {'data': message['data'], 'time': str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))})


@socketio.on('my broadcast event', namespace=namespace)
def test_message(message):
    emit('my response', {'data': message['data'], 'time': str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))},
         broadcast=True)


@socketio.on('disconnect_request', namespace=namespace)
def disconnect_request():
    emit('my response',
         {'data': '连接已断开.', 'time': str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))})
    disconnect()


@socketio.on('connect', namespace=namespace)
def test_connect():
    emit('my response', {'data': '已连接.', 'time': str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))})


# @socketio.on('disconnect', namespace=namespace)
# def test_disconnect():
#     print 'Client disconnected', request.sid
