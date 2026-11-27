from datetime import datetime, timezone

from flask import Blueprint, jsonify

from models.assignment import Assignment
from reminders import get_reminders
from repositories.academic_repository import AcademicRepository
from repositories.user_repository import UserRepository


reminder_bp = Blueprint("reminders", __name__)
academic = AcademicRepository()
users = UserRepository()


def reminder_list(user_id):
    assignments = [
        Assignment(task["title"], task["due_date"], task["status"])
        for task in academic.get_tasks(user_id)
    ]

    reminders = get_reminders(assignments, datetime.now(timezone.utc))

    return [
        {
            "title": assignment.title,
            "due_date": assignment.due_date.isoformat(),
            "status": assignment.status
        }
        for assignment in reminders
    ]


@reminder_bp.get("/users/<int:user_id>/reminders")
def user_reminders(user_id):
    if users.find_by_id(user_id) is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify(reminder_list(user_id))
