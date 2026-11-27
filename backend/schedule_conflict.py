
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

    def check_datetime_conflict(self, start1, end1, start2, end2):

        """
        Checks whether two activities with complete
        date and time values overlap.
        """

        # Make sure both activities have valid time ranges
        if start1 >= end1 or start2 >= end2:
            raise ValueError("End time must be after start time")

        # Check whether the two activities overlap
        return start1 < end2 and start2 < end1

    def check_weekly_conflict(
        self, shift_start, shift_end, day_of_week,
        class_start, class_end, start_date, end_date
    ):
        # Get the date of the work shift
        shift_date = shift_start.date()

        # Check whether the shift occurs on the class weekday
        if shift_date.isoweekday() != day_of_week:
            return False

        # Check whether the shift is within the class date range
        if shift_date < start_date or shift_date > end_date:
            return False

        # Combine the class date and time
        meeting_start = datetime.combine(
            shift_date, class_start
        )

        meeting_end = datetime.combine(
            shift_date, class_end
        )

        # Match the timezone of the work shift
        meeting_start = meeting_start.replace(
            tzinfo=shift_start.tzinfo
        )

        meeting_end = meeting_end.replace(
            tzinfo=shift_start.tzinfo
        )

        # Reuse the existing datetime conflict checker
        return self.check_datetime_conflict(
            shift_start, shift_end,
            meeting_start, meeting_end
        )
