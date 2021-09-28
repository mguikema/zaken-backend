import unittest

from api.client import Client
from api.config import Situations, Themes, api_config
from api.mock import get_case_mock
from api.tasks import AssertNextOpenTasks, ScheduleVisit, Task, Visit


class TestReschedule(unittest.TestCase):
    def setUp(self):
        self.api = Client(api_config)

    def test(self):
        case = self.api.create_case(get_case_mock(Themes.HOLIDAY_RENTAL))
        steps = [
            ScheduleVisit(),
            Visit(
                situation=Situations.NOBODY_PRESENT,
                can_next_visit_go_ahead=True,
            ),
            ScheduleVisit(),
            Visit(),
            AssertNextOpenTasks([Task.debrief]),
        ]
        case.run_steps(steps)
