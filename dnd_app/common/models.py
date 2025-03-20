from django.db import models

from .validators import validate_year


class Source(models.Model):
    """
    This model represents a source of information
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    link = models.URLField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True, validators=[validate_year])
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
