
from datetime import date, datetime
from math import isfinite
from flask import request


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
