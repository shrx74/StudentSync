from datetime import datetime


class Assignment:

    def __init__(self, title, due_date=None, status="pending"):

        #empty checks
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")

        if due_date is not None and not isinstance(due_date, datetime):
            raise ValueError("Due date must be a datetime")

        self.title = title
        self.due_date = due_date
        self.status = status
