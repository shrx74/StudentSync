import unittest
from unittest.mock import patch
from app import create_app


class TestConflictRoutes(unittest.TestCase):

    @patch("routes.conflict_routes.ConflictService")
    def test_get_conflicts(self, mock_service):
        mock_service.return_value.get_conflicts.return_value = [
            {
                "study_session": "Calculus Review",
                "work_shift": "Campus Library"
            }
        ]

        app = create_app()
        client = app.test_client()

        response = client.get("/users/1/conflicts")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["user_id"], 1)
        self.assertEqual(len(response.json["conflicts"]), 1)
        self.assertEqual(
            response.json["conflicts"][0]["study_session"],
            "Calculus Review"
        )
        mock_service.return_value.get_conflicts.assert_called_once_with(1)


if __name__ == "__main__":
    unittest.main()
