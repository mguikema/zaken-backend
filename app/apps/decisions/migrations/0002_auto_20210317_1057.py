# Generated by Django 3.1.7 on 2021-03-17 09:57

from django.db import migrations


class Migration(migrations.Migration):
    def create_decision_types(apps, schema_editor):
        DecisionType = apps.get_model("decisions", "DecisionType")
        CaseTeam = apps.get_model("cases", "CaseTeam")

        (team, _) = CaseTeam.objects.get_or_create(name="Vakantieverhuur")

        DecisionType.objects.get_or_create(
            camunda_option="boete", name="Boete", is_sanction=True, team=team
        )

        DecisionType.objects.get_or_create(
            camunda_option="invordering_dwangsom",
            name="Invordering dwangsom",
            is_sanction=True,
            team=team,
        )

        DecisionType.objects.get_or_create(
            camunda_option="meldplicht_beschikking_boete",
            name="Meldplicht beschikking dwangsom",
            is_sanction=False,
            team=team,
        )

        DecisionType.objects.get_or_create(
            camunda_option="preventieve_last",
            name="Preventieve last",
            is_sanction=False,
            team=team,
        )

        DecisionType.objects.get_or_create(
            camunda_option="last_onder_dwangsom",
            name="Last onder dwangsom",
            is_sanction=False,
            team=team,
        )

        DecisionType.objects.get_or_create(
            camunda_option="intrekken_vv_vergunning",
            name="Intrekken VV vergunning",
            is_sanction=False,
            team=team,
        )

        DecisionType.objects.get_or_create(
            camunda_option="intrekken_bb_vergunning",
            name="Intrekken BB vergunning",
            is_sanction=False,
            team=team,
        )

        DecisionType.objects.get_or_create(
            camunda_option="intrekken_shortstay_vergunning",
            name="Intrekken Shortstay vergunning",
            is_sanction=False,
            team=team,
        )

    dependencies = [
        ("decisions", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_decision_types, migrations.RunPython.noop),
    ]
