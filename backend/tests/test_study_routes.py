from unittest.mock import patch

import pytest
from app import create_app


SESSION_DATA = {
    "title": "Calculus Review",
    "start_time": "2026-11-30T10:00:00",
    "end_time": "2026-11-30T11:00:00"
}


SESSION = {
    "session_id": 1,
    "user_id": 1,
    **SESSION_DATA
}


# Test 1: Retrieve study sessions
@patch("routes.study_routes.study")
def test_get_study_sessions(mock_study):
    mock_study.get_study_sessions.return_value = [SESSION]

    client = create_app().test_client()
    response = client.get("/users/1/study-sessions")

    assert response.status_code == 200
    assert response.get_json()[0]["title"] == "Calculus Review"

    mock_study.get_study_sessions.assert_called_once_with(1)


# Test 2: Create a valid study session
@patch("routes.study_routes.study")
def test_create_study_session(mock_study):
    mock_study.create_study_session.return_value = SESSION

    client = create_app().test_client()

    response = client.post(
        "/users/1/study-sessions",
        json=SESSION_DATA
    )

    assert response.status_code == 201
    assert response.get_json()["session_id"] == 1

    mock_study.create_study_session.assert_called_once_with(
        1, SESSION_DATA
    )


# Test 3: Reject a missing title
@patch("routes.study_routes.study")
def test_missing_title(mock_study):
    client = create_app().test_client()

    data = dict(SESSION_DATA)
    del data["title"]

    response = client.post(
        "/users/1/study-sessions",
        json=data
    )

    assert response.status_code == 400
    mock_study.create_study_session.assert_not_called()


# Tests 4-6: Reject invalid end times
@pytest.mark.parametrize("end_time", [
    "2026-11-30T09:00:00",
    "2026-11-30T10:00:00",
    "invalid-time"
])
@patch("routes.study_routes.study")
def test_invalid_end_time(mock_study, end_time):
    client = create_app().test_client()

    data = dict(SESSION_DATA)
    data["end_time"] = end_time

    response = client.post(
        "/users/1/study-sessions",
        json=data
    )

    assert response.status_code == 400
    mock_study.create_study_session.assert_not_called()


# Test 7: User does not exist
@patch("routes.study_routes.study")
def test_user_not_found(mock_study):
    mock_study.create_study_session.return_value = None

    client = create_app().test_client()

    response = client.post(
        "/users/99/study-sessions",
        json=SESSION_DATA
    )

    assert response.status_code == 404


# Test 8: Course does not belong to the user
@patch("routes.study_routes.academic")
@patch("routes.study_routes.study")
def test_course_not_found(mock_study, mock_academic):
    mock_academic.get_course.return_value = None

    client = create_app().test_client()

    data = dict(SESSION_DATA)
    data["course_id"] = 99

    response = client.post(
        "/users/1/study-sessions",
        json=data
    )

    assert response.status_code == 404
    mock_study.create_study_session.assert_not_called()


# Test 9: Delete an existing study session
@patch("routes.study_routes.study")
def test_delete_study_session(mock_study):
    mock_study.delete_study_session.return_value = {
        "session_id": 1
    }

    client = create_app().test_client()

    response = client.delete(
        "/users/1/study-sessions/1"
    )

    assert response.status_code == 200
    assert response.get_json()["session_id"] == 1

    mock_study.delete_study_session.assert_called_once_with(
        1, 1
    )


# Test 10: Delete a nonexistent study session
@patch("routes.study_routes.study")
def test_delete_missing_session(mock_study):
    mock_study.delete_study_session.return_value = None

    client = create_app().test_client()

    response = client.delete(
        "/users/1/study-sessions/99"
    )

    assert response.status_code == 404
