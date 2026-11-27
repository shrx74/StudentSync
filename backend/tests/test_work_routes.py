from datetime import datetime
from unittest.mock import patch

from app import create_app


JOB = {
    "job_id": 1,
    "user_id": 1,
    "employer": "Campus Library",
    "hourly_wage": 18
}

SHIFT = {
    "shift_id": 1,
    "job_id": 1,
    "start_time": datetime(2026, 11, 16, 16, 0),
    "end_time": datetime(2026, 11, 16, 22, 0),
    "break_minutes": 30,
    "break_paid": False,
    "hourly_wage": 18
}


@patch("routes.work_routes.work")
def test_get_jobs(mock_work):
    mock_work.get_jobs.return_value = [JOB]
    client = create_app().test_client()

    response = client.get("/users/1/jobs")

    assert response.status_code == 200
    assert response.get_json()[0]["employer"] == "Campus Library"


@patch("routes.work_routes.work")
def test_create_job(mock_work):
    mock_work.create_job.return_value = JOB
    client = create_app().test_client()

    response = client.post("/users/1/jobs", json={
        "employer": "Campus Library",
        "hourly_wage": 18
    })

    assert response.status_code == 201
    mock_work.create_job.assert_called_once()


@patch("routes.work_routes.work")
def test_create_job_negative_wage(mock_work):
    client = create_app().test_client()

    response = client.post("/users/1/jobs", json={
        "employer": "Campus Library",
        "hourly_wage": -5
    })

    assert response.status_code == 400
    mock_work.create_job.assert_not_called()


@patch("routes.work_routes.work")
def test_create_job_user_not_found(mock_work):
    mock_work.create_job.return_value = None
    client = create_app().test_client()

    response = client.post("/users/99/jobs", json={
        "employer": "Campus Library",
        "hourly_wage": 18
    })

    assert response.status_code == 404


@patch("routes.work_routes.work")
def test_create_shift_returns_earnings(mock_work):
    mock_work.create_shift.return_value = {"shift_id": 1}
    mock_work.get_shift.return_value = SHIFT
    client = create_app().test_client()

    response = client.post("/users/1/shifts", json={
        "job_id": 1,
        "start_time": "2026-11-16T16:00:00",
        "end_time": "2026-11-16T22:00:00",
        "break_minutes": 30
    })

    assert response.status_code == 201
    assert response.get_json()["paid_hours"] == 5.5
    assert response.get_json()["estimated_earnings"] == 99.0


@patch("routes.work_routes.work")
def test_create_shift_end_before_start(mock_work):
    client = create_app().test_client()

    response = client.post("/users/1/shifts", json={
        "job_id": 1,
        "start_time": "2026-11-16T22:00:00",
        "end_time": "2026-11-16T16:00:00"
    })

    assert response.status_code == 400
    mock_work.create_shift.assert_not_called()


@patch("routes.work_routes.work")
def test_create_shift_job_not_found(mock_work):
    mock_work.create_shift.return_value = None
    client = create_app().test_client()

    response = client.post("/users/1/shifts", json={
        "job_id": 99,
        "start_time": "2026-11-16T16:00:00",
        "end_time": "2026-11-16T22:00:00"
    })

    assert response.status_code == 404


@patch("routes.work_routes.work")
def test_get_missing_shift(mock_work):
    mock_work.get_shift.return_value = None
    client = create_app().test_client()

    response = client.get("/users/1/shifts/99")

    assert response.status_code == 404


@patch("routes.work_routes.work")
def test_delete_missing_shift(mock_work):
    mock_work.delete_shift.return_value = None
    client = create_app().test_client()

    response = client.delete("/users/1/shifts/99")

    assert response.status_code == 404
