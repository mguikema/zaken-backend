from apps.cases.models import Case
from apps.summons.models import Summon, SummonedPerson, SummonType
from rest_framework import serializers


class SummonedPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = SummonedPerson
        fields = ("id", "first_name", "preposition", "last_name", "summon")
        read_only_fields = ("summon",)


class SummonSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    type = serializers.PrimaryKeyRelatedField(
        many=False, required=True, queryset=SummonType.objects.all()
    )
    case = serializers.PrimaryKeyRelatedField(
        many=False, required=True, queryset=Case.objects.all()
    )
    persons = SummonedPersonSerializer(required=True, many=True)

    class Meta:
        model = Summon
        fields = ("id", "author", "description", "case", "type", "persons")

    def create(self, validated_data):
        persons = validated_data.pop("persons")
        summon = Summon.objects.create(**validated_data)

        for person in persons:
            SummonedPerson.objects.create(summon=summon, **person)

        return summon


class SummonTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SummonType
        fields = (
            "id",
            "name",
        )
