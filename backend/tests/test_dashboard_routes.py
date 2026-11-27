from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from app import create_app


def task(title, hours_from_now):
    return {
        "title": title,
        "due_date": datetime.now(timezone.utc) + timedelta(hours=hours_from_now),
        "status": "pending"
    }


@patch("routes.dashboard_routes.users")
def test_dashboard_user_not_found(mock_users):
    mock_users.find_by_id.return_value = None
    client = create_app().test_client()

    response = client.get("/users/99/dashboard")

    assert response.status_code == 404


@patch("routes.reminder_routes.academic")
@patch("routes.dashboard_routes.users")
def test_dashboard_reminders(mock_users, mock_academic):
    mock_users.find_by_id.return_value = {"user_id": 1}
    mock_academic.get_tasks.return_value = [
        task("Lab 5", 5),
        task("Essay", 72)
    ]
    client = create_app().test_client()

    response = client.get("/users/1/dashboard")
    reminders = response.get_json()["reminders"]

    assert response.status_code == 200
    assert [r["title"] for r in reminders] == ["Lab 5"]
