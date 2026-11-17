from datetime import timedelta

REMINDER_HOURS = 48


def get_reminders(assignments, now):
    # Latest due date that still gets a reminder
    window_end = now + timedelta(hours=REMINDER_HOURS)
    reminders = []

    for assignment in assignments:
        # Skip assignments with no due date (must come before the date comparison)
        if assignment.due_date is None:
            continue

        # Skip assignments that are already done
        if assignment.status == "completed":
            continue

        # Keep assignments due between now and the end of the window
        if now <= assignment.due_date <= window_end:
            reminders.append(assignment)

    return reminders
