from datetime import datetime, timedelta

import pytest

from models.assignment import Assignment
from reminders import get_reminders

# Test time for reference
NOW = datetime(2026, 11, 17, 12, 0)


# Test 1: Due in 47 hours gets a reminder
def test_due_within_48_hours():
    assignment = Assignment("Lab 4", NOW + timedelta(hours=47))

    assert get_reminders([assignment], NOW) == [assignment]


# Test 2: Due in 49 hours is too far 
def test_due_after_48_hours():
    assignment = Assignment("Lab 5", NOW + timedelta(hours=49))

    assert get_reminders([assignment], NOW) == []


# Test 3: Completed assignment gets no reminder
def test_completed_assignment():
    assignment = Assignment("Lab 4", NOW + timedelta(hours=5), "completed")

    assert get_reminders([assignment], NOW) == []


# Test 4: Past due assignment gets no reminder
def test_past_due_assignment():
    assignment = Assignment("Lab 3", NOW - timedelta(hours=1))

    assert get_reminders([assignment], NOW) == []


# Test 5: Assignment with no due date gets no reminder
def test_no_due_date():
    assignment = Assignment("Reading")

    assert get_reminders([assignment], NOW) == []


# Test 6: Empty title is rejected
def test_empty_title():
    with pytest.raises(ValueError):
        Assignment("", NOW)


# Test 7: Due date that is not a datetime is rejected
def test_invalid_due_date():
    with pytest.raises(ValueError):
        Assignment("Lab 4", "tomorrow")
