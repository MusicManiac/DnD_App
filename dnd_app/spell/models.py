from functools import partial

from django.db import models

from character_class.models import CharacterClass
from common.models import Source
from utils.validators import validate_integer_in_range, validate_positive_integer

validate_spell_level = partial(validate_integer_in_range, min_value=0, max_value=9)


class MagicAuraStrength(models.Model):
    """
    This model represents the strength of a magic aura.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name


class MagicSchool(models.Model):
    """
    This model represents the school of magic.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return self.name


class MagicSubSchool(MagicSchool):
    """
    This model represents the subschool of magic.
    """

    pass


class SpellDescriptor(models.Model):
    """
    This model represents the descriptor of a spell.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name


class SpellComponent(models.Model):
    """
    This model represents the components of a spell.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    short_name = models.CharField(max_length=2, unique=True)
    description = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.short_name})"


class CastingTime(models.Model):
    """
    This model represents the casting time of a spell.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    approximate_time_in_seconds = models.IntegerField(
        validators=[validate_positive_integer], default=3
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("approximate_time_in_seconds",)


class SpellRange(models.Model):
    """
    This model represents the range of a spell.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name


class Spell(models.Model):
    """
    This model represents a spell in the game.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=4000, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    target = models.CharField(max_length=50, blank=True, null=True)
    effect = models.CharField(max_length=50, blank=True, null=True)
    area = models.CharField(max_length=50, blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)
    saving_throw = models.CharField(max_length=100, blank=True, null=True)
    spell_resistance = models.BooleanField(default=False, blank=True, null=True)

    # FK
    source = models.ForeignKey(
        Source,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    school = models.ForeignKey(
        MagicSchool,
        on_delete=models.PROTECT,
    )
    subschool = models.ForeignKey(
        MagicSubSchool,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="spell_subschool",
    )
    casting_time = models.ForeignKey(CastingTime, on_delete=models.PROTECT)
    range = models.ForeignKey(SpellRange, on_delete=models.PROTECT)

    # M2M
    descriptor = models.ManyToManyField(
        SpellDescriptor, blank=True, through="SpellSpellDescriptor"
    )
    level = models.ManyToManyField(CharacterClass, blank=True, through="SpellLevel")
    components = models.ManyToManyField(
        SpellComponent, blank=True, through="SpellSpellComponent"
    )

    def __str__(self):
        return self.name


class SpellSpellDescriptor(models.Model):
    """
    This model represents the intermediate table between Spell and SpellDescriptor.
    """

    id = models.AutoField(primary_key=True)

    # FK
    spell = models.ForeignKey(Spell, on_delete=models.CASCADE)
    descriptor = models.ForeignKey(SpellDescriptor, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("spell", "descriptor")
        verbose_name = "Spell Descriptor"
        verbose_name_plural = "Spell Descriptors"


class SpellLevel(models.Model):
    """
    This model represents the intermediate table between Spell and Class, indicating what's the spell level for a given class.
    """

    id = models.AutoField(primary_key=True)
    level = models.IntegerField(validators=[validate_spell_level], default=1)

    # FK
    spell = models.ForeignKey(Spell, on_delete=models.CASCADE)
    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("spell", "character_class")


class SpellSpellComponent(models.Model):
    """
    This model represents the intermediate table between Spell and SpellComponent.
    """

    id = models.AutoField(primary_key=True)

    # FK
    spell = models.ForeignKey(Spell, on_delete=models.CASCADE)
    component = models.ForeignKey(SpellComponent, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("spell", "component")
        verbose_name = "Spell Component"
        verbose_name_plural = "Spell Components"
