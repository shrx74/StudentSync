
from datetime import datetime


class TimedEvent:
    """Represents a scheduled class, study session, or work shift."""

    def __init__(self, title, date, start_time, end_time):
        self.title = title
        self.date = date
        self.start_time = start_time
        self.end_time = end_time


class ScheduleConflictChecker:
    """Checks whether two scheduled activities overlap."""

    def check_conflict(self, event1, event2):

        # Activities on different dates cannot conflict
        if event1.date != event2.date:
            return False

        # Convert time strings to time objects
        start1 = datetime.strptime(event1.start_time, "%H:%M").time()
        end1 = datetime.strptime(event1.end_time, "%H:%M").time()

        start2 = datetime.strptime(event2.start_time, "%H:%M").time()
        end2 = datetime.strptime(event2.end_time, "%H:%M").time()

        # Check that each activity has valid start/end times
        if start1 >= end1 or start2 >= end2:
            raise ValueError("End time must be after start time")

        # Check whether the activities overlap
        return start1 < end2 and start2 < end1