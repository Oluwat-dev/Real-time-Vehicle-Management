"""This script defines two models, User and Violation, using SQLAlchemy and integrates them with Flask-Login for session management. The User model includes fields for id, username, and password, and establishes a one-to-many relationship with the Violation model, enabling each user to have multiple violations. The Violation model tracks violation details like license_plate, speed, timestamp, and associates each violation with a specific user via the user_id field, facilitating user-specific violation tracking"""

from datetime import datetime
from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    violations = db.relationship('Violation', backref='user', lazy=True)

class Violation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String(50), nullable=False)
    speed = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
