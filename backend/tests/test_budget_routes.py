from unittest.mock import patch
from datetime import date
from decimal import Decimal

import pytest
from psycopg.errors import UniqueViolation
from app import create_app


CASES = [
    (
        "/users/1/incomes",
        "create_income",
        "get_incomes",
        {
            "source": "Salary",
            "amount": 500,
            "income_date": "2026-11-27"
        },
        "amount", 0
    ),
    (
        "/users/1/expense-categories",
        "create_category",
        "get_categories",
        {"category_name": "Food"},
        "category_name", ""
    ),
    (
        "/users/1/expenses",
        "create_expense",
        "get_expenses",
        {
            "category_id": 1,
            "description": "Groceries",
            "amount": 50,
            "expense_date": "2026-11-27"
        },
        "amount", -50
    ),
    (
        "/users/1/savings-targets",
        "create_savings_target",
        "get_savings_targets",
        {
            "target_name": "Laptop",
            "target_amount": 1000
        },
        "target_amount", 0
    ),
    (
        "/users/1/savings-targets/1/contributions",
        "create_contribution",
        "get_contributions",
        {
            "amount": 100,
            "contribution_date": "2026-11-27"
        },
        "amount", -100
    )
]


# Test valid POST requests
@pytest.mark.parametrize(
    "url,creator,getter,data,field,bad_value", CASES
)
def test_create_finance(url, creator, getter, data, field, bad_value):
    with patch("routes.budget_routes.budget") as mock_budget:
        method = getattr(mock_budget, creator)
        method.return_value = data

        client = create_app().test_client()
        response = client.post(url, json=data)

        assert response.status_code == 201

        expected = dict(data)

        if creator == "create_contribution":
            expected["target_id"] = 1

        method.assert_called_once_with(1, expected)


# Test invalid POST requests
@pytest.mark.parametrize(
    "url,creator,getter,data,field,bad_value", CASES
)
def test_invalid_finance(url, creator, getter, data, field, bad_value):
    with patch("routes.budget_routes.budget") as mock_budget:
        invalid = dict(data)
        invalid[field] = bad_value

        client = create_app().test_client()
        response = client.post(url, json=invalid)

        assert response.status_code == 400
        getattr(mock_budget, creator).assert_not_called()


# Test GET requests
@pytest.mark.parametrize(
    "url,creator,getter,data,field,bad_value", CASES
)
def test_get_finance(url, creator, getter, data, field, bad_value):
    with patch("routes.budget_routes.budget") as mock_budget:
        method = getattr(mock_budget, getter)
        method.return_value = [data]

        client = create_app().test_client()
        response = client.get(url)

        assert response.status_code == 200
        assert response.get_json() == [data]

        if getter == "get_contributions":
            method.assert_called_once_with(1, 1)

        else:
            method.assert_called_once_with(1)


# Test missing expense category
@patch("routes.budget_routes.budget")
def test_missing_expense_category(mock_budget):
    mock_budget.create_expense.return_value = None

    client = create_app().test_client()

    response = client.post("/users/1/expenses", json={
        "category_id": 99,
        "description": "Food",
        "amount": 50,
        "expense_date": "2026-11-27"
    })

    assert response.status_code == 404


# Test deleting income
@patch("routes.budget_routes.budget")
def test_delete_income(mock_budget):
    mock_budget.delete_income.return_value = {"income_id": 1}

    client = create_app().test_client()
    response = client.delete("/users/1/incomes/1")

    assert response.status_code == 200
    mock_budget.delete_income.assert_called_once_with(1, 1)


# Test deleting expense
@patch("routes.budget_routes.budget")
def test_delete_expense(mock_budget):
    mock_budget.delete_expense.return_value = {"expense_id": 1}

    client = create_app().test_client()
    response = client.delete("/users/1/expenses/1")

    assert response.status_code == 200
    mock_budget.delete_expense.assert_called_once_with(1, 1)


# Test deleting a missing expense
@patch("routes.budget_routes.budget")
def test_delete_missing_expense(mock_budget):
    mock_budget.delete_expense.return_value = None

    client = create_app().test_client()
    response = client.delete("/users/1/expenses/99")

    assert response.status_code == 404


# Test updating savings target
@patch("routes.budget_routes.budget")
def test_update_savings_target(mock_budget):
    mock_budget.update_savings_target.return_value = {
        "target_id": 1,
        "target_name": "Laptop",
        "target_amount": 1500
    }

    client = create_app().test_client()

    response = client.put("/users/1/savings-targets/1", json={
        "target_name": "Laptop",
        "target_amount": 1500
    })

    assert response.status_code == 200
    assert response.get_json()["target_amount"] == 1500


# Test duplicate expense category
@patch("routes.budget_routes.budget")
def test_duplicate_category(mock_budget):
    mock_budget.create_category.side_effect = UniqueViolation()

    client = create_app().test_client()

    response = client.post("/users/1/expense-categories", json={
        "category_name": "Food"
    })

    assert response.status_code == 409


# Test database date and decimal conversion
@patch("routes.budget_routes.budget")
def test_finance_json(mock_budget):
    mock_budget.get_incomes.return_value = [{
        "amount": Decimal("500.25"),
        "income_date": date(2026, 11, 27)
    }]

    client = create_app().test_client()
    response = client.get("/users/1/incomes")

    assert response.status_code == 200
    assert response.get_json()[0]["amount"] == 500.25
    assert response.get_json()[0]["income_date"] == "2026-11-27"
