from rest_framework import serializers

from character_class.models import (
    BSBProgression,
    BABProgression,
    CharacterClass,
    ClassAlignment,
    ClassTrait,
    ClassBsbProgression,
    ClassBonusLanguage,
    ClassSkill,
    PrestigeClassSkillRankRequirement,
    PrestigeCharacterClass,
    PrestigeClassRaceRequirement,
    PrestigeClassLanguageRequirement,
    PrestigeClassFeatRequirement,
)
from common.models import Alignment, Trait, Language, Die
from feat.models import Feat
from race.models import Race
from skill.models import Skill


class BSBProgressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BSBProgression
        fields = "__all__"


class BABProgressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BABProgression
        fields = "__all__"


class ClassAlignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassAlignment
        fields = "__all__"


class ClassSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassSkill
        fields = "__all__"


class ClassTraitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassTrait
        fields = "__all__"


class ClassBsbProgressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassBsbProgression
        fields = "__all__"


class ClassBonusLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassBonusLanguage
        fields = "__all__"


class CharacterClassSerializer(serializers.ModelSerializer):
    bsb_progression = serializers.PrimaryKeyRelatedField(
        queryset=BSBProgression.objects.all(), many=True, required=False
    )
    required_alignment = serializers.PrimaryKeyRelatedField(
        queryset=Alignment.objects.all(), many=True, required=False
    )
    class_skills = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(), many=True, required=False
    )
    class_traits = serializers.PrimaryKeyRelatedField(
        queryset=Trait.objects.all(), many=True, required=False
    )
    bonus_languages = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.all(), many=True, required=False
    )
    hit_die = serializers.PrimaryKeyRelatedField(queryset=Die.objects.class_hd_list())

    class Meta:
        model = CharacterClass
        fields = "__all__"


class PrestigeCharacterClassSerializer(CharacterClassSerializer):
    required_skill_ranks = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(), many=True, required=False
    )
    required_race = serializers.PrimaryKeyRelatedField(
        queryset=Race.objects.all(), many=True, required=False
    )
    required_languages = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.all(), many=True, required=False
    )
    required_feats = serializers.PrimaryKeyRelatedField(
        queryset=Feat.objects.all(), many=True, required=False
    )

    class Meta:
        model = PrestigeCharacterClass
        fields = "__all__"


class PrestigeClassSkillRankRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrestigeClassSkillRankRequirement
        fields = "__all__"


class PrestigeClassRaceRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrestigeClassRaceRequirement
        fields = "__all__"


class PrestigeClassLanguageRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrestigeClassLanguageRequirement
        fields = "__all__"


class PrestigeClassFeatRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrestigeClassFeatRequirement
        fields = "__all__"
