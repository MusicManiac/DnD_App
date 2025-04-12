from django.db import models


class DieQuerySet(models.QuerySet):
    def class_hd_list(self):
        return self.filter(sides__in=[4, 6, 8, 10, 12])
