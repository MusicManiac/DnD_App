from django.db import models

from common.querysets import DieQuerySet
from utils.validators import validate_year, validate_positive_integer


class Source(models.Model):
    """
    This model represents a source of information
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, unique=True)
    link = models.URLField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True, validators=[validate_year])
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Die(models.Model):
    """
    This model represents a die
    """

    objects = DieQuerySet.as_manager()

    id = models.AutoField(primary_key=True)
    sides = models.IntegerField(validators=[validate_positive_integer], unique=True)

    def __int__(self):
        return self.sides

    def __str__(self):
        return f"d{self.sides}"

    class Meta:
        verbose_name_plural = "Dice"
        ordering = ["sides"]


class TraitClassification(models.Model):
    """
    This model represents a classification for a race trait, such as Vision, Movement, Weapon Proficiency, Immunity.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=4000, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class Trait(models.Model):
    """
    This model represents a type trait of a race or class, such as Darkvision, Proficiency, Trap Sense, etc.
    """

    id = models.AutoField(primary_key=True)
    short_description = models.CharField(max_length=100, unique=True)
    long_description = models.TextField(max_length=4000, blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    # FK
    trait_classification = models.ForeignKey(
        TraitClassification, on_delete=models.PROTECT
    )

    def __str__(self):
        return self.short_description

    class Meta:
        ordering = ("short_description",)


class DurationUnit(models.Model):
    """
    This model represents a unit of time for durations.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    name_plural = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    duration_in_seconds = models.IntegerField(validators=[validate_positive_integer])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("duration_in_seconds",)


class Ability(models.Model):
    """
    This model represents an attribute, such as strength, dexterity, etc.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    abbreviation = models.CharField(max_length=3, unique=True)
    description = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Abilities"


class Alignment(models.Model):
    """
    This model represents an alignment, such as Lawful Good, Chaotic Evil, etc.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    abbreviation = models.CharField(max_length=2, unique=True)
    description = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name


class Language(models.Model):
    """
    This model represents a language that a race can speak.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    alphabet = models.CharField(max_length=50, blank=True, null=True)
    is_secret = models.BooleanField(default=False)

    # FK
    source = models.ForeignKey(Source, null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.name
