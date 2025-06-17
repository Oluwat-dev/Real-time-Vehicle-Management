"""
The Config class stores essential configuration settings for a Flask application, including the SECRET_KEY for cryptographic operations and session security. It sets the SQLALCHEMY_DATABASE_URI to connect to a database, either from an environment variable or defaulting to SQLite. Additionally, it disables SQLAlchemy's object modification tracking to reduce overhead in the application.
"""

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///violations.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
