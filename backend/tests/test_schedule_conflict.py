
import unittest
from datetime import datetime
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

if __name__ == "__main__":
    unittest.main()