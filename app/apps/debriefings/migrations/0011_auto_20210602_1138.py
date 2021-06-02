# Generated by Django 3.1.8 on 2021-06-02 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("debriefings", "0010_auto_20210520_1201"),
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
                    ("SEND_TO_OTHER_THEME", "Naar ander team"),
                    ("AUTHORIZATION_REQUEST", "Aanvraag machting"),
                ],
                default="NO",
                max_length=28,
            ),
        ),
    ]
