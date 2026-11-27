from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal
from unittest.mock import patch

from app import create_app


TODAY = date.today()
TOMORROW = TODAY + timedelta(days=1)


def task(title, hours_from_now):
    return {
        "title": title,
        "due_date": datetime.now(timezone.utc) + timedelta(hours=hours_from_now),
        "status": "pending"
    }


def meeting(course_code, day, start, end_date=TOMORROW):
    return {
        "course_code": course_code,
        "day_of_week": day.isoweekday(),
        "start_time": time(start, 0),
        "end_time": time(start + 1, 0),
        "start_date": TODAY - timedelta(days=30),
        "end_date": end_date
    }


def shift(employer, day, start, end):
    return {
        "employer": employer,
        "start_time": datetime.combine(day, time(start, 0)),
        "end_time": datetime.combine(day, time(end, 0)),
        "break_minutes": 30,
        "break_paid": False,
        "hourly_wage": 18
    }


def get_dashboard(tasks=(), meetings=(), shifts=(), conflicts=(), incomes=(), expenses=(), targets=(), contributions=()):
    with patch("routes.dashboard_routes.users") as mock_users, \
            patch("routes.dashboard_routes.academic") as mock_academic, \
            patch("routes.dashboard_routes.work") as mock_work, \
            patch("routes.dashboard_routes.ConflictService") as mock_service, \
            patch("routes.dashboard_routes.budget") as mock_budget, \
            patch("routes.reminder_routes.academic") as mock_tasks:
        mock_users.find_by_id.return_value = {"user_id": 1}
        mock_service.return_value.get_conflicts.return_value = list(conflicts)
        mock_budget.get_incomes.return_value = list(incomes)
        mock_budget.get_expenses.return_value = list(expenses)
        mock_budget.get_savings_targets.return_value = list(targets)
        mock_budget.get_contributions.return_value = list(contributions)
        mock_tasks.get_tasks.return_value = list(tasks)
        mock_academic.get_class_meetings.return_value = list(meetings)
        mock_work.get_shifts.return_value = list(shifts)

        return create_app().test_client().get("/users/1/dashboard")


@patch("routes.dashboard_routes.users")
def test_dashboard_user_not_found(mock_users):
    mock_users.find_by_id.return_value = None
    client = create_app().test_client()

    response = client.get("/users/99/dashboard")

    assert response.status_code == 404


def test_dashboard_reminders():
    response = get_dashboard(tasks=[task("Lab 5", 5), task("Essay", 72)])
    reminders = response.get_json()["reminders"]

    assert response.status_code == 200
    assert [r["title"] for r in reminders] == ["Lab 5"]


def test_schedule_only_shows_today():
    response = get_dashboard(
        meetings=[meeting("CS2043", TODAY, 10), meeting("MATH1503", TOMORROW, 9)],
        shifts=[shift("Campus Library", TODAY, 16, 22), shift("Campus Library", TOMORROW, 8, 12)]
    )
    schedule = response.get_json()["schedule"]

    assert [item["title"] for item in schedule] == ["CS2043", "Campus Library"]
    assert [item["type"] for item in schedule] == ["Class", "Work Shift"]


def test_schedule_skips_class_after_term_ends():
    yesterday = TODAY - timedelta(days=1)

    response = get_dashboard(meetings=[meeting("CS2043", TODAY, 10, end_date=yesterday)])

    assert response.get_json()["schedule"] == []


def test_schedule_shift_earnings():
    response = get_dashboard(shifts=[shift("Campus Library", TODAY, 16, 22)])
    item = response.get_json()["schedule"][0]

    assert item["start"] == "16:00"
    assert item["end"] == "22:00"
    assert item["estimated_earnings"] == 99.0


def test_dashboard_conflicts():
    conflict = {"study_session": "Calculus Review", "work_shift": "Campus Library"}

    response = get_dashboard(conflicts=[conflict])

    assert response.get_json()["conflicts"] == [conflict]


def test_dashboard_no_conflicts():
    response = get_dashboard()

    assert response.get_json()["conflicts"] == []


def test_dashboard_finance_lists():
    income = {"income_id": 1, "source": "Salary", "amount": Decimal("1200.00"), "income_date": TODAY}
    expense = {"expense_id": 1, "description": "Rent", "amount": Decimal("600.50"),
               "expense_date": TODAY, "category_name": "Rent"}

    response = get_dashboard(incomes=[income], expenses=[expense])
    finance = response.get_json()["finance"]

    assert finance["incomes"][0]["amount"] == 1200.0
    assert finance["incomes"][0]["income_date"] == TODAY.isoformat()
    assert finance["expenses"][0]["amount"] == 600.5


def test_dashboard_savings_target_contributions():
    target = {"target_id": 3, "target_name": "New Laptop", "target_amount": Decimal("1500.00")}
    contribution = {"contribution_id": 1, "target_id": 3, "amount": Decimal("200.00"),
                    "contribution_date": TODAY}

    response = get_dashboard(targets=[target], contributions=[contribution])
    saved = response.get_json()["finance"]["savings_targets"][0]

    assert saved["target_name"] == "New Laptop"
    assert saved["contributions"][0]["amount"] == 200.0


def test_dashboard_empty_finance():
    response = get_dashboard()

    assert response.get_json()["finance"] == {
        "incomes": [],
        "expenses": [],
        "savings_targets": []
    }
