from datetime import datetime
from flask import Blueprint, request, jsonify

from repositories.study_repository import StudyRepository
from repositories.academic_repository import AcademicRepository
from utils import get_data, check_text


study_bp = Blueprint("study", __name__)
study = StudyRepository()
academic = AcademicRepository()


# Validate study session details
def check_study_session(data):
    check_text(data["title"], 150)

    try:
        start = datetime.fromisoformat(data["start_time"])
        end = datetime.fromisoformat(data["end_time"])

        if end <= start:
            raise ValueError("End time must be after start time")

    except TypeError:
        raise ValueError("Invalid study session time")


# Convert datetime objects into JSON-friendly strings
def session_json(session):
    result = dict(session)

    for field in ("start_time", "end_time"):
        if isinstance(result.get(field), datetime):
            result[field] = result[field].isoformat()

    return result


# Retrieve or create study sessions
@study_bp.route(
    "/users/<int:user_id>/study-sessions",
    methods=["GET", "POST"]
)
def study_sessions(user_id):

    if request.method == "GET":
        sessions = study.get_study_sessions(user_id)

        return jsonify([
            session_json(session) for session in sessions
        ])

    data = get_data([
        "title", "start_time", "end_time"
    ])

    check_study_session(data)

    course_id = data.get("course_id")

    if course_id is not None:
        if type(course_id) is not int:
            raise ValueError("Invalid course ID")

        if academic.get_course(user_id, course_id) is None:
            return jsonify({"error": "Course not found"}), 404

    if data.get("notes") is not None:
        if not isinstance(data["notes"], str):
            raise ValueError("Invalid notes")

    session = study.create_study_session(user_id, data)

    if session is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify(session_json(session)), 201


# Delete a study session
@study_bp.route(
    "/users/<int:user_id>/study-sessions/<int:session_id>",
    methods=["DELETE"]
)
def delete_study_session(user_id, session_id):

    result = study.delete_study_session(user_id, session_id)

    if result is None:
        return jsonify({"error": "Study session not found"}), 404

    return jsonify(result)
