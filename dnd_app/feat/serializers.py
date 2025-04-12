from rest_framework import serializers

from common.models import Ability
from skill.models import Skill
from .models import (
    TypeOfFeat,
    Feat,
    FeatTypeOfFeat,
    FeatAbilityPrerequisite,
    FeatFeatPrerequisite,
    FeatSkillPrerequisite,
)


class TypeOfFeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOfFeat
        fields = "__all__"


class FeatSerializer(serializers.ModelSerializer):
    feat_type = serializers.PrimaryKeyRelatedField(
        queryset=TypeOfFeat.objects.all(), many=True
    )
    ability_prerequisite = serializers.PrimaryKeyRelatedField(
        queryset=Ability.objects.all(), many=True, required=False
    )
    skill_prerequisite = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(), many=True, required=False
    )
    feat_prerequisite = serializers.PrimaryKeyRelatedField(
        queryset=Feat.objects.all(), many=True, required=False
    )

    class Meta:
        model = Feat
        fields = "__all__"


class FeatTypeOfFeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatTypeOfFeat
        fields = "__all__"


class FeatAbilityPrerequisiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatAbilityPrerequisite
        fields = "__all__"


class FeatFeatPrerequisiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatFeatPrerequisite
        fields = "__all__"


class FeatSkillPrerequisiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatSkillPrerequisite
        fields = "__all__"
