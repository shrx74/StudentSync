import pytest
from datetime import datetime

from utils import check_period, check_task, check_job, check_shift, calculate_earnings
from utils import (
    check_income, check_expense,
    check_savings_target, check_contribution,
    check_category
)

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

# Test 7: Check valid income
def test_valid_income():
    check_income({
        "source": "Salary",
        "amount": 500,
        "income_date": "2026-11-27"
    })

# Test 8: Check invalid income
@pytest.mark.parametrize("amount", [0, -50, "bad", "NaN"])
def test_invalid_income(amount):
    with pytest.raises(ValueError):
        check_income({
            "source": "Salary",
            "amount": amount,
            "income_date": "2026-11-27"
        })

# Test 9: Check invalid expense
def test_invalid_expense():
    with pytest.raises(ValueError):
        check_expense({
            "category_id": 1,
            "description": "Food",
            "amount": 0,
            "expense_date": "2026-11-27"
        })

# Test 10: Check invalid finance date
def test_invalid_finance_date():
    with pytest.raises(ValueError):
        check_income({
            "source": "Salary",
            "amount": 500,
            "income_date": "invalid"
        })

# Test 11: Check invalid savings target
def test_invalid_savings_target():
    with pytest.raises(ValueError):
        check_savings_target({
            "target_name": "Laptop",
            "target_amount": 0
        })

# Test 12: Check invalid contribution
def test_invalid_contribution():
    with pytest.raises(ValueError):
        check_contribution({
            "amount": -100,
            "contribution_date": "2026-11-27"
        })

# Test 13: Check invalid category
def test_invalid_category():
    with pytest.raises(ValueError):
        check_category({"category_name": " "})