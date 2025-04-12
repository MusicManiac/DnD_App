from functools import partial

from django.db import models
from common.models import Source, Trait, Ability, Language
from utils.validators import validate_integer_in_range

# Validators
validate_level_adjustment = partial(
    validate_integer_in_range, min_value=0, max_value=10
)


class AbilityModifier(models.Model):
    """
    This model represents a modifier of an ability, such as +2 to strength, -1 to dexterity, etc.
    """

    id = models.AutoField(primary_key=True)
    value = models.IntegerField()

    # FK
    ability = models.ForeignKey(Ability, on_delete=models.PROTECT)

    def __str__(self):
        value_str = f"+{self.value}" if self.value > 0 else str(self.value)
        return f"{value_str} {self.ability.name}"

    class Meta:
        ordering = ("ability__name", "value")
        unique_together = ("value", "ability")


class Size(models.Model):
    """
    This model represents a size of a race, such as Tiny, Medium, etc.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)

    # FK
    size_modifier = models.IntegerField(default=0, blank=False, null=False)
    grapple_modifier = models.IntegerField(default=0, blank=False, null=False)
    height_or_length = models.CharField(max_length=20)
    weight = models.CharField(max_length=20)
    space_ft = models.DecimalField(
        max_digits=3, decimal_places=1, blank=False, null=False
    )
    natural_reach_tall_ft = models.IntegerField(default=0, blank=False, null=False)
    natural_reach_long_ft = models.IntegerField(default=0, blank=False, null=False)

    @property
    def hide_modifier(self):
        return -(self.grapple_modifier)

    @staticmethod
    def get_default_size_id():
        try:
            return Size.objects.get(name="Medium").id
        except Size.DoesNotExist:
            return None

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-size_modifier",)


class CharacterType(models.Model):
    """
    This model represents a type or subtype of a race, such as Humanoid, Elf, etc.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=2000, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    subtype = models.BooleanField(default=False)

    # FK
    source = models.ForeignKey(Source, null=True, blank=True, on_delete=models.PROTECT)

    # M2M
    traits = models.ManyToManyField(Trait, blank=True, through="CharacterTypeTrait")

    def __str__(self):
        return self.name


class CharacterTypeTrait(models.Model):
    """
    This model represents the intermediate table between CharacterType and Trait.
    """

    id = models.AutoField(primary_key=True)
    additional_value = models.TextField(max_length=100, blank=True, null=True)

    # FK
    character_type = models.ForeignKey(CharacterType, on_delete=models.CASCADE)
    trait = models.ForeignKey(Trait, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("character_type", "trait")


class Race(models.Model):
    """
    This model represents Race of a race, such as Human, Elf, etc.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    level_adjustment = models.IntegerField(
        blank=False, null=False, default=0, validators=[validate_level_adjustment]
    )

    # FK
    size = models.ForeignKey(
        Size, on_delete=models.PROTECT, default=Size.get_default_size_id
    )
    source = models.ForeignKey(Source, null=True, blank=True, on_delete=models.PROTECT)

    # M2M
    types = models.ManyToManyField(CharacterType, blank=True, through="RaceType")
    abilities = models.ManyToManyField(
        AbilityModifier, blank=True, through="RaceAbilityModifier"
    )
    traits = models.ManyToManyField(Trait, blank=True, through="RaceTrait")
    languages = models.ManyToManyField(Language, blank=True, through="RaceLanguage")
    favored_classes = models.ManyToManyField(
        "character_class.CharacterClass", blank=True, through="RaceFavoredClass"
    )

    def __str__(self):
        return self.name


class RaceType(models.Model):
    """
    This model represents the intermediate table between Race and Type.
    """

    id = models.AutoField(primary_key=True)

    # FK
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    character_type = models.ForeignKey(CharacterType, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("race", "character_type")


class RaceAbilityModifier(models.Model):
    """
    This model represents the intermediate table between Race and AttributeModifier.
    """

    id = models.AutoField(primary_key=True)

    # FK
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    ability_modifier = models.ForeignKey(AbilityModifier, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("race", "ability_modifier")


class RaceTrait(models.Model):
    """
    This model represents the intermediate table between Race amd Trait.
    """

    id = models.AutoField(primary_key=True)
    additional_value = models.TextField(max_length=100, blank=True, null=True)

    # FK
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    trait = models.ForeignKey(Trait, on_delete=models.PROTECT)


class RaceLanguage(models.Model):
    """
    This model represents the intermediate table between Race and Language.
    """

    id = models.AutoField(primary_key=True)
    is_automatic = models.BooleanField(default=False)

    # FK
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("race", "language")


class RaceFavoredClass(models.Model):
    """
    This model represents the intermediate table between Race and Class.
    """

    id = models.AutoField(primary_key=True)

    # FK
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    character_class = models.ForeignKey(
        "character_class.CharacterClass", on_delete=models.PROTECT
    )

    class Meta:
        unique_together = ("race", "character_class")
