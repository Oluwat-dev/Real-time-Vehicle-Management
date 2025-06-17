"""This script defines a function get_violation_statistics() that calculates and returns statistics about vehicle violations. It queries the Violation model to get the total count of violations and the average speed of violations using SQLAlchemy. The function returns a dictionary containing the total number of violations and the average speed, rounding the average speed to two decimal places (or returning 0 if no violations exist)."""

#IMPORT DEPENDENCIES
from models import Violation
from app import db

#GET_VIOLATION_STATISTICS FUNCTIONS DEFINED0
def get_violation_statistics():
    total_violations = Violation.query.count()
    average_speed = db.session.query(db.func.avg(Violation.speed)).scalar()
    return {
        'total_violations': total_violations,
        'average_speed': round(average_speed, 2) if average_speed else 0
    }
