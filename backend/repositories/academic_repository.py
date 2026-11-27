
from db import query


class AcademicRepository:

    # Add a semester
    def create_semester(self, user_id, data):
        return query(
            """
            INSERT INTO semesters
            (user_id, semester_name, start_date, end_date)
            SELECT user_id, %s, %s, %s
            FROM users WHERE user_id = %s
            RETURNING *
            """,
            (data["semester_name"], data["start_date"],
             data["end_date"], user_id)
        )

    # Get all semesters
    def get_semesters(self, user_id):
        return query(
            "SELECT * FROM semesters WHERE user_id = %s ORDER BY start_date",
            (user_id,), True
        )

    # Get one semester
    def get_semester(self, user_id, semester_id):
        return query(
            "SELECT * FROM semesters WHERE user_id = %s AND semester_id = %s",
            (user_id, semester_id)
        )

    # Update a semester
    def update_semester(self, user_id, semester_id, data):
        return query(
            """
            UPDATE semesters
            SET semester_name = %s, start_date = %s, end_date = %s
            WHERE user_id = %s AND semester_id = %s
            RETURNING *
            """,
            (data["semester_name"], data["start_date"],
             data["end_date"], user_id, semester_id)
        )

    # Delete a semester
    def delete_semester(self, user_id, semester_id):
        return query(
            """
            DELETE FROM semesters
            WHERE user_id = %s AND semester_id = %s
            RETURNING semester_id
            """,
            (user_id, semester_id)
        )

    # Add a course
    def create_course(self, user_id, data):
        return query(
            """
            INSERT INTO courses
            (semester_id, course_code, course_name, instructor, location)
            SELECT semester_id, %s, %s, %s, %s
            FROM semesters
            WHERE semester_id = %s AND user_id = %s
            RETURNING *
            """,
            (data["course_code"], data["course_name"],
             data.get("instructor"), data.get("location"),
             data["semester_id"], user_id)
        )

    # Get all courses
    def get_courses(self, user_id):
        return query(
            """
            SELECT c.*
            FROM courses c
            JOIN semesters s ON c.semester_id = s.semester_id
            WHERE s.user_id = %s
            ORDER BY c.course_code
            """,
            (user_id,), True
        )

    # Get one course
    def get_course(self, user_id, course_id):
        return query(
            """
            SELECT c.*
            FROM courses c
            JOIN semesters s ON c.semester_id = s.semester_id
            WHERE s.user_id = %s AND c.course_id = %s
            """,
            (user_id, course_id)
        )

    # Update a course
    def update_course(self, user_id, course_id, data):
        return query(
            """
            UPDATE courses
            SET semester_id = %s, course_code = %s,
                course_name = %s, instructor = %s, location = %s
            WHERE course_id = %s
              AND semester_id IN
                  (SELECT semester_id FROM semesters WHERE user_id = %s)
            RETURNING *
            """,
            (data["semester_id"], data["course_code"],
             data["course_name"], data.get("instructor"),
             data.get("location"), course_id, user_id)
        )

    # Delete a course
    def delete_course(self, user_id, course_id):
        return query(
            """
            DELETE FROM courses
            WHERE course_id = %s
              AND semester_id IN
                  (SELECT semester_id FROM semesters WHERE user_id = %s)
            RETURNING course_id
            """,
            (course_id, user_id)
        )

    # Add an academic task
    def create_task(self, user_id, data):
        return query(
            """
            INSERT INTO academic_tasks
            (user_id, course_id, title, description,
             task_type, due_date, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING *
            """,
            (user_id, data.get("course_id"), data["title"],
             data.get("description"), data.get("task_type", "assignment"),
             data["due_date"], data.get("status", "pending"))
        )

    # Get all academic tasks
    def get_tasks(self, user_id):
        return query(
            """
            SELECT * FROM academic_tasks
            WHERE user_id = %s ORDER BY due_date
            """,
            (user_id,), True
        )

    # Get one academic task
    def get_task(self, user_id, task_id):
        return query(
            """
            SELECT * FROM academic_tasks
            WHERE user_id = %s AND task_id = %s
            """,
            (user_id, task_id)
        )

    # Update an academic task
    def update_task(self, user_id, task_id, data):
        return query(
            """
            UPDATE academic_tasks
            SET course_id = %s, title = %s, description = %s,
                task_type = %s, due_date = %s, status = %s
            WHERE user_id = %s AND task_id = %s
            RETURNING *
            """,
            (data.get("course_id"), data["title"],
             data.get("description"), data.get("task_type", "assignment"),
             data["due_date"], data.get("status", "pending"),
             user_id, task_id)
        )

    # Delete an academic task
    def delete_task(self, user_id, task_id):
        return query(
            """
            DELETE FROM academic_tasks
            WHERE user_id = %s AND task_id = %s
            RETURNING task_id
            """,
            (user_id, task_id)
        )
