# Generated by Django 3.2.7 on 2022-03-31 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("visits", "0002_visit_completed"),
    ]

    operations = [
        migrations.AddField(
            model_name="visit",
            name="top_visit_id",
            field=models.PositiveBigIntegerField(default=1),
            preserve_default=False,
        ),
    ]
