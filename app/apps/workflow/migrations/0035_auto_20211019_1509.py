# Generated by Django 3.2.7 on 2021-10-19 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("workflow", "0034_workflowoption"),
    ]

    operations = [
        migrations.RunSQL(
            """
            INSERT INTO workflow_workflowoption (
                id,
                name,
                message_name,
                to_directing_proccess,
                theme_id
            )
            SELECT
                id,
                name,
                camunda_message_name,
                to_directing_proccess,
                theme_id
            FROM
                camunda_camundaprocess;
        """,
            reverse_sql="""
            INSERT INTO camunda_camundaprocess (
                id,
                name,
                camunda_message_name,
                to_directing_proccess,
                theme_id
            )
            SELECT
                id,
                name,
                message_name,
                to_directing_proccess,
                theme_id
            FROM
                workflow_workflowoption;
        """,
        )
    ]
