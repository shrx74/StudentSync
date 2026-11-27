from decimal import Decimal
import pytest

from finance_summary import summarize, savings_progress


# Test 1: Financial totals
def test_financial_totals():
    incomes = [{"amount": 500}, {"amount": 300}]
    expenses = [{"amount": 150}]

    result = summarize(incomes, expenses)

    assert result["total_income"] == Decimal("800")
    assert result["total_expenses"] == Decimal("150")
    assert result["balance"] == Decimal("650")


# Test 2: Empty financial records
def test_empty_financial_records():
    result = summarize([], [])

    assert result["total_income"] == Decimal("0")
    assert result["total_expenses"] == Decimal("0")
    assert result["balance"] == Decimal("0")


# Test 3: Normal savings progress
def test_savings_progress():
    contributions = [{"amount": 100}, {"amount": 150}]

    result = savings_progress(500, contributions)

    assert result["total_saved"] == Decimal("250")
    assert result["percent"] == 50


# Test 4: Savings exceed target
def test_savings_exceed_target():
    result = savings_progress(500, [{"amount": 600}])

    assert result["total_saved"] == Decimal("600")
    assert result["percent"] == 100


# Test 5: No savings contributions
def test_empty_contributions():
    result = savings_progress(500, [])

    assert result["total_saved"] == Decimal("0")
    assert result["percent"] == 0


# Test 6: Invalid savings target
def test_invalid_target():
    with pytest.raises(ValueError):
        savings_progress(0, [])
