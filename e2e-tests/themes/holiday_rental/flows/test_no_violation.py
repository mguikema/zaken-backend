from api.config import Violation
from api.tasks.close import Close, PlanNextStep
from api.tasks.debrief import Debrief, HomeVisitReport
from api.tasks.visit import ScheduleVisit, Visit
from api.test import DefaultAPITest
from api.validators import ValidateNoOpenTasks


class TestNoViolation(DefaultAPITest):
    def test(self):
        self.skipTest("#BUG Multiple bugs.")
        self.case.run_steps(
            ScheduleVisit(),
            Visit(),
            Debrief(violation=Violation.NO),
            # FeedbackReporters(),  # BUG: If Violation=No (or send to other team) we also expect FeedbackReporters (actually feature request)
            HomeVisitReport(),  # BUG: Gives Timeline issue, you can disable validate_timeline in config to skip timeline validation
            # BUG: PlanNextStep (and subsequent) tasks are not always available (some kind of raise condition it seems)
            PlanNextStep(),  # Current/old implementation gave PlanNextStep, but even better would be skipping this step all together.
            Close(),
            ValidateNoOpenTasks(),
        )
