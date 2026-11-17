
class User:

    def __init__(self, user_id, full_name, email):

        # Check if the full name is empty
        if not full_name or not full_name.strip():
            raise ValueError("Full name cannot be empty")

        # Check if the email is invalid
        if not email or "@" not in email:
            raise ValueError("Invalid email address")

        self.user_id = user_id
        self.full_name = full_name
        self.email = email
