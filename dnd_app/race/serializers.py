from rest_framework import serializers

from character_class.models import CharacterClass
from common.models import Trait, Language
from race.models import (
    AbilityModifier,
    Size,
    CharacterType,
    CharacterTypeTrait,
    Race,
    RaceType,
    RaceAbilityModifier,
    RaceTrait,
    RaceLanguage,
    RaceFavoredClass,
)


class AbilityModifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbilityModifier
        fields = "__all__"


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = "__all__"


class CharacterTypeSerializer(serializers.ModelSerializer):
    traits = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Trait.objects.all(),
        required=False,
    )

    class Meta:
        model = CharacterType
        fields = "__all__"


class CharacterTypeTraitSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterTypeTrait
        fields = "__all__"


class RaceSerializer(serializers.ModelSerializer):
    types = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=CharacterType.objects.all(),
        required=False,
    )
    abilities = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=AbilityModifier.objects.all(),
        required=False,
    )
    traits = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Trait.objects.all(),
        required=False,
    )
    languages = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Language.objects.all(),
        required=False,
    )
    favored_classes = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=CharacterClass.objects.all(),
        required=False,
    )

    class Meta:
        model = Race
        fields = "__all__"


class RaceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaceType
        fields = "__all__"


class RaceAbilityModifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaceAbilityModifier
        fields = "__all__"


class RaceTraitSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaceTrait
        fields = "__all__"


class RaceLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaceLanguage
        fields = "__all__"


class RaceFavoredClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaceFavoredClass
        fields = "__all__"
