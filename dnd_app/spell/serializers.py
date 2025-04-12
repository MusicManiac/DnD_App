# serializers.py
from rest_framework import serializers

from character_class.models import CharacterClass
from .models import (
    MagicAuraStrength,
    MagicSchool,
    MagicSubSchool,
    SpellDescriptor,
    SpellComponent,
    CastingTime,
    SpellRange,
    Spell,
    SpellSpellDescriptor,
    SpellLevel,
    SpellSpellComponent,
)


class MagicAuraStrengthSerializer(serializers.ModelSerializer):
    class Meta:
        model = MagicAuraStrength
        fields = "__all__"


class MagicSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = MagicSchool
        fields = "__all__"


class MagicSubSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = MagicSubSchool
        fields = "__all__"


class SpellDescriptorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpellDescriptor
        fields = "__all__"


class SpellComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpellComponent
        fields = "__all__"


class CastingTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CastingTime
        fields = "__all__"


class SpellRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpellRange
        fields = "__all__"


class SpellSerializer(serializers.ModelSerializer):
    descriptor = serializers.PrimaryKeyRelatedField(
        queryset=SpellDescriptor.objects.all(), many=True, required=False
    )
    level = serializers.PrimaryKeyRelatedField(
        queryset=CharacterClass.objects.all(), many=True, required=False
    )
    components = serializers.PrimaryKeyRelatedField(
        queryset=SpellComponent.objects.all(), many=True, required=False
    )

    class Meta:
        model = Spell
        fields = "__all__"


class SpellSpellDescriptorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpellSpellDescriptor
        fields = "__all__"


class SpellLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpellLevel
        fields = "__all__"


# Serializer for SpellSpellComponent
class SpellSpellComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpellSpellComponent
        fields = "__all__"
