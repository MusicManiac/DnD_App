from rest_framework import serializers
from .models import (
    Source,
    Die,
    TraitClassification,
    Trait,
    DurationUnit,
    Ability,
    Alignment,
    Language,
)


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = "__all__"


class DieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Die
        fields = "__all__"


class TraitClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TraitClassification
        fields = "__all__"


class TraitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trait
        fields = "__all__"


class DurationUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = DurationUnit
        fields = "__all__"


class AbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ability
        fields = "__all__"


class AlignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alignment
        fields = "__all__"


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = "__all__"
