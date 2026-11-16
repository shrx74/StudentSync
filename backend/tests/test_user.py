import unittest
from models.user import User


class TestUser(unittest.TestCase):

    # Test 1: Valid user
    def test_valid_user(self):
        user = User(1, "John Smith", "john@gmail.com")

        self.assertEqual(user.full_name, "John Smith")
        self.assertEqual(user.email, "john@gmail.com")

    # Test 2: Empty name
    def test_empty_name(self):
        with self.assertRaises(ValueError):
            User(2, "", "john@gmail.com")

    # Test 3: Invalid email
    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            User(3, "John Smith", "invalidemail")


if __name__ == "__main__":
    unittest.main()
