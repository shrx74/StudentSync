from flask import Blueprint, jsonify

from repositories.user_repository import UserRepository
from routes.reminder_routes import reminder_list


dashboard_bp = Blueprint("dashboard", __name__)
users = UserRepository()


@dashboard_bp.get("/users/<int:user_id>/dashboard")
def dashboard(user_id):
    if users.find_by_id(user_id) is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "reminders": reminder_list(user_id)
    })
