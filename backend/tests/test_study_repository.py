from unittest.mock import patch

from repositories.study_repository import StudyRepository


# Test 1: Create a study session
@patch("repositories.study_repository.query")
def test_create_study_session(mock_query):
    repository = StudyRepository()

    data = {
        "title": "Calculus Review",
        "start_time": "2026-11-30T10:00:00",
        "end_time": "2026-11-30T11:00:00"
    }

    mock_query.return_value = {
        "session_id": 1,
        "user_id": 1,
        **data
    }

    result = repository.create_study_session(1, data)

    assert result["session_id"] == 1
    assert result["title"] == "Calculus Review"

    mock_query.assert_called_once()
    assert mock_query.call_args.args[1] == (
        None, data["title"], data["start_time"],
        data["end_time"], None, 1
    )


# Test 2: Retrieve study sessions
@patch("repositories.study_repository.query")
def test_get_study_sessions(mock_query):
    repository = StudyRepository()

    mock_query.return_value = [
        {"session_id": 1, "title": "Calculus Review"},
        {"session_id": 2, "title": "Java Practice"}
    ]

    result = repository.get_study_sessions(1)

    assert len(result) == 2
    assert result[0]["title"] == "Calculus Review"

    mock_query.assert_called_once()
    assert mock_query.call_args.args[1] == (1,)
    assert mock_query.call_args.args[2] is True


# Test 3: Delete a study session
@patch("repositories.study_repository.query")
def test_delete_study_session(mock_query):
    repository = StudyRepository()

    mock_query.return_value = {"session_id": 1}

    result = repository.delete_study_session(1, 1)

    assert result["session_id"] == 1

    mock_query.assert_called_once()
    assert mock_query.call_args.args[1] == (1, 1)
