# from flask import Flask, render_template, request, jsonify, redirect, url_for

# app = Flask(__name__)

# # Root endpoint
# @app.route('/')
# def home():
#     """Renders the homepage."""
#     return render_template('index.html')

# # Endpoint: View Violations
# @app.route('/get_violations', methods=['GET'])
# def get_violations():
#     """Displays a list of recorded vehicle violations."""
#     # Mock data for violations
#     violations = [
#         {"id": 1, "plate_number": "ABC123", "location": "Downtown", "time": "2024-11-23 10:00"},
#         {"id": 2, "plate_number": "XYZ789", "location": "Highway", "time": "2024-11-23 11:15"}
#     ]
#     return render_template('violations.html', violations=violations)

# # Endpoint: Record a Violation
# @app.route('/record_violation', methods=['GET', 'POST'])
# def record_violation():
#     """Allows users to record a new vehicle violation."""
#     if request.method == 'POST':
#         # Extract data from form
#         plate_number = request.form.get('plate_number')
#         location = request.form.get('location')
#         time = request.form.get('time')
        
#         # Process the data (e.g., save to database)
#         # This is a mock response for now
#         return jsonify({
#             "message": "Violation recorded successfully",
#             "data": {
#                 "plate_number": plate_number,
#                 "location": location,
#                 "time": time
#             }
#         }), 201

#     return render_template('record_violation.html')

# # Endpoint: Register User
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     """Handles user registration."""
#     if request.method == 'POST':
#         # Extract registration data
#         username = request.form.get('username')
#         password = request.form.get('password')
        
#         # Process registration (e.g., save to database)
#         # Mock response
#         return jsonify({
#             "message": "User registered successfully",
#             "data": {"username": username}
#         }), 201

#     return render_template('register.html')

# # Endpoint: Login User
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     """Handles user login."""
#     if request.method == 'POST':
#         # Extract login data
#         username = request.form.get('username')
#         password = request.form.get('password')
        
#         # Validate login (mock validation)
#         if username == "admin" and password == "password":  # Example credentials
#             return redirect(url_for('home'))
#         else:
#             return jsonify({"message": "Invalid credentials"}), 401

#     return render_template('login.html')

# # Endpoint: Redirect to Analytics (Dash)
# @app.route('/analytics', methods=['GET'])
# def analytics():
#     """Redirects to Dash frontend for data insights."""
#     # Redirect to the Dash app running on localhost:8050
#     return redirect("http://127.0.0.1:8050", code=302)

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify, render_template, redirect, url_for
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
    return render_template('index.html')

# Record violation endpoint
@app.route('/record_violation', methods=['GET', 'POST'])
def record_violation():
    if request.method == 'POST':
        license_plate = request.form.get('license_plate')
        speed = request.form.get('speed')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')

        violation = Violation(
            license_plate=license_plate,
            speed=speed,
            latitude=latitude,
            longitude=longitude
        )

        db.session.add(violation)
        db.session.commit()
        return redirect(url_for('get_violations'))

    return render_template('record_violation.html')

# Get all violations
@app.route('/get_violations', methods=['GET'])
def get_violations():
    violations = Violation.query.all()
    return render_template('violations.html', violations=violations)

# User registration endpoint
@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'User already exists'}), 400

        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login_user'))

    return render_template('register.html')

# User login endpoint
@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            return redirect(url_for('home'))
        return jsonify({'error': 'Invalid credentials'}), 401

    return render_template('login.html')

# Update violation
@app.route('/update_violation/<int:id>', methods=['GET', 'POST'])
def update_violation(id):
    violation = Violation.query.get_or_404(id)
    if request.method == 'POST':
        violation.license_plate = request.form.get('license_plate')
        violation.speed = request.form.get('speed')
        violation.latitude = request.form.get('latitude')
        violation.longitude = request.form.get('longitude')

        db.session.commit()
        return redirect(url_for('get_violations'))

    return render_template('update_violation.html', violation=violation)

# Delete violation
@app.route('/delete_violation/<int:id>', methods=['GET'])
def delete_violation(id):
    violation = Violation.query.get_or_404(id)
    db.session.delete(violation)
    db.session.commit()
    return redirect(url_for('get_violations'))

if __name__ == '__main__':
    app.run(debug=True)
