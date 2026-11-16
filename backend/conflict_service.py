from repositories.conflict_repository import ConflictRepository
from schedule_conflict import ScheduleConflictChecker


class ConflictService:

    def __init__(self):
        self.repository = ConflictRepository()
        self.checker = ScheduleConflictChecker()

    def get_conflicts(self, user_id):
        sessions = self.repository.get_study_sessions(user_id)
        shifts = self.repository.get_work_shifts(user_id)

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

        return conflicts
