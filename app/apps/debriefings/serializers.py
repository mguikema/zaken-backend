from apps.debriefings.models import Debriefing
from rest_framework import serializers


class DebriefingSerializer(serializers.ModelSerializer):
    case = serializers.CharField(read_only=True, source="case.identification")

    class Meta:
        model = Debriefing
        fields = (
            "id",
            "case",
            "author",
            "date_added",
            "date_modified",
            "violation",
            "feedback",
        )
        read_only_fields = (
            "date",
            "id",
        )


# TODO: Temp
class DebriefingCreateTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debriefing
        fields = (
            "id",
            "case",
            "author",
            "date_added",
            "date_modified",
            "violation",
            "feedback",
        )
        read_only_fields = ("date", "id")


class DebriefingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debriefing
        fields = (
            "id",
            "violation",
            "feedback",
            "case",
        )
        read_only_fields = ("id",)
