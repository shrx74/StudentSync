
import unittest
from datetime import datetime, date, time
from schedule_conflict import TimedEvent, ScheduleConflictChecker


class TestScheduleConflictChecker(unittest.TestCase):

    def setUp(self):
        self.checker = ScheduleConflictChecker()

    def test_overlapping_activities(self):
        class_event = TimedEvent(
            "Calculus", "2026-09-18", "14:00", "15:30"
        )
        work_shift = TimedEvent(
            "Library Shift", "2026-09-18", "15:00", "17:00"
        )

        self.assertTrue(
            self.checker.check_conflict(class_event, work_shift)
        )

    def test_non_overlapping_activities(self):
        class_event = TimedEvent(
            "Calculus", "2026-09-18", "09:00", "10:00"
        )
        work_shift = TimedEvent(
            "Library Shift", "2026-09-18", "11:00", "13:00"
        )

        self.assertFalse(
            self.checker.check_conflict(class_event, work_shift)
        )

    def test_different_dates(self):
        class_event = TimedEvent(
            "Calculus", "2026-09-18", "14:00", "15:30"
        )
        work_shift = TimedEvent(
            "Library Shift", "2026-09-19", "14:00", "16:00"
        )

        self.assertFalse(
            self.checker.check_conflict(class_event, work_shift)
        )

    def test_touching_times(self):
        class_event = TimedEvent(
            "Calculus", "2026-09-18", "14:00", "15:00"
        )
        work_shift = TimedEvent(
            "Library Shift", "2026-09-18", "15:00", "17:00"
        )

        self.assertFalse(
            self.checker.check_conflict(class_event, work_shift)
        )

    def test_invalid_time_range(self):
        class_event = TimedEvent(
            "Calculus", "2026-09-18", "16:00", "14:00"
        )
        work_shift = TimedEvent(
            "Library Shift", "2026-09-18", "15:00", "17:00"
        )

        with self.assertRaises(ValueError):
            self.checker.check_conflict(class_event, work_shift)

    def test_conflict_across_midnight(self):
        checker = ScheduleConflictChecker()

        start1 = datetime(2026, 11, 20, 22, 0)
        end1 = datetime(2026, 11, 21, 2, 0)

        start2 = datetime(2026, 11, 21, 1, 0)
        end2 = datetime(2026, 11, 21, 3, 0)

        result = checker.check_datetime_conflict(
            start1, end1, start2, end2
        )

        self.assertTrue(result)

    # Test a Monday class overlapping a Monday shift
    def test_weekly_class_conflict(self):
        result = self.checker.check_weekly_conflict(
            datetime(2026, 11, 30, 10, 0),
            datetime(2026, 11, 30, 12, 0),
            1,
            time(11, 0),
            time(12, 30),
            date(2026, 9, 9),
            date(2026, 12, 4)
        )

        self.assertTrue(result)

    # Test a Tuesday shift against a Monday class
    def test_weekly_different_weekday(self):
        result = self.checker.check_weekly_conflict(
            datetime(2026, 12, 1, 10, 0),
            datetime(2026, 12, 1, 12, 0),
            1,
            time(11, 0),
            time(12, 30),
            date(2026, 9, 9),
            date(2026, 12, 4)
        )

        self.assertFalse(result)

    # Test a class ending when the shift starts
    def test_weekly_touching_times(self):
        result = self.checker.check_weekly_conflict(
            datetime(2026, 11, 30, 10, 0),
            datetime(2026, 11, 30, 12, 0),
            1,
            time(9, 0),
            time(10, 0),
            date(2026, 9, 9),
            date(2026, 12, 4)
        )

        self.assertFalse(result)

    # Test a shift after the class end date
    def test_weekly_outside_date_range(self):
        result = self.checker.check_weekly_conflict(
            datetime(2026, 12, 7, 10, 0),
            datetime(2026, 12, 7, 12, 0),
            1,
            time(11, 0),
            time(12, 30),
            date(2026, 9, 9),
            date(2026, 12, 4)
        )

        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
