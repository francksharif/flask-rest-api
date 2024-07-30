import validators
from flask import request, jsonify
from . import auth 
from werkzeug.security import check_password_hash, generate_password_hash
from ..models import User
from ..constants.http_status_code import *
from .. import db


@auth.route('/register', methods=['GET', 'POST'])
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    
    if len(password) < 6:
        return jsonify({'error': 'Password is too short.'}), HTTP_400_BAD_REQUEST
    
    if len(username) < 5:
        return jsonify({'error': 'Username is too short.'}), HTTP_400_BAD_REQUEST

    if not username.isalnum() or ' ' in username:
        return jsonify({'error': 'Username should be alphanumeric, also no spaces.'}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({'error': 'Your email is not valid.'}), HTTP_400_BAD_REQUEST
        
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error': 'You are already registered.'}), HTTP_409_CONFLICT

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error': 'This username is already taken.'}), HTTP_409_CONFLICT
    
    pwd_hash = generate_password_hash(password)

    user = User(
        username = username,
        password = pwd_hash,
        email = email
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'User created',
        'user': {
            'username': username, 'email': email
        }
    }), HTTP_201_CREATED