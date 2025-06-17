"""
The init_db() function sets up the database by creating all necessary tables using SQLAlchemy's db.create_all() method. It also includes a step to add a default "admin" user if none exist, using the username "admin" and the password "admin". However, for security purposes, the admin password should be hashed before storing it in the database instead of saving it as plain text.
"""

from app import db
from models import User, Violation

def init_db():
    db.create_all()

    # Optional: Add some default data
    if not User.query.first():
        admin = User(username="admin", password="admin")
        db.session.add(admin)
        db.session.commit()
