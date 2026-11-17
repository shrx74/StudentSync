
from flask import Blueprint, jsonify

from repositories.user_repository import UserRepository
from utils import get_data


user_bp = Blueprint("users", __name__)
repo = UserRepository()


# Create user
@user_bp.route("/users", methods=["POST"])
def create_user():
    data = get_data(["full_name", "email"])

    user = repo.create_user(
        data["full_name"], data["email"]
    )

    return jsonify({
        "user_id": user.user_id,
        "full_name": user.full_name,
        "email": user.email
    }), 201


# Find user by ID
@user_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = repo.find_by_id(user_id)

    if user is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "user_id": user.user_id,
        "full_name": user.full_name,
        "email": user.email
    })
