from functools import partial

from django.db import models

from utils.constraints import at_least_one_not_null_field
from common.models import Source
from utils.validators import validate_integer_in_range, validate_positive_integer
from feat.models import Feat
from race.models import Size
from spell.models import MagicAuraStrength, MagicSchool, Spell

validate_crit_multiplier = partial(validate_integer_in_range, min_value=2, max_value=10)


class ItemCategory(models.Model):
    """
    This model represents a category of items in the game.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=1000, blank=True, null=True)

    @staticmethod
    def get_default_category_id():
        try:
            return ItemCategory.objects.get(name="Item").id
        except ItemCategory.DoesNotExist:
            return None

    def __str__(self):
        return self.name


class Item(models.Model):
    """
    This model represents an item in the game.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    weight_in_lb = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    price_in_gp = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    link = models.URLField(blank=True, null=True)
    hardness = models.IntegerField(
        validators=[validate_positive_integer], blank=True, null=True
    )
    hit_points = models.IntegerField(
        validators=[validate_positive_integer], blank=True, null=True
    )

    # FK
    category = models.ForeignKey(
        ItemCategory,
        on_delete=models.PROTECT,
        default=ItemCategory.get_default_category_id,
    )
    source = models.ForeignKey(Source, on_delete=models.PROTECT, blank=True, null=True)
    size = models.ForeignKey(
        Size,
        default=Size.get_default_size_id,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name


class SpecialMaterial(models.Model):
    """
    This model represents special materials that can be used to create weapons or armor.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=2000, blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    # FK
    source = models.ForeignKey(Source, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return self.name


class MagicAbility(models.Model):
    """
    This abstract model represents a special magical ability
    """

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=2000, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    caster_level_required_for_creation = models.IntegerField(
        validators=[validate_positive_integer]
    )
    other_craft_requirements = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class WeaponMagicAbility(MagicAbility):
    """
    This model represents a special ability of a magic weapon.
    """

    id = models.AutoField(primary_key=True)
    cost_increase_in_bonus = models.IntegerField(blank=True, null=True)
    cost_increase_in_gold = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )

    # FK
    source = models.ForeignKey(Source, on_delete=models.PROTECT, blank=True, null=True)
    magic_aura_strength = models.ForeignKey(MagicAuraStrength, on_delete=models.PROTECT)
    magic_aura_type = models.ForeignKey(MagicSchool, on_delete=models.PROTECT)

    # M2M
    feats_required = models.ManyToManyField(
        Feat, blank=True, through="WeaponMagicAbilityFeat"
    )
    spells_required = models.ManyToManyField(
        Spell, blank=True, through="WeaponMagicAbilitySpell"
    )

    class Meta:
        verbose_name_plural = "Weapon magic abilities"
        constraints = [
            at_least_one_not_null_field(
                "WeaponMagicAbility", "cost_increase_in_bonus", "cost_increase_in_gold"
            ),
        ]


class WeaponMagicAbilityFeat(models.Model):
    """
    This model represents the intermediate table between WeaponMagicAbility and Feat.
    """

    id = models.AutoField(primary_key=True)

    # FK
    weapon_magic_ability = models.ForeignKey(
        WeaponMagicAbility, on_delete=models.CASCADE
    )
    feat = models.ForeignKey(Feat, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("weapon_magic_ability", "feat")
        verbose_name_plural = "Required feats"


class WeaponMagicAbilitySpell(models.Model):
    """
    This model represents the intermediate table between WeaponMagicAbility and Spell.
    """

    id = models.AutoField(primary_key=True)

    # FK
    weapon_magic_ability = models.ForeignKey(
        WeaponMagicAbility, on_delete=models.CASCADE
    )
    spell = models.ForeignKey(Spell, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("weapon_magic_ability", "spell")
        verbose_name_plural = "Required spells"


class ArmorMagicAbility(MagicAbility):
    """
    This model represents a special ability of a magic armor.
    """

    cost_increase_in_bonus = models.IntegerField(blank=True, null=True)
    cost_increase_in_gold = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )

    # FK
    source = models.ForeignKey(Source, on_delete=models.PROTECT, blank=True, null=True)
    magic_aura_strength = models.ForeignKey(MagicAuraStrength, on_delete=models.PROTECT)
    magic_aura_type = models.ForeignKey(MagicSchool, on_delete=models.PROTECT)

    # M2M
    feats_required = models.ManyToManyField(Feat, through="ArmorMagicAbilityFeat")
    spells_required = models.ManyToManyField(
        Spell, blank=True, through="ArmorMagicAbilitySpell"
    )

    class Meta:
        verbose_name_plural = "Armor magic abilities"
        constraints = [
            at_least_one_not_null_field(
                "ArmorMagicAbility", "cost_increase_in_bonus", "cost_increase_in_gold"
            ),
        ]


class ArmorMagicAbilityFeat(models.Model):
    """
    This model represents the intermediate table between ArmorMagicAbility and Feat.
    """

    id = models.AutoField(primary_key=True)

    # FK
    armor_magic_ability = models.ForeignKey(ArmorMagicAbility, on_delete=models.CASCADE)
    feat = models.ForeignKey(Feat, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("armor_magic_ability", "feat")
        verbose_name_plural = "Required feats"


class ArmorMagicAbilitySpell(models.Model):
    """
    This model represents the intermediate table between ArmorMagicAbility and Spell.
    """

    id = models.AutoField(primary_key=True)

    # FK
    armor_magic_ability = models.ForeignKey(ArmorMagicAbility, on_delete=models.CASCADE)
    spell = models.ForeignKey(Spell, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("armor_magic_ability", "spell")
        verbose_name_plural = "Required seats"


class WeaponCategory(models.Model):
    """
    This model represents a type of weapon, such as Simple, Martial, Exotic.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name


class WeaponDamageType(models.Model):
    """
    This model represents a type of damage, such as Bludgeoning, Piercing, Slashing.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name


class Weapon(Item):
    """
    This model represents a weapon in the game.
    """

    damage = models.CharField(max_length=50, blank=True, null=True)
    crit_multiplier = models.IntegerField(
        validators=[validate_crit_multiplier], default=2
    )
    crit_range = models.CharField(max_length=5, default="20", blank=True, null=True)
    range_increment_in_ft = models.IntegerField(
        validators=[validate_positive_integer], blank=True, null=True
    )
    is_masterwork = models.BooleanField(default=False)
    enchantment_bonus = models.IntegerField(
        validators=[validate_positive_integer], blank=True, null=True, default=0
    )

    # FK
    special_material = models.ForeignKey(
        SpecialMaterial, on_delete=models.PROTECT, blank=True, null=True
    )
    weapon_damage_type = models.ForeignKey(WeaponDamageType, on_delete=models.PROTECT)

    # M2M
    weapon_category = models.ManyToManyField(
        WeaponCategory, blank=True, through="WeaponWeaponCategory"
    )

    weapon_magic_ability = models.ManyToManyField(
        WeaponMagicAbility, blank=True, through="WeaponWeaponMagicAbility"
    )


class WeaponWeaponCategory(models.Model):
    """
    This model represents the intermediate table between Weapon and WeaponCategory.
    """

    id = models.AutoField(primary_key=True)

    # FK
    weapon = models.ForeignKey(Weapon, on_delete=models.CASCADE)
    weapon_category = models.ForeignKey(WeaponCategory, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("weapon", "weapon_category")


class WeaponWeaponDamageType(models.Model):
    """
    This model represents the intermediate table between Weapon and WeaponDamageType.
    """

    id = models.AutoField(primary_key=True)

    # FK
    weapon = models.ForeignKey(Weapon, on_delete=models.CASCADE)
    weapon_damage_type = models.ForeignKey(WeaponDamageType, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("weapon", "weapon_damage_type")


class WeaponWeaponMagicAbility(models.Model):
    """
    This model represents the intermediate table between Weapon and WeaponMagicAbility.
    """

    id = models.AutoField(primary_key=True)

    # FK
    weapon = models.ForeignKey(Weapon, on_delete=models.CASCADE)
    weapon_magic_ability = models.ForeignKey(
        WeaponMagicAbility, on_delete=models.PROTECT
    )

    class Meta:
        unique_together = ("weapon", "weapon_magic_ability")


class ArmorType(models.Model):
    """
    This model represents a type of armor, such as Light, Medium, Heavy.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Armor(Item):
    """
    This model represents an armor in the game.
    """

    armor_bonus = models.IntegerField(
        validators=[validate_positive_integer], blank=True, null=True
    )
    max_dex_bonus = models.IntegerField(
        validators=[validate_positive_integer], blank=True, null=True
    )
    armor_check_penalty = models.IntegerField(blank=True, null=True)
    spell_failure_chance = models.IntegerField(blank=True, null=True)
    is_masterwork = models.BooleanField(default=False)
    enchantment_bonus = models.IntegerField(
        validators=[validate_positive_integer], blank=True, null=True, default=0
    )

    # FK
    armor_type = models.ForeignKey(
        ArmorType, on_delete=models.PROTECT, blank=True, null=True
    )
    special_material = models.ForeignKey(
        SpecialMaterial, on_delete=models.PROTECT, blank=True, null=True
    )

    # M2M
    armor_magic_ability = models.ManyToManyField(
        ArmorMagicAbility, blank=True, through="ArmorArmorMagicAbility"
    )

    def get_modified_speed(self, initial_speed):
        """
        Returns the speed modified by the armor type.
        If the armor is medium or heavy, the speed is reduced to 3/4 rounded to the nearest 5.
        """
        if self.armor_type and self.armor_type.name in ["Medium", "Heavy"]:
            modified_speed = round((initial_speed * 3 / 4) / 5) * 5
            return modified_speed
        return initial_speed


class ArmorArmorMagicAbility(models.Model):
    """
    This model represents the intermediate table between Armor and ArmorMagicAbility.
    """

    id = models.AutoField(primary_key=True)

    # FK
    armor = models.ForeignKey(Armor, on_delete=models.CASCADE)
    armor_magic_ability = models.ForeignKey(ArmorMagicAbility, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("armor", "armor_magic_ability")
