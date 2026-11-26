from unittest.mock import patch

from app import create_app


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
