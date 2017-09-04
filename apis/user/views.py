# -*- coding: UTF-8 -*-
from flask import jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
from apis.user import authapi
from models import *
import hashlib

auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'admin':
        return 'admin'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


@authapi.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def make_public_user(user):
    new_user = {}
    for field in user:
        if field == 'id':
            new_user['url'] = url_for('authapi.get_user_api', user_id=user['id'], _external=True)
        else:
            new_user[field] = user[field]
    return new_user


@authapi.route('/auth/v1/users', methods=['GET'])
@auth.login_required
def get_users_api():
    users = Serializer.serializelist(User.query.all())

    return jsonify({'users': map(make_public_user, users)})


@authapi.route('/auth/v1/users/<int:user_id>', methods=['GET'])
@auth.login_required
def get_user_api(user_id):
    users = Serializer.serializelist(User.query.all())
    user = filter(lambda t: t['id'] == user_id, users)
    if len(user) == 0:
        abort(404)
    return jsonify({'user': map(make_public_user, user)})


@authapi.route('/auth/v1/users', methods=['POST'])
@auth.login_required
def create_user():
    if not request.json or not 'username' in request.json or not 'password' in request.json or not 'role' in request.json:
        abort(400)
    user = {
        'username': request.json['username'],
        'password': request.json['password'],
        'role': request.json['role']
    }
    m = hashlib.md5()
    m.update(user.get('password'))
    u = User(user.get('username'), m.hexdigest(), user.get('role'))
    db.session.add(u)
    db.session.commit()

    return jsonify({'user': user}), 201


@authapi.route('/auth/v1/users/<int:user_id>', methods=['PUT'])
@auth.login_required
def update_user(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    if not request.json:
        abort(400)
    if 'username' in request.json and type(request.json['username']) != unicode:
        abort(400)
    if 'password' in request.json and type(request.json['password']) is not unicode:
        abort(400)
    if 'role' in request.json and type(request.json['role']) is not unicode:
        abort(400)

    m = hashlib.md5()
    m.update(request.json.get('password', user.password))

    user.username = request.json.get('username', user.username)
    user.password = m.hexdigest()
    user.role = request.json.get('role', user.role)
    db.session.commit()

    return jsonify({'user': {"status": "change success"}})


@authapi.route('/auth/v1/users/<int:user_id>', methods=['DELETE'])
@auth.login_required
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    db.session.delete(user)
    db.session.commit()

    return jsonify({'user': {"status": "delete success"}})
