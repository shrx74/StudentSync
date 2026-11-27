from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from app import create_app


def task(title, hours_from_now, status="pending"):
    return {
        "task_id": 1,
        "user_id": 1,
        "title": title,
        "due_date": datetime.now(timezone.utc) + timedelta(hours=hours_from_now),
        "status": status
    }


@patch("routes.reminder_routes.users")
@patch("routes.reminder_routes.academic")
def test_only_tasks_due_within_48_hours(mock_academic, mock_users):
    mock_users.find_by_id.return_value = {"user_id": 1}
    mock_academic.get_tasks.return_value = [
        task("Lab 5", 5),
        task("Essay", 72)
    ]
    client = create_app().test_client()

    response = client.get("/users/1/reminders")

    assert response.status_code == 200
    assert len(response.get_json()) == 1
    assert response.get_json()[0]["title"] == "Lab 5"


@patch("routes.reminder_routes.users")
@patch("routes.reminder_routes.academic")
def test_completed_task_has_no_reminder(mock_academic, mock_users):
    mock_users.find_by_id.return_value = {"user_id": 1}
    mock_academic.get_tasks.return_value = [task("Lab 5", 5, "completed")]
    client = create_app().test_client()

    response = client.get("/users/1/reminders")

    assert response.status_code == 200
    assert response.get_json() == []


@patch("routes.reminder_routes.users")
@patch("routes.reminder_routes.academic")
def test_past_due_task_has_no_reminder(mock_academic, mock_users):
    mock_users.find_by_id.return_value = {"user_id": 1}
    mock_academic.get_tasks.return_value = [task("Lab 4", -2)]
    client = create_app().test_client()

    response = client.get("/users/1/reminders")

    assert response.get_json() == []


@patch("routes.reminder_routes.users")
@patch("routes.reminder_routes.academic")
def test_reminders_user_not_found(mock_academic, mock_users):
    mock_users.find_by_id.return_value = None
    client = create_app().test_client()

    response = client.get("/users/99/reminders")

    assert response.status_code == 404
    mock_academic.get_tasks.assert_not_called()
