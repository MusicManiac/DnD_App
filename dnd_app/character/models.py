from functools import partial

from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils.translation.trans_real import translation

from common.models import Source
from common.validators import validate_integer

# Validators
validate_level_adjustment = partial(validate_integer, min_value=0, max_value=10)


class Attribute(models.Model):
    """
    This model represents an attribute of a character, such as strength, dexterity, etc.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    abbreviation = models.CharField(max_length=3, unique=True)
    description = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name


class AttributeModifier(models.Model):
    """
    This model represents a modifier of an attribute, such as +2 to strength, -1 to dexterity, etc.
    """

    id = models.AutoField(primary_key=True)
    value = models.IntegerField()

    attribute = models.ForeignKey(Attribute, on_delete=models.PROTECT)

    def __str__(self):
        value_str = f"+{self.value}" if self.value > 0 else str(self.value)
        return f"{value_str} {self.attribute.name}"

    class Meta:
        unique_together = ("value", "attribute")


class Alignment(models.Model):
    """
    This model represents an alignment of a character, such as Lawful Good, Chaotic Evil, etc.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    abbreviation = models.CharField(max_length=2, unique=True)
    description = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name


class Size(models.Model):
    """
    This model represents a size of a character, such as Tiny, Medium, etc.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=15, unique=True)
    size_modifier = models.IntegerField(default=0)
    grapple_modifier = models.IntegerField(
       default=0
    )
    @property
    def hide_modifier(self):
        return -(self.grapple_modifier)

    height_or_length = models.CharField(max_length=25)
    weight = models.CharField(max_length=25)
    space_ft = models.DecimalField(max_digits=3, decimal_places=1)
    natural_reach_tall_ft = models.IntegerField(default=0)
    natural_reach_long_ft = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class TraitClassification(models.Model):
    """
    This model represents a classification for a character trait, such as Vision, Movement, Weapon Proficiency, Immunity.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name


class Trait(models.Model):
    """
    This model represents a type trait of a character, such as Darkvision, Proficiency, etc.
    """

    id = models.AutoField(primary_key=True)
    short_description = models.CharField(max_length=100, unique=True)
    long_description = models.TextField(max_length=1000, blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    trait_classification = models.ForeignKey(
        TraitClassification, on_delete=models.PROTECT
    )

    def __str__(self):
        return self.short_description


class CharacterType(models.Model):
    """
    This model represents a type or subtype of a character, such as Humanoid, Elf, etc.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=200, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    subtype = models.BooleanField(default=False)

    source = models.ForeignKey(Source, null=True, blank=True, on_delete=models.PROTECT)

    traits = models.ManyToManyField(Trait, blank=True, through="CharacterTypeTrait")

    def __str__(self):
        return self.name


class CharacterTypeTrait(models.Model):
    """
    This model represents the intermediate table between CharacterType and TypeOrSubtypeTrait.
    """

    character_type = models.ForeignKey(CharacterType, on_delete=models.CASCADE)
    trait = models.ForeignKey(Trait, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("character_type", "trait")


class Language(models.Model):
    """
    This model represents a language that a character can speak.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    alphabet = models.CharField(max_length=50, blank=True, null=True)

    source = models.ForeignKey(Source, null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Race(models.Model):
    """
    This model represents Race of a character, such as Human, Elf, etc.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    level_adjustment = models.IntegerField(
        blank=False, null=False, default=0, validators=[validate_level_adjustment]
    )

    source = models.ForeignKey(Source, null=True, blank=True, on_delete=models.PROTECT)

    attributes = models.ManyToManyField(
        AttributeModifier, blank=True, through="RaceAttributeModifier"
    )
    languages = models.ManyToManyField(Language, blank=True, through="RaceLanguage")

    def __str__(self):
        return self.name


class RaceAttributeModifier(models.Model):
    """
    This model represents the intermediate table between Race and AttributeModifier.
    """

    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    attribute_modifier = models.ForeignKey(AttributeModifier, on_delete=models.CASCADE)


    def clean(self):
        if not self.race.pk:
            raise ValidationError("Save the race before adding any attributes.")

        if self.pk is None:
            attribute_modifier = self.attribute_modifier
            # Check if a modifier for this attribute already exists for the race
            if RaceAttributeModifier.objects.filter(
                race=self.race,
                attribute_modifier__attribute=attribute_modifier.attribute,
            ).exists():
                raise ValidationError(
                    f"{self.race.name} already has a modifier for {attribute_modifier.attribute.name}."
                )

    class Meta:
        unique_together = ("race", "attribute_modifier")


class RaceLanguage(models.Model):
    """
    This model represents the intermediate table between Race and Language.
    """

    is_automatic = models.BooleanField()

    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("race", "language")
