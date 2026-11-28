from db import query


class StudyRepository:

    # Create a study session
    def create_study_session(self, user_id, data):
        return query(
            """
            INSERT INTO study_sessions
            (user_id, course_id, title, start_time,
             end_time, notes)
            SELECT user_id, %s, %s, %s, %s, %s
            FROM users
            WHERE user_id = %s
            RETURNING *
            """,
            (data.get("course_id"), data["title"],
             data["start_time"], data["end_time"],
             data.get("notes"), user_id)
        )

    # Get all study sessions
    def get_study_sessions(self, user_id):
        return query(
            """
            SELECT * FROM study_sessions
            WHERE user_id = %s
            ORDER BY start_time
            """,
            (user_id,), True
        )

    # Delete a study session
    def delete_study_session(self, user_id, session_id):
        return query(
            """
            DELETE FROM study_sessions
            WHERE user_id = %s AND session_id = %s
            RETURNING session_id
            """,
            (user_id, session_id)
        )
