from rest_framework import serializers

from feat.models import Feat
from item.models import (
    ItemCategory,
    Item,
    SpecialMaterial,
    WeaponMagicAbility,
    WeaponMagicAbilityFeat,
    WeaponMagicAbilitySpell,
    WeaponCategory,
    WeaponDamageType,
    Weapon,
    WeaponWeaponCategory,
    WeaponWeaponDamageType,
    WeaponWeaponMagicAbility,
    ArmorType,
    ArmorMagicAbility,
    ArmorArmorMagicAbility,
    ArmorMagicAbilityFeat,
    ArmorMagicAbilitySpell,
    Armor,
)
from spell.models import Spell


class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory
        fields = "__all__"


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class SpecialMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialMaterial
        fields = "__all__"


class WeaponMagicAbilitySerializer(serializers.ModelSerializer):
    feats_required = serializers.PrimaryKeyRelatedField(
        queryset=Feat.objects.all(), many=True, required=False
    )
    spells_required = serializers.PrimaryKeyRelatedField(
        queryset=Spell.objects.all(), many=True, required=False
    )

    class Meta:
        model = WeaponMagicAbility
        fields = "__all__"


class WeaponMagicAbilityFeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeaponMagicAbilityFeat
        fields = "__all__"


class WeaponMagicAbilitySpellSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeaponMagicAbilitySpell
        fields = "__all__"


class ArmorMagicAbilitySerializer(serializers.ModelSerializer):
    feats_required = serializers.PrimaryKeyRelatedField(
        queryset=Feat.objects.all(), many=True, required=False
    )
    spells_required = serializers.PrimaryKeyRelatedField(
        queryset=Spell.objects.all(), many=True, required=False
    )

    class Meta:
        model = ArmorMagicAbility
        fields = "__all__"


class ArmorMagicAbilityFeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArmorMagicAbilityFeat
        fields = "__all__"


class ArmorMagicAbilitySpellSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArmorMagicAbilitySpell
        fields = "__all__"


class WeaponCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeaponCategory
        fields = "__all__"


class WeaponDamageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeaponDamageType
        fields = "__all__"


class WeaponSerializer(ItemSerializer):
    weapon_category = serializers.PrimaryKeyRelatedField(
        queryset=WeaponCategory.objects.all(), many=True, required=False
    )
    weapon_magic_ability = serializers.PrimaryKeyRelatedField(
        queryset=WeaponMagicAbility.objects.all(), many=True, required=False
    )

    class Meta:
        model = Weapon
        fields = "__all__"


class WeaponWeaponCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeaponWeaponCategory
        fields = "__all__"


class WeaponWeaponDamageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeaponWeaponDamageType
        fields = "__all__"


class WeaponWeaponMagicAbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeaponWeaponMagicAbility
        fields = "__all__"


class ArmorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArmorType
        fields = "__all__"


class ArmorSerializer(serializers.ModelSerializer):
    armor_magic_ability = serializers.PrimaryKeyRelatedField(
        queryset=ArmorMagicAbility.objects.all(), many=True, required=False
    )

    class Meta:
        model = Armor
        fields = "__all__"


class ArmorArmorMagicAbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArmorArmorMagicAbility
        fields = "__all__"
