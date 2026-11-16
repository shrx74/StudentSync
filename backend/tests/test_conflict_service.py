import unittest
from datetime import datetime
from unittest.mock import patch

from conflict_service import ConflictService


class TestConflictService(unittest.TestCase):

    @patch("conflict_service.ConflictRepository")
    def test_overlapping_session_and_shift(self, mock_repository):
        # Simulate a study session from 2 PM to 3 PM
        mock_repository.return_value.get_study_sessions.return_value = [
            (
                1,
                "Calculus Review",
                datetime(2026, 11, 20, 14, 0),
                datetime(2026, 11, 20, 15, 0)
            )
        ]

        # Simulate a work shift from 2:30 PM to 5 PM
        mock_repository.return_value.get_work_shifts.return_value = [
            (
                2,
                "Campus Library",
                datetime(2026, 11, 20, 14, 30),
                datetime(2026, 11, 20, 17, 0)
            )
        ]

        service = ConflictService()
        conflicts = service.get_conflicts(1)

        self.assertEqual(len(conflicts), 1)
        self.assertEqual(
            conflicts[0]["study_session"],
            "Calculus Review"
        )
        self.assertEqual(
            conflicts[0]["work_shift"],
            "Campus Library"
        )

    @patch("conflict_service.ConflictRepository")
    def test_no_conflict(self, mock_repository):
        # Study session ends before the shift starts
        mock_repository.return_value.get_study_sessions.return_value = [
            (
                1,
                "Calculus Review",
                datetime(2026, 11, 20, 10, 0),
                datetime(2026, 11, 20, 11, 0)
            )
        ]

        mock_repository.return_value.get_work_shifts.return_value = [
            (
                2,
                "Campus Library",
                datetime(2026, 11, 20, 14, 0),
                datetime(2026, 11, 20, 17, 0)
            )
        ]

        service = ConflictService()
        conflicts = service.get_conflicts(1)

        self.assertEqual(conflicts, [])


if __name__ == "__main__":
    unittest.main()
