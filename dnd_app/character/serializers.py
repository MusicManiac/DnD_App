from rest_framework import serializers

from character.models import (
    Inventory,
    InventoryItem,
    Character,
    CharacterAbilityScore,
    CharacterCharacterClass,
    CharacterFeat,
    CharacterLanguage,
    CharacterInventory,
    CharacterSkill,
)
from common.models import Ability, Language
from feat.models import Feat
from item.models import Item
from skill.models import Skill


class InventorySerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all(), many=True, required=False
    )

    class Meta:
        model = Inventory
        fields = "__all__"


class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = "__all__"


class CharacterSerializer(serializers.ModelSerializer):
    ability_scores = serializers.PrimaryKeyRelatedField(
        queryset=Ability.objects.all(), many=True, required=False
    )
    feats = serializers.PrimaryKeyRelatedField(
        queryset=Feat.objects.all(), many=True, required=False
    )
    additionally_learned_languages = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.all(), many=True, required=False
    )
    inventories = serializers.PrimaryKeyRelatedField(
        queryset=Inventory.objects.all(), many=True, required=False
    )
    skills = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(), many=True, required=False
    )

    class Meta:
        model = Character
        fields = "__all__"


class CharacterAbilityScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterAbilityScore
        fields = "__all__"


class CharacterCharacterClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterCharacterClass
        fields = "__all__"


class CharacterFeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterFeat
        fields = "__all__"


class CharacterLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterLanguage
        fields = "__all__"


class CharacterInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterInventory
        fields = "__all__"


class CharacterSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterSkill
        fields = "__all__"
