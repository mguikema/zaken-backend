# Generated by Django 3.2.7 on 2021-10-04 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cases", "0084_alter_casestate_workflow"),
    ]

    operations = [
        migrations.AddField(
            model_name="case",
            name="is_legacy_camunda",
            field=models.BooleanField(default=True),
        ),
    ]
