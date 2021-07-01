# Generated by Django 3.1.8 on 2021-07-01 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("summons", "0013_summon_type_result"),
    ]

    operations = [
        migrations.AddField(
            model_name="summonedperson",
            name="person_role",
            field=models.CharField(
                blank=True,
                choices=[
                    ("PERSON_ROLE_OWNER", "PERSON_ROLE_OWNER"),
                    ("PERSON_ROLE_RESIDENT", "PERSON_ROLE_RESIDENT"),
                    ("PERSON_ROLE_RESIDENT", "PERSON_ROLE_RESIDENT"),
                ],
                max_length=255,
                null=True,
            ),
        ),
    ]
