from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from database.connection import Database


def seed():

    now = datetime.now(ZoneInfo("America/Moncton"))
    today = now.date()
    tomorrow = today + timedelta(days=1)

    start_date = today - timedelta(days=30)
    end_date = today + timedelta(days=30)

    monday = today + timedelta(days=7 - today.weekday())

    with Database.connect() as connection:
        with connection.cursor() as cursor:

            # Create demo user
            cursor.execute(
                """
                INSERT INTO users (full_name, email, timezone)
                VALUES (%s, %s, %s)
                ON CONFLICT (email) DO NOTHING
                RETURNING user_id
                """,
                ("Demo Student", "demo@studentsync.example",
                 "America/Moncton")
            )

            user = cursor.fetchone()

            if user is None:
                print("Demo data already exists.")
                return

            user_id = user[0]

            # Create semester
            cursor.execute(
                """
                INSERT INTO semesters
                (user_id, semester_name, start_date, end_date)
                VALUES (%s, %s, %s, %s)
                RETURNING semester_id
                """,
                (user_id, "Demo Semester", start_date, end_date)
            )

            semester_id = cursor.fetchone()[0]

            # Create courses
            courses = [
                ("CS2043", "Software Engineering", "ITC 101"),
                ("CS2263", "Systems Software", "ITC 201"),
                ("MATH1503", "Linear Algebra", "Room 301")
            ]

            course_ids = []

            for code, name, location in courses:

                cursor.execute(
                    """
                    INSERT INTO courses
                    (semester_id, course_code, course_name, location)
                    VALUES (%s, %s, %s, %s)
                    RETURNING course_id
                    """,
                    (semester_id, code, name, location)
                )

                course_ids.append(cursor.fetchone()[0])

            # Create class meetings
            meetings = [
                (course_ids[0], 1, "10:00", "11:00", "ITC 101"),
                (course_ids[1], 2, "12:00", "13:00", "ITC 201"),
                (course_ids[2], 3, "14:00", "15:00", "Room 301")
            ]

            for course_id, day, start, end, location in meetings:

                cursor.execute(
                    """
                    INSERT INTO class_meetings
                    (course_id, day_of_week, start_time, end_time,
                     start_date, end_date, location)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (course_id, day, start, end,
                     start_date, end_date, location)
                )

            # Create academic tasks
            tasks = [
                (course_ids[0], "D4 Project", "project", 1),
                (course_ids[1], "Assignment 10", "assignment", 3),
                (course_ids[2], "Math Quiz", "quiz", 5),
                (course_ids[0], "Final Exam", "exam", 10)
            ]

            for course_id, title, task_type, days in tasks:

                due_date = (now + timedelta(days=days)).replace(
                    hour=23, minute=59, second=0, microsecond=0
                )

                cursor.execute(
                    """
                    INSERT INTO academic_tasks
                    (user_id, course_id, title, task_type, due_date)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (user_id, course_id, title, task_type, due_date)
                )

            # Create job
            cursor.execute(
                """
                INSERT INTO jobs
                (user_id, employer, job_title, hourly_wage)
                VALUES (%s, %s, %s, %s)
                RETURNING job_id
                """,
                (user_id, "Campus Restaurant", "Team Member", 18)
            )

            job_id = cursor.fetchone()[0]

            # Create work shifts
            shifts = [
                (monday, 9, 13),
                (monday + timedelta(days=2), 16, 21),
                (monday + timedelta(days=4), 17, 22)
            ]

            for shift_date, start_hour, end_hour in shifts:

                start = now.replace(
                    year=shift_date.year,
                    month=shift_date.month,
                    day=shift_date.day,
                    hour=start_hour,
                    minute=0,
                    second=0,
                    microsecond=0
                )

                end = start.replace(hour=end_hour)

                cursor.execute(
                    """
                    INSERT INTO work_shifts
                    (job_id, start_time, end_time, break_minutes)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (job_id, start, end, 30)
                )

            # Create income records
            incomes = [
                ("Salary", 1200),
                ("Scholarship", 300)
            ]

            for source, amount in incomes:

                cursor.execute(
                    """
                    INSERT INTO income_records
                    (user_id, source, amount, income_date)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (user_id, source, amount, today)
                )

            # Create expense categories and expenses
            expenses = [
                ("Food", "Groceries", 100),
                ("Rent", "Monthly rent", 600),
                ("Transportation", "Bus pass", 50)
            ]

            for category, description, amount in expenses:

                cursor.execute(
                    """
                    INSERT INTO expense_categories
                    (user_id, category_name)
                    VALUES (%s, %s)
                    RETURNING category_id
                    """,
                    (user_id, category)
                )

                category_id = cursor.fetchone()[0]

                cursor.execute(
                    """
                    INSERT INTO expense_records
                    (user_id, category_id, description,
                     amount, expense_date)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (user_id, category_id, description,
                     amount, today)
                )

            # Create savings target
            cursor.execute(
                """
                INSERT INTO savings_targets
                (user_id, target_name, target_amount)
                VALUES (%s, %s, %s)
                RETURNING target_id
                """,
                (user_id, "New Laptop", 1500)
            )

            target_id = cursor.fetchone()[0]

            # Create savings contributions
            for amount in [200, 100]:

                cursor.execute(
                    """
                    INSERT INTO savings_contributions
                    (target_id, amount, contribution_date)
                    VALUES (%s, %s, %s)
                    """,
                    (target_id, amount, today)
                )

    print("Seed data created successfully.")
    print("Demo user ID:", user_id)


if __name__ == "__main__":
    seed()