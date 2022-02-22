# Generated by Django 3.2.7 on 2022-02-17 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("summons", "0003_added_heir_role_to_summoned_person"),
    ]

    operations = [
        migrations.AddField(
            model_name="summonedperson",
            name="entity_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="summonedperson",
            name="function",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="summonedperson",
            name="first_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="summonedperson",
            name="last_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
