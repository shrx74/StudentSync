
from database.connection import Database
from models.user import User


class UserRepository:


    def find_by_id(self, user_id):
        with Database.connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM users WHERE user_id = %s",
                    (user_id,)
                )
                row = cursor.fetchone()

        if row is None:
            return None

        return User(
            row[0],
            row[1],
            row[2],
        )

    def create_user(self, full_name, email):
        with Database.connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO users (full_name, email)
                    VALUES (%s, %s)
                    RETURNING *
                    """,
                    (full_name, email)
                )
                row = cursor.fetchone()

        return User(
            row[0],
            row[1],
            row[2],
        )
