"""This script defines a Flask Blueprint main_bp that includes routes for managing vehicle violations, viewing statistics, and exporting violation data. It registers the auth_bp blueprint for authentication, allowing routes under /auth/* for user login and registration. The routes in main_bp include recording a violation (/record_violation), retrieving violation statistics (/violation_statistics), and exporting violation data (/export_violations), with error handling and user authentication through the @login_required decorator ensuring secure access.
"""

from flask import Blueprint, request, jsonify
from models import Violation, db
from analytics import get_violation_statistics
from notifications import notify_user
from flask_login import login_required
from auth import auth_bp

main_bp = Blueprint('main', __name__)

# Registering Authentication Blueprint
main_bp.register_blueprint(auth_bp, url_prefix='/auth')

@main_bp.route('/record_violation', methods=['POST'])
@login_required
def record_violation():
    data = request.json
    license_plate = data.get('license_plate')
    speed = data.get('speed')

    if not license_plate or not isinstance(speed, (int, float)):
        return jsonify({'error': 'Invalid input'}), 400

    try:
        new_violation = Violation(license_plate=license_plate, speed=speed, user_id=None)
        db.session.add(new_violation)
        db.session.commit()
        notify_user(license_plate, speed)
        return jsonify({'message': 'Violation recorded successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main_bp.route('/violation_statistics', methods=['GET'])
@login_required
def violation_statistics():
    try:
        stats = get_violation_statistics()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route('/export_violations', methods=['GET'])
@login_required
def export_violations():
    try:
        violations = Violation.query.all()
        data = [{"id": v.id, "license_plate": v.license_plate, "speed": v.speed, "timestamp": v.timestamp} for v in violations]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
