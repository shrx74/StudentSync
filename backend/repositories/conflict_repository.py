from database.connection import Database


class ConflictRepository:
    """Retrieves scheduled activities for conflict detection."""

    def get_study_sessions(self, user_id):
        with Database.connect() as connection:
            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT session_id, title, start_time, end_time
                    FROM study_sessions
                    WHERE user_id = %s
                    ORDER BY start_time
                    """,
                    (user_id,)
                )

                return cursor.fetchall()

    def get_work_shifts(self, user_id):
        with Database.connect() as connection:
            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT s.shift_id, j.employer,
                           s.start_time, s.end_time
                    FROM work_shifts s
                    JOIN jobs j ON s.job_id = j.job_id
                    WHERE j.user_id = %s
                    ORDER BY s.start_time
                    """,
                    (user_id,)
                )

                return cursor.fetchall()

    def get_class_meetings(self, user_id):
        with Database.connect() as connection:
            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT m.meeting_id, c.course_name,
                           m.day_of_week, m.start_time,
                           m.end_time, m.start_date,
                           m.end_date
                    FROM class_meetings m
                    JOIN courses c ON m.course_id = c.course_id
                    JOIN semesters s ON c.semester_id = s.semester_id
                    WHERE s.user_id = %s
                    ORDER BY m.day_of_week, m.start_time
                    """,
                    (user_id,)
                )

                return cursor.fetchall()
