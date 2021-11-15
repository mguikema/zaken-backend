from apps.cases.models import (
    Case,
    CaseClose,
    CaseCloseReason,
    CaseCloseResult,
    CaseProject,
    CaseReason,
    CaseState,
    CaseStateType,
    CaseTheme,
    CitizenReport,
)
from apps.workflow.tasks import (
    task_create_main_worflow_for_case,
    task_task_create_debrief,
    task_task_create_schedule,
    task_task_create_visit,
)
from django import forms
from django.contrib import admin


class LabelThemeModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.theme.name}: {obj.name}"


class CaseAdminForm(forms.ModelForm):
    class Meta:
        model = Case
        exclude = ()

    reason = LabelThemeModelChoiceField(
        queryset=CaseReason.objects.all(),
        required=False,
    )
    project = LabelThemeModelChoiceField(
        queryset=CaseProject.objects.all(),
        required=False,
    )


@admin.action(description="Create main workflow for case")
def create_main_worflow_for_case(modeladmin, request, queryset):
    for case in queryset.filter(is_legacy_camunda=True, end_date__isnull=True):
        task_create_main_worflow_for_case.delay(case.id)


@admin.action(description="Migrate camunda case: try to complete task_create_schedule")
def camunda_case_try_to_complete_task_create_schedule(modeladmin, request, queryset):
    for case in queryset.filter(is_legacy_camunda=True, end_date__isnull=True):
        task_task_create_schedule.delay(case.id)


@admin.action(description="Migrate camunda case: try to complete task_create_visit")
def camunda_case_try_to_complete_task_create_visit(modeladmin, request, queryset):
    for case in queryset.filter(is_legacy_camunda=True, end_date__isnull=True):
        task_task_create_visit.delay(case.id)


@admin.action(description="Migrate camunda case: try to complete task_create_debrief")
def camunda_case_try_to_complete_task_create_debrief(modeladmin, request, queryset):
    for case in queryset.filter(is_legacy_camunda=True, end_date__isnull=True):
        task_task_create_debrief.delay(case.id)


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    form = CaseAdminForm
    list_display = (
        "id",
        "theme",
        "identification",
        "start_date",
        "end_date",
        "address",
        "legacy_bwv_case_id",
        "is_legacy_bwv",
        "is_legacy_camunda",
        "author",
    )
    list_filter = ("theme",)
    actions = [
        create_main_worflow_for_case,
        camunda_case_try_to_complete_task_create_schedule,
        camunda_case_try_to_complete_task_create_visit,
        camunda_case_try_to_complete_task_create_debrief,
    ]


@admin.register(CaseState)
class CaseStateAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "case",
        "status",
        "start_date",
        "end_date",
        "case_process_id",
    )
    list_filter = ("status", "end_date")
    search_fields = ("case__id",)


@admin.register(CaseStateType)
class CaseStateTypeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "theme",
    )


@admin.register(CitizenReport)
class CitizenReportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "identification",
        "reporter_name",
        "reporter_phone",
        "reporter_email",
        "description_citizenreport",
        "nuisance",
        "author",
        "date_added",
        "case_user_task_id",
    )
    search_fields = ("case__id",)


@admin.register(CaseReason)
class CaseReasonAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "theme",
    )
    list_filter = ("theme",)


@admin.register(CaseProject)
class CaseProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "theme",
    )
    list_filter = ("theme",)


@admin.register(CaseCloseReason)
class CaseCloseReasonAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "case_theme",
        "result",
    )
    list_filter = (
        "case_theme",
        "result",
    )


@admin.register(CaseCloseResult)
class CaseCloseResultAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "case_theme",
    )
    list_filter = ("case_theme",)


@admin.register(CaseClose)
class CaseCloseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "case",
        "reason",
        "date_added",
        "case_user_task_id",
    )
    search_fields = ("case__id",)


admin.site.register(CaseTheme, admin.ModelAdmin)
