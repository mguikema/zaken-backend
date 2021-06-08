# Generated by Django 3.1.8 on 2021-06-08 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("debriefings", "0012_debriefing_violation_result"),
    ]

    operations = [
        migrations.AlterField(
            model_name="debriefing",
            name="violation",
            field=models.CharField(
                choices=[
                    ("NO", "No"),
                    ("YES", "Yes"),
                    ("ADDITIONAL_RESEARCH_REQUIRED", "Additional research required"),
                    ("ADDITIONAL_VISIT_REQUIRED", "Nieuw huisbezoek nodig"),
                    (
                        "ADDITIONAL_VISIT_WITH_AUTHORIZATION",
                        "Nieuw huisbezoek inclusief machtingaanvraag",
                    ),
                    ("SEND_TO_OTHER_THEME", "Naar ander team"),
                ],
                default="NO",
                max_length=255,
            ),
        ),
    ]
