import unittest
from unittest.mock import patch, MagicMock
from repositories.conflict_repository import ConflictRepository


class TestConflictRepository(unittest.TestCase):

    @patch("repositories.conflict_repository.Database.connect")
    def test_get_study_sessions(self, mock_connect):

        # Create a fake database connection
        mock_connection = MagicMock()
        mock_cursor = MagicMock()

        mock_connect.return_value.__enter__.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        # Fake database result
        mock_cursor.fetchall.return_value = [
            (1, "Calculus Study", "2026-11-20 14:00",
             "2026-11-20 15:00")
        ]

        repo = ConflictRepository()
        result = repo.get_study_sessions(1)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "Calculus Study")

        # Verify that the student ID was passed to the query
        self.assertEqual(mock_cursor.execute.call_args.args[1], (1,))

    @patch("repositories.conflict_repository.Database.connect")
    def test_get_work_shifts(self, mock_connect):

        mock_connection = MagicMock()
        mock_cursor = MagicMock()

        mock_connect.return_value.__enter__.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.fetchall.return_value = [
            (2, "Campus Library", "2026-11-20 14:30",
             "2026-11-20 17:00")
        ]

        repo = ConflictRepository()
        result = repo.get_work_shifts(1)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "Campus Library")
        self.assertEqual(mock_cursor.execute.call_args.args[1], (1,))


if __name__ == "__main__":
    unittest.main()
