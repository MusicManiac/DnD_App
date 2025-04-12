from django.db import models

from common.models import Ability, Source
from utils.validators import validate_positive_integer
from skill.models import Skill


class TypeOfFeat(models.Model):
    """
    Model representing a type of feat, such as Fighter Bonus Feat or General.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=3000, blank=True, null=True)

    def __str__(self):
        return self.name


class Feat(models.Model):
    """
    Model representing a feat such as Die Hard or Combat Expertise.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    benefit = models.TextField(max_length=2000)
    normal = models.TextField(max_length=1000, blank=True, null=True)
    special = models.TextField(max_length=1000, blank=True, null=True)
    other_prerequisites = models.TextField(max_length=1000, blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    # FK
    source = models.ForeignKey(Source, on_delete=models.PROTECT, blank=True, null=True)

    # M2M
    feat_type = models.ManyToManyField(TypeOfFeat, through="FeatTypeOfFeat")
    ability_prerequisite = models.ManyToManyField(
        Ability, blank=True, through="FeatAbilityPrerequisite"
    )
    feat_prerequisite = models.ManyToManyField(
        "self", symmetrical=False, blank=True, through="FeatFeatPrerequisite"
    )
    skill_prerequisite = models.ManyToManyField(
        Skill, blank=True, through="FeatSkillPrerequisite"
    )

    def __str__(self):
        return self.name


class FeatTypeOfFeat(models.Model):
    """
    This model represents the intermediate table between Feat and TypeOfFeat.
    """

    id = models.AutoField(primary_key=True)

    feat = models.ForeignKey(Feat, on_delete=models.CASCADE)
    type_of_feat = models.ForeignKey(TypeOfFeat, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("feat", "type_of_feat")
        verbose_name_plural = "Types of Feat"


class FeatAbilityPrerequisite(models.Model):
    """
    This model represents the intermediate table between Feat and Ability.
    """

    id = models.AutoField(primary_key=True)
    required_ability_value = models.IntegerField(
        default=10, validators=[validate_positive_integer]
    )

    feat = models.ForeignKey(Feat, on_delete=models.CASCADE)
    ability = models.ForeignKey(Ability, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("feat", "ability")


class FeatFeatPrerequisite(models.Model):
    """
    This model represents the intermediate table between Feat and Feat.
    """

    id = models.AutoField(primary_key=True)

    prerequisite_for_feat = models.ForeignKey(
        Feat, on_delete=models.CASCADE, related_name="prerequisite_for"
    )
    prerequisite = models.ForeignKey(
        Feat, on_delete=models.PROTECT, related_name="prerequisites"
    )

    class Meta:
        unique_together = ("prerequisite_for_feat", "prerequisite")
        verbose_name_plural = "Feat prerequisites for Feat"


class FeatSkillPrerequisite(models.Model):
    """
    This model represents the intermediate table between Feat and Skill.
    """

    id = models.AutoField(primary_key=True)
    required_ranks = models.IntegerField(
        default=0, validators=[validate_positive_integer]
    )

    feat = models.ForeignKey(Feat, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("feat", "skill")
