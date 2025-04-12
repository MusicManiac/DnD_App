from django.db import models

from common.models import Ability


class Skill(models.Model):
    """
    This model represents a skill, such as Climb, Intimidate, etc.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    trained_only = models.BooleanField(default=False)
    armor_check_penalty = models.BooleanField(default=False)
    description = models.TextField(max_length=3000, blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    # FK
    ability = models.ForeignKey(
        Ability, blank=False, null=False, on_delete=models.PROTECT
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
