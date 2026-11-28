from unittest.mock import patch

from app import create_app
from datetime import date, time

TASK = {
    "task_id": 1,
    "user_id": 1,
    "title": "Lab 5",
    "due_date": "2026-11-28T23:59:00",
    "status": "pending"
}


# Test 1: Get all tasks for a user
@patch("routes.academic_routes.academic")
def test_get_tasks(mock_academic):
    mock_academic.get_tasks.return_value = [TASK]
    client = create_app().test_client()

    response = client.get("/users/1/tasks")

    assert response.status_code == 200
    assert response.get_json()[0]["title"] == "Lab 5"


# Test 2: Create a valid task
@patch("routes.academic_routes.repo")
@patch("routes.academic_routes.academic")
def test_create_task(mock_academic, mock_repo):
    mock_repo.find_by_id.return_value = {"user_id": 1}
    mock_academic.create_task.return_value = TASK
    client = create_app().test_client()

    response = client.post("/users/1/tasks", json={
        "title": "Lab 5",
        "due_date": "2026-11-28T23:59:00"
    })

    assert response.status_code == 201
    mock_academic.create_task.assert_called_once()


# Test 3: Reject a task with no title
@patch("routes.academic_routes.academic")
def test_create_task_without_title(mock_academic):
    client = create_app().test_client()

    response = client.post("/users/1/tasks", json={
        "due_date": "2026-11-28T23:59:00"
    })

    assert response.status_code == 400
    mock_academic.create_task.assert_not_called()


# Test 4: Reject a task with an invalid status
@patch("routes.academic_routes.academic")
def test_create_task_invalid_status(mock_academic):
    client = create_app().test_client()

    response = client.post("/users/1/tasks", json={
        "title": "Lab 5",
        "due_date": "2026-11-28T23:59:00",
        "status": "done"
    })

    assert response.status_code == 400
    mock_academic.create_task.assert_not_called()


# Test 5: Return 404 when the user does not exist
@patch("routes.academic_routes.repo")
@patch("routes.academic_routes.academic")
def test_create_task_user_not_found(mock_academic, mock_repo):
    mock_repo.find_by_id.return_value = None
    client = create_app().test_client()

    response = client.post("/users/99/tasks", json={
        "title": "Lab 5",
        "due_date": "2026-11-28T23:59:00"
    })

    assert response.status_code == 404


# Test 6: Return 404 when deleting a task that does not exist
@patch("routes.academic_routes.academic")
def test_delete_missing_task(mock_academic):
    mock_academic.delete_task.return_value = None
    client = create_app().test_client()

    response = client.delete("/users/1/tasks/99")

    assert response.status_code == 404


MEETING_DATA = {
    "day_of_week": 1,
    "start_time": "10:00",
    "end_time": "11:00",
    "start_date": "2026-09-09",
    "end_date": "2026-12-04",
    "location": "Room 101"
}


MEETING = {
    "meeting_id": 1,
    "course_id": 5,
    "day_of_week": 1,
    "start_time": time(10, 0),
    "end_time": time(11, 0),
    "start_date": date(2026, 9, 9),
    "end_date": date(2026, 12, 4),
    "location": "Room 101"
}

@patch("routes.academic_routes.academic")
def test_create_meeting(mock_academic):
    mock_academic.create_class_meeting.return_value = MEETING
    client = create_app().test_client()

    response = client.post(
        "/users/1/courses/5/meetings",
        json=MEETING_DATA
    )

    assert response.status_code == 201
    assert response.get_json()["meeting_id"] == 1
    assert response.get_json()["start_time"] == "10:00"

    mock_academic.create_class_meeting.assert_called_once_with(
        1, dict(MEETING_DATA, course_id=5)
    )

@patch("routes.academic_routes.academic")
def test_create_meeting_invalid_day(mock_academic):
    client = create_app().test_client()

    data = dict(MEETING_DATA)
    data["day_of_week"] = 8

    response = client.post(
        "/users/1/courses/5/meetings",
        json=data
    )

    assert response.status_code == 400
    mock_academic.create_class_meeting.assert_not_called()

@patch("routes.academic_routes.academic")
def test_get_missing_meeting(mock_academic):
    mock_academic.get_class_meeting.return_value = None
    client = create_app().test_client()

    response = client.get("/users/1/meetings/99")

    assert response.status_code == 404

@patch("routes.academic_routes.academic")
def test_get_meetings(mock_academic):
    mock_academic.get_course.return_value = {
        "course_id": 5
    }

    other_meeting = dict(MEETING)
    other_meeting["course_id"] = 6
    other_meeting["meeting_id"] = 2

    mock_academic.get_class_meetings.return_value = [
        MEETING, other_meeting
    ]

    client = create_app().test_client()

    response = client.get(
        "/users/1/courses/5/meetings"
    )

    assert response.status_code == 200
    assert len(response.get_json()) == 1
    assert response.get_json()[0]["course_id"] == 5

@patch("routes.academic_routes.academic")
def test_get_meeting(mock_academic):
    mock_academic.get_class_meeting.return_value = MEETING
    client = create_app().test_client()

    response = client.get("/users/1/meetings/1")

    assert response.status_code == 200
    assert response.get_json()["meeting_id"] == 1

@patch("routes.academic_routes.academic")
def test_update_meeting(mock_academic):
    updated = dict(MEETING)
    updated["day_of_week"] = 2

    mock_academic.update_class_meeting.return_value = updated

    client = create_app().test_client()

    data = dict(MEETING_DATA)
    data["day_of_week"] = 2

    response = client.put(
        "/users/1/meetings/1",
        json=data
    )

    assert response.status_code == 200
    assert response.get_json()["day_of_week"] == 2

    mock_academic.update_class_meeting.assert_called_once_with(
        1, 1, data
    )

@patch("routes.academic_routes.academic")
def test_delete_meeting(mock_academic):
    mock_academic.delete_class_meeting.return_value = {
        "meeting_id": 1
    }

    client = create_app().test_client()

    response = client.delete("/users/1/meetings/1")

    assert response.status_code == 200
    assert response.get_json()["meeting_id"] == 1
