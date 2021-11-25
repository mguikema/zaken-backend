import logging

from api import events
from api.config import Violation
from api.tasks import AbstractUserTask, GenericUserTask
from api.tasks.visit import test_doorgeven_status_top
from api.user_tasks import (
    task_afwachten_intern_onderzoek,
    task_nakijken_aanschrijvingen,
    task_opstellen_beeldverslag,
    task_opstellen_concept_aanschrijvingen,
    task_opstellen_rapport_van_bevindingen,
    task_opstellen_verkorte_rapportage_huisbezoek,
    task_terugkoppelen_melder_1,
    task_terugkoppelen_melder_2,
    task_verwerken_debrief,
)

logger = logging.getLogger(__name__)


class test_verwerken_debrief(AbstractUserTask, task_verwerken_debrief):
    event = events.DebriefingEvent
    endpoint = "debriefings"

    def __init__(self, violation=Violation.NO, feedback="Some feedback"):
        super(test_verwerken_debrief, self).__init__(
            violation=violation, feedback=feedback
        )

    @staticmethod
    def get_steps(violation=Violation.NO):
        return [*test_doorgeven_status_top.get_steps(), __class__(violation=violation)]

    def get_post_data(self, case, task):
        return super().get_post_data(case, task) | {
            "case_user_task_id": task["case_user_task_id"],
        }


class test_terugkoppelen_melder_1(GenericUserTask, task_terugkoppelen_melder_1):
    @staticmethod
    def get_steps(violation=Violation.NO):
        return [*test_verwerken_debrief.get_steps(violation=violation), __class__()]


class test_terugkoppelen_melder_2(GenericUserTask, task_terugkoppelen_melder_2):
    @staticmethod
    def get_steps(violation=Violation.YES):
        return [*test_verwerken_debrief.get_steps(violation=violation), __class__()]


class test_afwachten_intern_onderzoek(GenericUserTask, task_afwachten_intern_onderzoek):
    @staticmethod
    def get_steps():
        return [
            *test_verwerken_debrief.get_steps(
                violation=Violation.ADDITIONAL_RESEARCH_REQUIRED
            ),
            __class__(),
        ]


class test_opstellen_beeldverslag(GenericUserTask, task_opstellen_beeldverslag):
    @staticmethod
    def get_steps():
        return [*test_terugkoppelen_melder_2.get_steps(), __class__()]


class test_opstellen_rapport_van_bevindingen(
    GenericUserTask, task_opstellen_rapport_van_bevindingen
):
    @staticmethod
    def get_steps():
        return [*test_terugkoppelen_melder_2.get_steps(), __class__()]


class test_opstellen_concept_aanschrijvingen(
    GenericUserTask, task_opstellen_concept_aanschrijvingen
):
    @staticmethod
    def get_steps():
        return [*test_terugkoppelen_melder_2.get_steps(), __class__()]


class test_opstellen_verkorte_rapportage_huisbezoek(
    GenericUserTask, task_opstellen_verkorte_rapportage_huisbezoek
):
    @staticmethod
    def get_steps(to_other_team=False):
        violation = Violation.SEND_TO_OTHER_THEME if to_other_team else Violation.NO
        return [
            *test_terugkoppelen_melder_1.get_steps(violation=violation),
            __class__(),
        ]


class test_nakijken_aanschrijvingen(GenericUserTask, task_nakijken_aanschrijvingen):
    @staticmethod
    def get_steps():
        return [
            *test_verwerken_debrief.get_steps(violation=Violation.YES),
            test_terugkoppelen_melder_2(),
            test_opstellen_beeldverslag(),
            test_opstellen_rapport_van_bevindingen(),
            test_opstellen_concept_aanschrijvingen(),
            __class__(),
        ]
