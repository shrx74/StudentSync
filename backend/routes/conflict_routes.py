from flask import Blueprint, jsonify
from conflict_service import ConflictService

conflict_bp = Blueprint("conflicts", __name__)


@conflict_bp.get("/users/<int:user_id>/conflicts")
def get_conflicts(user_id):
    service = ConflictService()
    conflicts = service.get_conflicts(user_id)

    return jsonify({
        "user_id": user_id,
        "conflicts": conflicts
    })
