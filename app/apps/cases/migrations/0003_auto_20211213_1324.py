# Generated by Django 3.2.7 on 2021-12-13 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cases", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="case",
            name="sensitive",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="casetheme",
            name="sensitive",
            field=models.BooleanField(default=False),
        ),
    ]
