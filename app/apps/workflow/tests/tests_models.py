from apps.cases.models import Case, CaseReason, CaseTheme
from apps.workflow.models import Task, Workflow
from django.conf import settings
from django.core import management
from django.test import TestCase
from model_bakery import baker
from SpiffWorkflow.bpmn.specs.BpmnProcessSpec import BpmnProcessSpec
from SpiffWorkflow.bpmn.workflow import BpmnWorkflow


class WorkflowModelTest(TestCase):
    def setUp(self):
        management.call_command("flush", verbosity=0, interactive=False)

    def test_can_create_workflow(self):
        """ Tests Workflow object creation """
        self.assertEquals(Workflow.objects.count(), 0)
        baker.make(Workflow)
        self.assertEquals(Workflow.objects.count(), 1)

    def test_can_get_workflow_spec(self):
        """ Tests can get workflow spec """
        baker.make(Workflow)
        spec = (
            Workflow.objects.all()
            .first()
            .get_workflow_spec(
                "top_workflow.bpmn",
                [
                    "common_workflow.bpmn",
                ],
            )
        )
        self.assertEquals(type(spec), BpmnProcessSpec)

    def test_initial_serialized_workflow_state(self):
        """ Tests initial serialized_workflow_state  """
        baker.make(Workflow)
        workflow_instance = Workflow.objects.all().first()
        self.assertEquals(workflow_instance._get_serialized_workflow_state(), None)

    def test_get_workflow(self):
        """ Tests get_workflow  """
        baker.make(Workflow)
        workflow_instance = Workflow.objects.all().first()
        spec = (
            Workflow.objects.all()
            .first()
            .get_workflow_spec(
                "top_workflow.bpmn",
                [
                    "common_workflow.bpmn",
                ],
            )
        )
        workflow = workflow_instance.get_workflow(spec)
        self.assertEquals(type(workflow), BpmnWorkflow)

    def test_get_workflow_current_task_names(self):
        """ Tests get workflow current task names  """
        baker.make(Workflow)
        workflow_instance = Workflow.objects.all().first()
        spec = (
            Workflow.objects.all()
            .first()
            .get_workflow_spec(
                "top_workflow.bpmn",
                [
                    "common_workflow.bpmn",
                ],
            )
        )
        workflow = workflow_instance.get_workflow(spec)
        task_names = workflow_instance.get_ready_task_names(workflow)
        self.assertEquals(task_names, ["create_case"])
        task_names = workflow_instance.get_ready_task_names(workflow)
        self.assertEquals(task_names, ["create_case"])

    def test_get_user_task_form(self):
        """ Tests get user task form """
        baker.make(Workflow)
        workflow_instance = Workflow.objects.all().first()
        spec = (
            Workflow.objects.all()
            .first()
            .get_workflow_spec(
                "top_workflow.bpmn",
                [
                    "common_workflow.bpmn",
                ],
            )
        )
        workflow = workflow_instance.get_workflow(spec)
        task_names = workflow_instance.get_ready_task_names(workflow)
        form = workflow_instance.get_user_task_form(task_names[0], workflow)
        self.assertEquals(
            form,
            {
                "form": {"key": "create_case_form"},
                "fields": [
                    {
                        "id": "create_case_formfield",
                        "type": "string",
                        "label": "create_case_formfield label",
                        "default_value": None,
                        "properties": [],
                        "validation": [],
                    }
                ],
            },
        )

    def test_complete_user_task(self):
        """ Tests complete usertask  """
        theme = CaseTheme.objects.create(
            name=settings.DEFAULT_THEME,
        )
        reason = CaseReason.objects.create(
            name=settings.DEFAULT_REASON,
            theme=theme,
        )
        case = Case.objects.create(
            reason=reason,
            theme=theme,
        )
        workflow_instance = Workflow.objects.create(
            case=case,
        )
        spec = (
            Workflow.objects.all()
            .first()
            .get_workflow_spec(
                "top_workflow.bpmn",
                [
                    "common_workflow.bpmn",
                ],
            )
        )
        workflow = workflow_instance.get_workflow(spec)
        # workflow_instance.set_initial_data(data={
        #     "init_data": "my init data",
        # }, wf=workflow)

        task_names = workflow_instance.get_ready_task_names(workflow)

        self.assertEquals(
            workflow_instance.get_ready_task_names(workflow), ["create_case"]
        )
        workflow_instance.complete_user_task(
            task_names[0], workflow, {"create_case_formfield": "je moeder"}
        )
        task_names = workflow_instance.get_ready_task_names(workflow)

        self.assertEquals(
            workflow_instance.get_ready_task_names(workflow), ["create_case2"]
        )
        self.assertEquals(Task.objects.all().count(), 1)
