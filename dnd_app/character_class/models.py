from functools import partial

from django.db import models

from utils.validators import validate_integer_in_range, validate_positive_integer
from common.models import Trait, Source, Die, Ability, Alignment, Language
from feat.models import Feat

from skill.models import Skill

# Validators
validate_max_class_level = partial(validate_integer_in_range, min_value=1, max_value=20)


class BSBProgression(models.Model):
    """
    This model represents the Base Save Bonus progression for a class.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    save_bonus_table = models.JSONField()

    # FK
    ability = models.ForeignKey(Ability, on_delete=models.PROTECT)

    def get_save_bonus_for_lvl(self, level):
        """
        Fetches the save bonus for a given level from the save_bonus_table JSON field.
        """
        return self.save_bonus_table.get(str(level), None)

    def __str__(self):
        bonuses = [str(self.get_save_bonus_for_lvl(level)) for level in range(1, 7)]
        return f"BSB ({self.name}) ({'/'.join(bonuses)})"

    class Meta:
        unique_together = ("ability", "save_bonus_table")
        verbose_name_plural = "Base save bonus progressions"
        ordering = ["name", "save_bonus_table"]


class BABProgression(models.Model):
    """
    This model represents the Base Attack Bonus progression for a class.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    attack_bonus_table = models.JSONField(unique=True)

    def get_attack_bonus_for_lvl(self, level):
        """
        Fetches the save bonus for a given level from the save_bonus_table JSON field.
        """
        return self.attack_bonus_table.get(str(level), None)

    def __str__(self):
        bonuses = [str(self.get_attack_bonus_for_lvl(level)) for level in range(1, 7)]
        return f"BAB ({self.name}) ({'/'.join(bonuses)})"

    class Meta:
        verbose_name_plural = "Base attack bonus progressions"
        ordering = ["attack_bonus_table"]


class CharacterClass(models.Model):
    """
    This model represents the character class, such as Fighter, Wizard, etc.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=2000, blank=True, null=True)
    max_level = models.IntegerField(default=20, validators=(validate_max_class_level,))
    link = models.URLField(blank=True, null=True)
    skill_points_per_level = models.IntegerField(
        default=0, validators=(validate_positive_integer,)
    )
    spells_per_day = models.JSONField(blank=True, null=True)
    spells_known = models.JSONField(blank=True, null=True)

    # FK
    source = models.ForeignKey(Source, blank=True, null=True, on_delete=models.PROTECT)
    hit_die = models.ForeignKey(Die, on_delete=models.PROTECT)
    bab_progression = models.ForeignKey(
        BABProgression, on_delete=models.PROTECT, verbose_name="BAB Progression"
    )

    # M2M
    required_alignment = models.ManyToManyField(
        Alignment, blank=False, through="ClassAlignment"
    )
    class_skills = models.ManyToManyField(Skill, blank=True, through="ClassSkill")
    class_traits = models.ManyToManyField(Trait, blank=True, through="ClassTrait")
    bsb_progression = models.ManyToManyField(
        BSBProgression, blank=True, through="ClassBsbProgression"
    )
    bonus_languages = models.ManyToManyField(
        Language, blank=True, through="ClassBonusLanguage"
    )

    @property
    def max_class_skill_ranks(self):
        """
        Returns the maximum number of skill ranks a character can have
        """
        return self.max_level + 3

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Character Classes"
        ordering = ["name"]


class ClassAlignment(models.Model):
    """
    This model represents the intermediate table between Class and Alignment.
    """

    id = models.AutoField(primary_key=True)

    # FK
    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE)
    alignment = models.ForeignKey(Alignment, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.character_class} - {self.alignment}"

    class Meta:
        unique_together = ("character_class", "alignment")


class ClassSkill(models.Model):
    """
    This model represents the intermediate table between Class and Skill.
    """

    id = models.AutoField(primary_key=True)

    # FK
    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("character_class", "skill")


class ClassTrait(models.Model):
    """
    This model represents the intermediate table between Class and Trait.
    """

    id = models.AutoField(primary_key=True)
    class_level_requirement = models.IntegerField(
        default=1, validators=(validate_positive_integer,)
    )
    additional_value = models.TextField(max_length=100, blank=True, null=True)

    # FK
    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE)
    trait = models.ForeignKey(Trait, on_delete=models.PROTECT)

    class Meta:
        ordering = ["class_level_requirement"]


class ClassBsbProgression(models.Model):
    """
    This model represents the intermediate table between Class and BSBProgression.
    """

    id = models.AutoField(primary_key=True)

    # FK
    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE)
    bsb_progression = models.ForeignKey(BSBProgression, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("character_class", "bsb_progression")


class ClassBonusLanguage(models.Model):
    """
    This model represents the intermediate table between Class and Language.
    """

    id = models.AutoField(primary_key=True)

    # FK
    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("character_class", "language")


class PrestigeCharacterClass(CharacterClass):
    """
    This model represents the prestige class, which is a special class that can only be taken after meeting certain requirements.
    """

    required_bab = models.IntegerField(
        default=0, validators=(validate_positive_integer,)
    )
    other_requirements = models.TextField(max_length=1000, blank=True, null=True)

    # M2M
    required_skill_ranks = models.ManyToManyField(
        Skill, blank=True, through="PrestigeClassSkillRankRequirement"
    )
    required_race = models.ManyToManyField(
        "race.Race", blank=True, through="PrestigeClassRaceRequirement"
    )
    required_languages = models.ManyToManyField(
        Language, blank=True, through="PrestigeClassLanguageRequirement"
    )
    required_feats = models.ManyToManyField(
        Feat, blank=True, through="PrestigeClassFeatRequirement"
    )

    class Meta:
        verbose_name_plural = "Prestige Classes"


class PrestigeClassSkillRankRequirement(models.Model):
    """
    This model represents the intermediate table between PrestigeClass and Skill.
    """

    id = models.AutoField(primary_key=True)
    required_ranks = models.IntegerField(
        default=0, validators=(validate_positive_integer,)
    )

    # FK
    prestige_class = models.ForeignKey(PrestigeCharacterClass, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("prestige_class", "skill")


class PrestigeClassRaceRequirement(models.Model):
    """
    This model represents the intermediate table between PrestigeClass and Race.
    """

    id = models.AutoField(primary_key=True)

    # FK
    prestige_class = models.ForeignKey(PrestigeCharacterClass, on_delete=models.CASCADE)
    race = models.ForeignKey("race.Race", on_delete=models.PROTECT)

    class Meta:
        unique_together = ("prestige_class", "race")


class PrestigeClassLanguageRequirement(models.Model):
    """
    This model represents the intermediate table between PrestigeClass and Language.
    """

    id = models.AutoField(primary_key=True)

    # FK
    prestige_class = models.ForeignKey(PrestigeCharacterClass, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("prestige_class", "language")


class PrestigeClassFeatRequirement(models.Model):
    """
    This model represents the intermediate table between PrestigeClass and Feat.
    """

    id = models.AutoField(primary_key=True)

    # FK
    prestige_class = models.ForeignKey(PrestigeCharacterClass, on_delete=models.CASCADE)
    feat = models.ForeignKey(Feat, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("prestige_class", "feat")
