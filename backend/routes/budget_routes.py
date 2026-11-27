from flask import Blueprint, request, jsonify
from datetime import date
from decimal import Decimal
from psycopg.errors import UniqueViolation

from repositories.budget_repository import BudgetRepository
from utils import (
    get_data, check_income, check_category,
    check_expense, check_savings_target,
    check_contribution
)


budget_bp = Blueprint("budget", __name__)
budget = BudgetRepository()


# Convert database objects into JSON values
def finance_json(record):
    result = dict(record)

    for key, value in result.items():
        if isinstance(value, date):
            result[key] = value.isoformat()

        elif isinstance(value, Decimal):
            result[key] = float(value)

    return result


# Return appropriate JSON response
def finance_response(result, status=200):
    if result is None:
        return jsonify({"error": "Record not found"}), 404

    if isinstance(result, list):
        return jsonify([finance_json(r) for r in result]), status

    return jsonify(finance_json(result)), status


@budget_bp.errorhandler(UniqueViolation)
def duplicate_record(error):
    return jsonify({"error": "Record already exists"}), 409


# Income routes
@budget_bp.route(
    "/users/<int:user_id>/incomes",
    methods=["GET", "POST"]
)
def incomes(user_id):
    if request.method == "GET":
        return finance_response(budget.get_incomes(user_id))

    data = get_data(["source", "amount", "income_date"])
    check_income(data)

    return finance_response(
        budget.create_income(user_id, data), 201
    )


@budget_bp.route(
    "/users/<int:user_id>/incomes/<int:income_id>",
    methods=["DELETE"]
)
def delete_income(user_id, income_id):
    return finance_response(
        budget.delete_income(user_id, income_id)
    )


# Expense category routes
@budget_bp.route(
    "/users/<int:user_id>/expense-categories",
    methods=["GET", "POST"]
)
def categories(user_id):
    if request.method == "GET":
        return finance_response(budget.get_categories(user_id))

    data = get_data(["category_name"])
    check_category(data)

    return finance_response(
        budget.create_category(user_id, data), 201
    )


# Expense routes
@budget_bp.route(
    "/users/<int:user_id>/expenses",
    methods=["GET", "POST"]
)
def expenses(user_id):
    if request.method == "GET":
        return finance_response(budget.get_expenses(user_id))

    data = get_data([
        "category_id", "description", "amount", "expense_date"
    ])

    check_expense(data)

    return finance_response(
        budget.create_expense(user_id, data), 201
    )


@budget_bp.route(
    "/users/<int:user_id>/expenses/<int:expense_id>",
    methods=["DELETE"]
)
def delete_expense(user_id, expense_id):
    return finance_response(
        budget.delete_expense(user_id, expense_id)
    )


# Savings target routes
@budget_bp.route(
    "/users/<int:user_id>/savings-targets",
    methods=["GET", "POST"]
)
def savings_targets(user_id):
    if request.method == "GET":
        return finance_response(
            budget.get_savings_targets(user_id)
        )

    data = get_data(["target_name", "target_amount"])
    check_savings_target(data)

    return finance_response(
        budget.create_savings_target(user_id, data), 201
    )


@budget_bp.route(
    "/users/<int:user_id>/savings-targets/<int:target_id>",
    methods=["PUT"]
)
def update_target(user_id, target_id):
    data = get_data(["target_name", "target_amount"])
    check_savings_target(data)

    return finance_response(
        budget.update_savings_target(user_id, target_id, data)
    )


# Savings contribution routes
@budget_bp.route(
    "/users/<int:user_id>/savings-targets/<int:target_id>/contributions",
    methods=["GET", "POST"]
)
def contributions(user_id, target_id):
    if request.method == "GET":
        return finance_response(
            budget.get_contributions(user_id, target_id)
        )

    data = get_data(["amount", "contribution_date"])
    check_contribution(data)

    data["target_id"] = target_id

    return finance_response(
        budget.create_contribution(user_id, data), 201
    )
