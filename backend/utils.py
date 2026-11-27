
from datetime import date, datetime
from math import isfinite
from flask import request
from decimal import Decimal, InvalidOperation

def get_data(fields):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        raise ValueError("JSON data required")

    for field in fields:
        if field not in data or data[field] is None or data[field] == "":
            raise ValueError(field + " is required")

    return data


def check_period(start, end):
    start = date.fromisoformat(start)
    end = date.fromisoformat(end)

    if end < start:
        raise ValueError("End date must be after start date")


def check_task(data):
    datetime.fromisoformat(data["due_date"])

    if data.get("task_type", "assignment") not in (
        "assignment", "project", "quiz", "exam", "other"
    ):
        raise ValueError("Invalid task type")

    if data.get("status", "pending") not in (
        "pending", "in_progress", "completed"
    ):
        raise ValueError("Invalid task status")


def check_job(data):
    wage = float(data["hourly_wage"])

    if not isfinite(wage) or wage < 0:
        raise ValueError("Invalid hourly wage")

    start = data.get("start_date")
    end = data.get("end_date")

    if start:
        date.fromisoformat(start)

    if end:
        date.fromisoformat(end)

    if start and end:
        check_period(start, end)


def check_shift(data):
    start = datetime.fromisoformat(data["start_time"])
    end = datetime.fromisoformat(data["end_time"])

    if end <= start:
        raise ValueError("End time must be after start time")

    minutes = data.get("break_minutes", 0)

    if type(minutes) is not int:
        raise ValueError("Break minutes must be an integer")

    duration = (end - start).total_seconds() / 60

    if minutes < 0 or minutes > duration:
        raise ValueError("Invalid break duration")

    if type(data.get("break_paid", False)) is not bool:
        raise ValueError("Invalid break_paid value")


def calculate_earnings(shift):
    start = shift["start_time"]
    end = shift["end_time"]

    hours = (end - start).total_seconds() / 3600

    if not shift["break_paid"]:
        hours -= shift["break_minutes"] / 60

    earnings = hours * float(shift["hourly_wage"])

    result = dict(shift)
    result["paid_hours"] = round(hours, 2)
    result["estimated_earnings"] = round(earnings, 2)

    return result

def check_amount(value):
    if isinstance(value, bool):
        raise ValueError("Invalid amount")

    try:
        amount = Decimal(str(value))

        if not amount.is_finite():
            raise ValueError("Invalid amount")

        if amount <= 0 or amount > Decimal("99999999.99"):
            raise ValueError("Invalid amount")

        if amount != amount.quantize(Decimal("0.01")):
            raise ValueError("Invalid decimal places")

    except InvalidOperation:
        raise ValueError("Invalid amount")


def check_text(value, maximum):
    if not isinstance(value, str):
        raise ValueError("Invalid text")

    if not value.strip() or len(value) > maximum:
        raise ValueError("Invalid text")


def check_finance_date(value):
    if not isinstance(value, str):
        raise ValueError("Invalid date")

    if date.fromisoformat(value).isoformat() != value:
        raise ValueError("Invalid date format")


def check_income(data):
    check_text(data["source"], 150)
    check_amount(data["amount"])
    check_finance_date(data["income_date"])


def check_category(data):
    check_text(data["category_name"], 100)


def check_expense(data):
    if type(data["category_id"]) is not int:
        raise ValueError("Invalid category")

    if not 1 <= data["category_id"] <= 2147483647:
        raise ValueError("Invalid category")

    check_text(data["description"], 200)
    check_amount(data["amount"])
    check_finance_date(data["expense_date"])


def check_savings_target(data):
    check_text(data["target_name"], 150)
    check_amount(data["target_amount"])


def check_contribution(data):
    check_amount(data["amount"])
    check_finance_date(data["contribution_date"])