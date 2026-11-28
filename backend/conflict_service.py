from repositories.conflict_repository import ConflictRepository
from schedule_conflict import ScheduleConflictChecker


class ConflictService:

    def __init__(self):
        self.repository = ConflictRepository()
        self.checker = ScheduleConflictChecker()

    def get_conflicts(self, user_id):
        sessions = self.repository.get_study_sessions(user_id)
        shifts = self.repository.get_work_shifts(user_id)
        meetings = self.repository.get_class_meetings(user_id)

        conflicts = []

        for session in sessions:
            for shift in shifts:
                if self.checker.check_datetime_conflict(
                    session[2], session[3],
                    shift[2], shift[3]
                ):
                    conflicts.append({
                        "study_session": session[1],
                        "work_shift": shift[1]
                    })

        # Check recurring class meetings against work shifts
        for meeting in meetings:
            for shift in shifts:
                if self.checker.check_weekly_conflict(
                    shift[2], shift[3],
                    meeting[2], meeting[3],
                    meeting[4], meeting[5],
                    meeting[6]
                ):
                    conflicts.append({
                        "class_meeting": meeting[1],
                        "work_shift": shift[1]
                    })

        return conflicts
