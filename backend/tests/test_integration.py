import os
from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from app import create_app
from database.connection import Database


pytestmark = pytest.mark.skipif(
    not os.getenv("DATABASE_URL") and not os.getenv("DB_HOST"),
    reason="needs a database connection in backend/.env"
)


@pytest.fixture
def client():
    return create_app().test_client()


@pytest.fixture
def user_id(client):
    email = f"integration-{uuid4().hex[:8]}@test.ca"
    response = client.post("/users", json={"full_name": "Integration Test", "email": email})
    user_id = response.get_json()["user_id"]

    yield user_id

    with Database.connect() as connection:
        connection.execute("DELETE FROM users WHERE user_id = %s", (user_id,))


def post(client, path, data):
    response = client.post(path, json=data)
    assert response.status_code == 201, response.get_json()
    return response.get_json()


def test_dashboard_shows_data_entered_through_routes(client, user_id):
    base = f"/users/{user_id}"
    now = datetime.now().astimezone()
    shift_start = now.replace(hour=10, minute=0, second=0, microsecond=0)

    job = post(client, f"{base}/jobs", {"employer": "Test Cafe", "hourly_wage": 20})
    post(client, f"{base}/shifts", {
        "job_id": job["job_id"],
        "start_time": shift_start.isoformat(),
        "end_time": (shift_start + timedelta(hours=4)).isoformat()
    })
    post(client, f"{base}/study-sessions", {
        "title": "Exam Review",
        "start_time": (shift_start + timedelta(hours=2)).isoformat(),
        "end_time": (shift_start + timedelta(hours=3)).isoformat()
    })
    post(client, f"{base}/tasks", {
        "title": "Lab Report",
        "due_date": (now + timedelta(hours=5)).isoformat()
    })
    post(client, f"{base}/incomes", {
        "source": "Paycheque", "amount": 500, "income_date": now.date().isoformat()
    })
    category = post(client, f"{base}/expense-categories", {"category_name": "Food"})
    post(client, f"{base}/expenses", {
        "category_id": category["category_id"],
        "description": "Groceries",
        "amount": 120,
        "expense_date": now.date().isoformat()
    })

    response = client.get(f"{base}/dashboard")
    dashboard = response.get_json()

    assert response.status_code == 200

    shift = next(item for item in dashboard["schedule"] if item["type"] == "Work Shift")
    assert shift["title"] == "Test Cafe"
    assert shift["start"] == "10:00"
    assert shift["estimated_earnings"] == 80.0

    assert {"study_session": "Exam Review", "work_shift": "Test Cafe"} in dashboard["conflicts"]
    assert [reminder["title"] for reminder in dashboard["reminders"]] == ["Lab Report"]

    assert dashboard["finance"]["total_income"] == 500.0
    assert dashboard["finance"]["total_expenses"] == 120.0
    assert dashboard["finance"]["balance"] == 380.0
