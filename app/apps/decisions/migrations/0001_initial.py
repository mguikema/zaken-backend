# Generated by Django 3.2.7 on 2021-11-16 09:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("cases", "0002_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("summons", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="DecisionType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("workflow_option", models.CharField(max_length=255)),
                ("name", models.CharField(max_length=255)),
                ("is_sanction", models.BooleanField(default=False)),
                (
                    "theme",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="decision_types",
                        to="cases.casetheme",
                    ),
                ),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Decision",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("case_user_task_id", models.CharField(default="-1", max_length=255)),
                (
                    "sanction_amount",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=100, null=True
                    ),
                ),
                ("description", models.TextField(blank=True, null=True)),
                ("date_added", models.DateTimeField(auto_now_add=True)),
                ("sanction_id", models.CharField(blank=True, max_length=20, null=True)),
                (
                    "author",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "case",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="decisions",
                        to="cases.case",
                    ),
                ),
                (
                    "decision_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="decisions.decisiontype",
                    ),
                ),
                (
                    "summon",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="decision",
                        to="summons.summon",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
