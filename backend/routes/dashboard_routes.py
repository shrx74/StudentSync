from datetime import date

from flask import Blueprint, jsonify

from conflict_service import ConflictService
from finance_summary import savings_progress, summarize
from repositories.academic_repository import AcademicRepository
from repositories.budget_repository import BudgetRepository
from repositories.user_repository import UserRepository
from repositories.work_repository import WorkRepository
from routes.budget_routes import finance_json
from routes.reminder_routes import reminder_list
from utils import calculate_earnings


dashboard_bp = Blueprint("dashboard", __name__)
users = UserRepository()
academic = AcademicRepository()
work = WorkRepository()
budget = BudgetRepository()


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
        start = shift["start_time"].astimezone()
        end = shift["end_time"].astimezone()

        if start.date() == today:
            schedule.append({
                "type": "Work Shift",
                "title": shift["employer"],
                "start": start.strftime("%H:%M"),
                "end": end.strftime("%H:%M"),
                "estimated_earnings": calculate_earnings(shift)["estimated_earnings"]
            })

    return sorted(schedule, key=lambda item: item["start"])


def finance_overview(user_id):
    incomes = budget.get_incomes(user_id)
    expenses = budget.get_expenses(user_id)
    targets = []

    for target in budget.get_savings_targets(user_id):
        contributions = budget.get_contributions(user_id, target["target_id"])
        target = finance_json(target)
        target.update(finance_json(savings_progress(target["target_amount"], contributions)))
        target["contributions"] = [finance_json(contribution) for contribution in contributions]
        targets.append(target)

    overview = finance_json(summarize(incomes, expenses))
    overview["incomes"] = [finance_json(income) for income in incomes]
    overview["expenses"] = [finance_json(expense) for expense in expenses]
    overview["savings_targets"] = targets

    return overview


@dashboard_bp.get("/users/<int:user_id>/dashboard")
def dashboard(user_id):
    if users.find_by_id(user_id) is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "schedule": todays_schedule(user_id, date.today()),
        "conflicts": ConflictService().get_conflicts(user_id),
        "reminders": reminder_list(user_id),
        "finance": finance_overview(user_id)
    })
