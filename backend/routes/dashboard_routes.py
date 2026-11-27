from datetime import date

from flask import Blueprint, jsonify

from repositories.academic_repository import AcademicRepository
from repositories.user_repository import UserRepository
from repositories.work_repository import WorkRepository
from routes.reminder_routes import reminder_list
from utils import calculate_earnings


dashboard_bp = Blueprint("dashboard", __name__)
users = UserRepository()
academic = AcademicRepository()
work = WorkRepository()


def todays_schedule(user_id, today):
    schedule = []

    for meeting in academic.get_class_meetings(user_id):
        meets_today = meeting["day_of_week"] == today.isoweekday()
        in_term = meeting["start_date"] <= today <= meeting["end_date"]

        if meets_today and in_term:
            schedule.append({
                "type": "Class",
                "title": meeting["course_code"],
                "start": meeting["start_time"].strftime("%H:%M"),
                "end": meeting["end_time"].strftime("%H:%M")
            })

    for shift in work.get_shifts(user_id):
        if shift["start_time"].date() == today:
            shift = calculate_earnings(shift)
            schedule.append({
                "type": "Work Shift",
                "title": shift["employer"],
                "start": shift["start_time"].strftime("%H:%M"),
                "end": shift["end_time"].strftime("%H:%M"),
                "estimated_earnings": shift["estimated_earnings"]
            })

    return sorted(schedule, key=lambda item: item["start"])


@dashboard_bp.get("/users/<int:user_id>/dashboard")
def dashboard(user_id):
    if users.find_by_id(user_id) is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "schedule": todays_schedule(user_id, date.today()),
        "reminders": reminder_list(user_id)
    })
