import pytest
from datetime import datetime

from utils import check_period, check_task, check_job, check_shift, calculate_earnings


# Test 1: Check valid semester dates
def test_valid_period():
    check_period("2026-09-01", "2026-12-20")


# Test 2: Check invalid semester dates
def test_invalid_period():
    with pytest.raises(ValueError):
        check_period("2026-12-20", "2026-09-01")


# Test 3: Check invalid academic task status
def test_invalid_task():
    data = {
        "due_date": "2026-11-25T23:59:00",
        "status": "invalid"
    }

    with pytest.raises(ValueError):
        check_task(data)


# Test 4: Check invalid hourly wage
def test_invalid_job():
    data = {
        "hourly_wage": -5
    }

    with pytest.raises(ValueError):
        check_job(data)


# Test 5: Check invalid shift break
def test_invalid_shift():
    data = {
        "start_time": "2026-11-16T16:00:00",
        "end_time": "2026-11-16T22:00:00",
        "break_minutes": 400,
        "break_paid": False
    }

    with pytest.raises(ValueError):
        check_shift(data)


# Test 6: Check calculated earnings
def test_calculate_earnings():
    shift = {
        "start_time": datetime(2026, 11, 16, 16, 0),
        "end_time": datetime(2026, 11, 16, 22, 0),
        "break_minutes": 30,
        "break_paid": False,
        "hourly_wage": 18
    }

    result = calculate_earnings(shift)

    assert result["paid_hours"] == 5.5
    assert result["estimated_earnings"] == 99.0
