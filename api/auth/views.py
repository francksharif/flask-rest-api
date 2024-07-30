import validators
from flask import request, jsonify
from . import auth 
from werkzeug.security import check_password_hash, generate_password_hash
from ..models import User
from ..constants.http_status_code import *
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from .. import db



# Registering a new User 
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



# Login a registered User
@auth.route('/login', methods=['GET', 'POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    user  = User.query.filter_by(email=email).first()
    
    if user:
        if check_password_hash(user.password, password):
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)


            return jsonify({
                'message': 'User logged in successfully.',
                'user':{
                    'refresh': refresh,
                    'access': access,
                    'username': user.username,
                    'email': user.email
                }
            }), HTTP_200_OK


    return jsonify({
            'error': 'Wrong credentials. Please try again.'
        }), HTTP_401_UNAUTHORIZED


# Get User information when logged in
@auth.route('/me')
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        'username': user.username,
        'email': user.email
    }), HTTP_200_OK


# Refresh User token
@auth.route('/token/refresh')
@jwt_required(refresh=True)
def refresh_users_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({
        'access': access,
    }), HTTP_200_OK