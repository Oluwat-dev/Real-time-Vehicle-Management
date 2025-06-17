# """
# This script defines a Flask web application with endpoints to manage vehicle violations and user authentication. It uses SQLAlchemy to interact with a SQLite database, allowing for the recording, retrieval, updating, and deletion of violation records, as well as user registration, login, and deletion. The application includes models for Violation and User, with endpoints for handling violation data and user management.
# """

# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)

# # Configure SQLite Database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///violations.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # Initialize the database
# db = SQLAlchemy(app)

# # Models
# class Violation(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     license_plate = db.Column(db.String(50), nullable=False)
#     speed = db.Column(db.Float, nullable=False)
#     latitude = db.Column(db.Float)
#     longitude = db.Column(db.Float)
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'license_plate': self.license_plate,
#             'speed': self.speed,
#             'latitude': self.latitude,
#             'longitude': self.longitude,
#             'timestamp': self.timestamp
#         }

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(200), nullable=False)

# # Initialize the database schema
# @app.before_first_request
# def create_tables():
#     db.create_all()

# # Record violation endpoint
# @app.route('/record_violation', methods=['POST'])
# def record_violation():
#     data = request.json
#     if not data or 'license_plate' not in data or 'speed' not in data:
#         return jsonify({'error': 'Invalid input'}), 400
    
#     license_plate = data.get('license_plate')
#     speed = data.get('speed')
#     latitude = data.get('latitude')  # Optional
#     longitude = data.get('longitude')  # Optional

#     violation = Violation(
#         license_plate=license_plate,
#         speed=speed,
#         latitude=latitude,
#         longitude=longitude
#     )

#     db.session.add(violation)
#     db.session.commit()

#     return jsonify({'message': 'Violation recorded successfully'}), 200

# # Get all violations (for displaying on map or in table)
# @app.route('/get_violations', methods=['GET'])
# def get_violations():
#     violations = Violation.query.all()
#     return jsonify([violation.to_dict() for violation in violations])

# # User registration endpoint
# @app.route('/register', methods=['POST'])
# def register_user():
#     data = request.json
#     if not data or 'username' not in data or 'email' not in data or 'password' not in data:
#         return jsonify({'error': 'Missing data'}), 400

#     username = data.get('username')
#     email = data.get('email')
#     password = data.get('password')

#     # Check if the user already exists
#     if User.query.filter_by(email=email).first():
#         return jsonify({'error': 'User already exists'}), 400

#     # Hash the password
#     hashed_password = generate_password_hash(password, method='sha256')

#     # Create a new user
#     new_user = User(username=username, email=email, password=hashed_password)
#     db.session.add(new_user)
#     db.session.commit()

#     return jsonify({'message': 'User registered successfully'}), 201

# # User login endpoint
# @app.route('/login', methods=['POST'])
# def login_user():
#     data = request.json
#     if not data or 'email' not in data or 'password' not in data:
#         return jsonify({'error': 'Missing data'}), 400

#     email = data.get('email')
#     password = data.get('password')

#     # Find user by email
#     user = User.query.filter_by(email=email).first()

#     # Verify password
#     if user and check_password_hash(user.password, password):
#         return jsonify({'message': 'Login successful'}), 200
#     else:
#         return jsonify({'error': 'Invalid credentials'}), 401

# # Update violation (in case of manual corrections)
# @app.route('/update_violation/<int:id>', methods=['PUT'])
# def update_violation(id):
#     violation = Violation.query.get_or_404(id)
#     data = request.json

#     license_plate = data.get('license_plate')
#     speed = data.get('speed')
#     latitude = data.get('latitude')
#     longitude = data.get('longitude')

#     if license_plate:
#         violation.license_plate = license_plate
#     if speed:
#         violation.speed = speed
#     if latitude:
#         violation.latitude = latitude
#     if longitude:
#         violation.longitude = longitude

#     db.session.commit()
#     return jsonify({'message': 'Violation updated successfully'}), 200

# # Delete violation
# @app.route('/delete_violation/<int:id>', methods=['DELETE'])
# def delete_violation(id):
#     violation = Violation.query.get_or_404(id)
#     db.session.delete(violation)
#     db.session.commit()
#     return jsonify({'message': 'Violation deleted successfully'}), 200

# # Delete user
# @app.route('/delete_user/<int:id>', methods=['DELETE'])
# def delete_user(id):
#     user = User.query.get_or_404(id)
#     db.session.delete(user)
#     db.session.commit()
#     return jsonify({'message': 'User deleted successfully'}), 200

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configure SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///violations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Models
class Violation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String(50), nullable=False)
    speed = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'license_plate': self.license_plate,
            'speed': self.speed,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Initialize the database schema
@app.before_first_request
def create_tables():
    db.create_all()

# Root endpoint
@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the Vehicle Violation API'})
# Root endpoint
# @app.route('/')
# def home():
#     return render_template('index.html')

# Record violation endpoint
@app.route('/record_violation', methods=['POST'])
def record_violation():
    data = request.get_json()
    if not data or 'license_plate' not in data or 'speed' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    license_plate = data.get('license_plate')
    speed = data.get('speed')
    latitude = data.get('latitude', None) 
    longitude = data.get('longitude', None) 

    try:
        violation = Violation(
            license_plate=license_plate,
            speed=speed,
            latitude=latitude,
            longitude=longitude
        )
        db.session.add(violation)
        db.session.commit()
        return jsonify({'message': 'Violation recorded successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get all violations
@app.route('/get_violations', methods=['GET'])
def get_violations():
    try:
        violations = Violation.query.all()
        return jsonify([violation.to_dict() for violation in violations]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# User registration endpoint
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    if not data or 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Missing data'}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'User already exists'}), 400

    try:
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# User login endpoint
@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Missing data'}), 400

    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

# Update violation
@app.route('/update_violation/<int:id>', methods=['PUT'])
def update_violation(id):
    violation = Violation.query.get_or_404(id)
    data = request.get_json()

    if 'license_plate' in data:
        violation.license_plate = data['license_plate']
    if 'speed' in data:
        violation.speed = data['speed']
    if 'latitude' in data:
        violation.latitude = data['latitude']
    if 'longitude' in data:
        violation.longitude = data['longitude']

    try:
        db.session.commit()
        return jsonify({'message': 'Violation updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete violation
@app.route('/delete_violation/<int:id>', methods=['DELETE'])
def delete_violation(id):
    violation = Violation.query.get_or_404(id)
    try:
        db.session.delete(violation)
        db.session.commit()
        return jsonify({'message': 'Violation deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete user
@app.route('/delete_user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
