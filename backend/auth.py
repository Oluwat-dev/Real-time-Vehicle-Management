"""
This script implements a Flask Blueprint for user authentication with three key routes: /register, /login, and /logout. The /register route allows new users to sign up by hashing their passwords and checking for existing usernames, while the /login route authenticates users and logs them in using Flask-Login. The /logout route logs out the authenticated user and requires them to be logged in before access, returning appropriate JSON responses for each action
"""

#Import Dependencies
from flask import Blueprint, request, jsonify
from models import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = generate_password_hash(data['password'], method='sha256')

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'User already exists'}), 400

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully!'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()

    if user and check_password_hash(user.password, data['password']):
        login_user(user)
        return jsonify({'message': 'Login successful!'}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully!'}), 200
