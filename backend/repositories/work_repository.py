
from db import query


class WorkRepository:

    # Add a job
    def create_job(self, user_id, data):
        return query(
            """
            INSERT INTO jobs
            (user_id, employer, job_title, hourly_wage, start_date, end_date)
            SELECT user_id, %s, %s, %s, %s, %s
            FROM users WHERE user_id = %s
            RETURNING *
            """,
            (data["employer"], data.get("job_title"),
             data["hourly_wage"], data.get("start_date"),
             data.get("end_date"), user_id)
        )

    # Get all jobs
    def get_jobs(self, user_id):
        return query(
            "SELECT * FROM jobs WHERE user_id = %s ORDER BY job_id",
            (user_id,), True
        )

    # Get one job
    def get_job(self, user_id, job_id):
        return query(
            "SELECT * FROM jobs WHERE user_id = %s AND job_id = %s",
            (user_id, job_id)
        )

    # Update a job
    def update_job(self, user_id, job_id, data):
        return query(
            """
            UPDATE jobs
            SET employer = %s, job_title = %s, hourly_wage = %s,
                start_date = %s, end_date = %s
            WHERE user_id = %s AND job_id = %s
            RETURNING *
            """,
            (data["employer"], data.get("job_title"),
             data["hourly_wage"], data.get("start_date"),
             data.get("end_date"), user_id, job_id)
        )

    # Delete a job
    def delete_job(self, user_id, job_id):
        return query(
            """
            DELETE FROM jobs
            WHERE user_id = %s AND job_id = %s
            RETURNING job_id
            """,
            (user_id, job_id)
        )

    # Add a work shift
    def create_shift(self, user_id, data):
        return query(
            """
            INSERT INTO work_shifts
            (job_id, start_time, end_time, break_minutes, break_paid, notes)
            SELECT job_id, %s, %s, %s, %s, %s
            FROM jobs
            WHERE user_id = %s AND job_id = %s
            RETURNING *
            """,
            (data["start_time"], data["end_time"],
             data.get("break_minutes", 0),
             data.get("break_paid", False),
             data.get("notes"), user_id, data["job_id"])
        )

    # Get all shifts
    def get_shifts(self, user_id):
        return query(
            """
            SELECT s.*, j.hourly_wage, j.employer
            FROM work_shifts s
            JOIN jobs j ON s.job_id = j.job_id
            WHERE j.user_id = %s
            ORDER BY s.start_time
            """,
            (user_id,), True
        )

    # Get one shift
    def get_shift(self, user_id, shift_id):
        return query(
            """
            SELECT s.*, j.hourly_wage
            FROM work_shifts s
            JOIN jobs j ON s.job_id = j.job_id
            WHERE j.user_id = %s AND s.shift_id = %s
            """,
            (user_id, shift_id)
        )

    # Update a work shift
    def update_shift(self, user_id, shift_id, data):
        return query(
            """
            UPDATE work_shifts
            SET job_id = %s, start_time = %s, end_time = %s,
                break_minutes = %s, break_paid = %s, notes = %s
            WHERE shift_id = %s
              AND job_id IN
                  (SELECT job_id FROM jobs WHERE user_id = %s)
            RETURNING *
            """,
            (data["job_id"], data["start_time"], data["end_time"],
             data.get("break_minutes", 0),
             data.get("break_paid", False),
             data.get("notes"), shift_id, user_id)
        )

    # Delete a work shift
    def delete_shift(self, user_id, shift_id):
        return query(
            """
            DELETE FROM work_shifts
            WHERE shift_id = %s
              AND job_id IN
                  (SELECT job_id FROM jobs WHERE user_id = %s)
            RETURNING shift_id
            """,
            (shift_id, user_id)
        )
