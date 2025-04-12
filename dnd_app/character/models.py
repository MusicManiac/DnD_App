from django.db import models

from character_class.models import CharacterClass
from common.models import Ability, Alignment, Language
from utils.string_formatters import format_bab_into_multiattack
from feat.models import Feat
from item.models import Item
from race.models import Race
from skill.models import Skill


class Inventory(models.Model):
    """
    This model represents the inventory of a character.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    capacity = models.IntegerField(default=0)

    # M2M
    items = models.ManyToManyField(Item, blank=True, through="InventoryItem")

    @property
    def total_weight(self):
        """
        Returns the total weight of all items in the inventory, considering their quantity.
        """
        return sum(
            inventory_item.item_stack_weight
            for inventory_item in self.inventoryitem_set.all()
        )

    @property
    def total_value(self):
        """
        Returns the total value of all items in the inventory.
        """
        return sum(
            inventory_item.item_stack_value
            for inventory_item in self.inventoryitem_set.all()
        )

    @property
    def available_capacity(self):
        """
        Returns the available capacity of the inventory.
        """
        return self.capacity - self.total_weight

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Inventories"


class InventoryItem(models.Model):
    """
    This model represents the intermediate table between Inventory and Item.
    """

    id = models.AutoField(primary_key=True)
    quantity = models.IntegerField(default=1)

    # FK
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)

    @property
    def item_stack_weight(self):
        """
        Returns the total weight of the item stack in the inventory.
        """
        return self.item.weight_in_lb * self.quantity

    @property
    def item_stack_value(self):
        """
        Returns the total value of the item stack in the inventory.
        """
        return self.item.price_in_gp * self.quantity

    def __str__(self):
        return f"{self.inventory.name} - {self.item.name}: {self.quantity}"

    class Meta:
        verbose_name_plural = "Inventory Items"


class Character(models.Model):
    """
    This model represent player character
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    current_hit_points = models.IntegerField(default=0)
    max_hit_points = models.IntegerField(default=0)
    gender = models.CharField(max_length=20, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    height = models.CharField(max_length=20, blank=True, null=True)
    skin_color = models.CharField(max_length=20, blank=True, null=True)
    hair_color = models.CharField(max_length=20, blank=True, null=True)
    eye_color = models.CharField(max_length=20, blank=True, null=True)
    weight = models.CharField(max_length=20, blank=True, null=True)
    spell_resistance = models.IntegerField(default=0)
    fortitude_save_bonus = models.IntegerField(default=0)
    reflex_save_bonus = models.IntegerField(default=0)
    will_save_bonus = models.IntegerField(default=0)
    initiative_bonus = models.IntegerField(default=0)
    speed = models.IntegerField(default=30)
    armor_class = models.IntegerField(default=10)

    # FK
    race = models.ForeignKey(Race, on_delete=models.PROTECT)
    alignment = models.ForeignKey(Alignment, on_delete=models.PROTECT)

    # M2M
    ability_scores = models.ManyToManyField(
        Ability, blank=True, through="CharacterAbilityScore"
    )
    character_classes = models.ManyToManyField(
        CharacterClass, blank=True, through="CharacterCharacterClass"
    )
    feats = models.ManyToManyField(Feat, blank=True, through="CharacterFeat")
    additionally_learned_languages = models.ManyToManyField(
        Language, blank=True, through="CharacterLanguage"
    )
    inventories = models.ManyToManyField(
        Inventory, blank=True, through="CharacterInventory"
    )
    skills = models.ManyToManyField(Skill, blank=True, through="CharacterSkill")

    @property
    def class_levels(self):
        """
        Returns the character's level based on the sum of levels in all character classes.
        """
        return sum(
            [
                character_class.level
                for character_class in self.charactercharacterclass_set.all()
            ]
        )

    def get_save_for_ability(self, ability):
        """
        Returns the character's save bonus for the specified ability.
        It consists of all the bonuses from the character's classes + selected ability modifier.
        """
        bonus_from_classes = sum(
            character_class.character_class.bsb_progression.filter(
                ability__name=ability
            )
            .first()
            .get_save_bonus_for_lvl(character_class.level)
            for character_class in self.charactercharacterclass_set.all()
            if character_class.character_class.bsb_progression.filter(
                ability__name=ability
            ).first()
        )

        ability_score = self.characterabilityscore_set.filter(
            ability__name=ability
        ).first()

        if ability_score:
            return bonus_from_classes + ability_score.modifier
        else:
            return bonus_from_classes

    @property
    def fortitude_save(self):
        """
        Returns the character's fortitude save bonus.
        """
        return self.get_save_for_ability("Constitution") + self.fortitude_save_bonus

    @property
    def reflex_save(self):
        """
        Returns the character's reflex save bonus.
        """
        return self.get_save_for_ability("Dexterity") + self.reflex_save_bonus

    @property
    def will_save(self):
        """
        Returns the character's will save bonus.
        """
        return self.get_save_for_ability("Wisdom") + self.will_save_bonus

    @property
    def initiative(self):
        """
        Returns the character's initiative, including bonus.
        """
        return (
            self.initiative_bonus
            + self.characterabilityscore_set.filter(ability__name="Dexterity")
            .first()
            .modifier
        )

    @property
    def list_of_languages(self):
        """
        Returns a list of languages known by the character.
        Combines languages from the character's race and additionally learned languages.
        """
        race_languages = [
            race_language.language.name
            for race_language in self.race.racelanguage_set.all()
            if race_language.is_automatic
        ]

        learned_languages = [
            character_language.language.name
            for character_language in self.characterlanguage_set.all()
        ]
        all_languages = race_languages + learned_languages

        return ", ".join(all_languages)

    @property
    def multiattack_bab(self):
        """
        Fetches the full attack bonus for character from sum of his classes in a form of +W/+X/+Y/+Z
        where W, X, Y, Z are the attack bonuses for subsequent attacks.
        """

        bab_from_classes = sum(
            character_class.character_class.bab_progression.get_attack_bonus_for_lvl(
                character_class.level
            )
            for character_class in self.charactercharacterclass_set.all()
        )
        if bab_from_classes is None:
            return None

        return format_bab_into_multiattack(bab_from_classes)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["level", "name"]


class CharacterAbilityScore(models.Model):
    """
    This model represents the intermediate table between Character and Ability.
    """

    id = models.AutoField(primary_key=True)
    value = models.IntegerField(default=10)
    bonus = models.IntegerField(default=0)

    # FK
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    ability = models.ForeignKey(Ability, on_delete=models.PROTECT)

    @property
    def modifier(self):
        """
        Returns the modifier for the ability score.
        The modifier is calculated as (value - 10) // 2.
        """
        return (self.value + self.bonus - 10) // 2

    def __str__(self):
        return f"{self.character.name} - {self.ability.name}: {self.value}"

    class Meta:
        unique_together = ("character", "ability")
        verbose_name_plural = "Ability Scores"


class CharacterCharacterClass(models.Model):
    """
    This model represents the relationship between a character and their class, indicating how many levels character has in that class.
    """

    id = models.AutoField(primary_key=True)
    level = models.IntegerField(default=1)

    # FK
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    character_class = models.ForeignKey(CharacterClass, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.character.name} - {self.character_class.name}: {self.level}"

    class Meta:
        unique_together = ("character", "character_class")
        ordering = ["character_class__name"]
        verbose_name_plural = "Character Classes"


class CharacterFeat(models.Model):
    """
    This model represents the intermediate table between a character and their feats.
    """

    id = models.AutoField(primary_key=True)
    level_acquired = models.IntegerField(default=1)

    # FK
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    feat = models.ForeignKey(Feat, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.character.name} - {self.feat.name}"

    class Meta:
        ordering = ["level_acquired"]
        verbose_name_plural = "Feats"


class CharacterLanguage(models.Model):
    """
    This model represents the intermediate table between a character and their languages.
    """

    id = models.AutoField(primary_key=True)
    is_automatic = models.BooleanField(default=False)

    # FK
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.character.name} - {self.language.name}"

    class Meta:
        ordering = ["language__name"]
        verbose_name_plural = "Languages"


class CharacterInventory(models.Model):
    """
    This model represents the intermediate table between a character and their inventories.
    """

    id = models.AutoField(primary_key=True)

    # FK
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.character.name} - {self.inventory.name}"

    class Meta:
        ordering = ["inventory__name"]
        verbose_name_plural = "Inventories"


class CharacterSkill(models.Model):
    """
    This model represents the intermediate table between a character and their skills.
    """

    id = models.AutoField(primary_key=True)
    ranks = models.IntegerField(default=0)
    misc_bonus = models.IntegerField(default=0)

    # FK
    skill = models.ForeignKey(Skill, on_delete=models.PROTECT)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)

    @property
    def total_bonus(self):
        """
        Returns the total bonus for the skill, which is the sum of ranks, misc bonus, and ability modifier.
        """
        ability_score = self.character.characterabilityscore_set.filter(
            ability__name=self.skill.ability.name
        ).first()

        if ability_score:
            return self.ranks + self.misc_bonus + ability_score.modifier
        else:
            return self.ranks + self.misc_bonus

    def __str__(self):
        return f"{self.character.name} - {self.skill.name}"

    class Meta:
        ordering = ["skill__name"]
        verbose_name_plural = "Skills"
