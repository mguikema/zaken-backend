# Generated by Django 3.0.8 on 2020-07-20 10:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cases", "0008_state_statetype"),
    ]

    operations = [
        migrations.AlterField(
            model_name="case",
            name="address",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cases",
                to="cases.Address",
            ),
        ),
        migrations.AlterField(
            model_name="case",
            name="case_type",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cases",
                to="cases.CaseType",
            ),
        ),
    ]
