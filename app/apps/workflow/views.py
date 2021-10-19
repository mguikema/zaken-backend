from apps.cases.serializers import CaseUserTaskListSerializer
from apps.users.permissions import rest_permission_classes_for_top
from apps.workflow.serializers import GenericCompletedTaskSerializer
from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import CaseUserTask, GenericCompletedTask

role_parameter = OpenApiParameter(
    name="role",
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    required=False,
    description="Role",
)
completed_parameter = OpenApiParameter(
    name="completed",
    type=OpenApiTypes.STR,
    enum=["all", "completed", "not_completed"],
    location=OpenApiParameter.QUERY,
    required=False,
    description="Completed",
)


class CaseUserTaskViewSet(
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = rest_permission_classes_for_top()
    serializer_class = CaseUserTaskListSerializer
    queryset = CaseUserTask.objects.all()
    http_method_names = ["patch", "get"]

    @extend_schema(
        parameters=[
            role_parameter,
            completed_parameter,
        ],
        description="CaseUserTask filter query parameters",
        responses={200: CaseUserTaskListSerializer(many=True)},
    )
    def list(self, request):
        role = request.GET.get(role_parameter.name)
        completed = request.GET.get(completed_parameter.name, "not_completed")

        tasks = self.get_queryset()
        if role:
            tasks = tasks.filter(
                roles__contains=[
                    role,
                ]
            )

        if completed != "all":
            tasks = tasks.filter(
                completed=True if completed == "completed" else False,
            )

        serializer = CaseUserTaskListSerializer(
            tasks, many=True, context={"request": request}
        )

        return Response(serializer.data)


class GenericCompletedTaskViewSet(viewsets.ViewSet):
    serializer_class = GenericCompletedTaskSerializer
    queryset = GenericCompletedTask.objects.all()

    @extend_schema(
        description="Complete a task in Camunda",
        responses={200: None},
    )
    @action(
        detail=False,
        url_path="complete",
        methods=["post"],
        serializer_class=GenericCompletedTaskSerializer,
    )
    def complete_task(self, request):
        context = {"request": self.request}
        serializer = GenericCompletedTaskSerializer(data=request.data, context=context)

        if serializer.is_valid():
            data = serializer.validated_data

            variables = data.get("variables", {})
            task = get_object_or_404(CaseUserTask, id=data["case_user_task_id"])
            data.update(
                {
                    "description": task.name if task else "Algemene taak",
                    "variables": task.map_variables_on_form(variables),
                }
            )

            try:
                GenericCompletedTask.objects.create(**data)
                task.workflow.complete_user_task_and_create_new_user_tasks(
                    task.task_id, variables
                )
                return Response(
                    f"CaseUserTask {data['case_user_task_id']} has been completed"
                )
            except Exception:
                return Response(
                    f"CaseUserTask {data['case_user_task_id']} has NOT been completed"
                )

        return Response(status=status.HTTP_400_BAD_REQUEST)
