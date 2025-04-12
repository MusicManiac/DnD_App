from django.contrib.admin import SimpleListFilter

from character_class.models import PrestigeCharacterClass
from utils.filters import DefaultIncludeExcludeFilter
from common.models import Die


class ClassHitDieFilter(SimpleListFilter):
    """
    Custom filter to exclude some Dice from HD choices.
    """

    title = "hit die"
    parameter_name = "hit_die"

    def lookups(self, request, model_admin):
        hit_die_choices = Die.objects.class_hd_list()
        return [(hd.id, str(hd)) for hd in hit_die_choices]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(hit_die__id=self.value())
        return queryset


class PrestigeClassFilter(DefaultIncludeExcludeFilter):
    """
    Filter to include or exclude prestige classes in the admin interface.
    """

    title = "Prestige Class"
    parameter_name = "prestige_class"

    def lookups(self, request, model_admin):
        return (
            ("include", "Include Prestige Classes"),
            ("exclude", "Exclude Prestige Classes"),
            ("only", "Only Prestige Classes"),
        )

    def queryset(self, request, queryset):
        if self.value() == "exclude":
            return queryset.exclude(
                id__in=PrestigeCharacterClass.objects.values_list("id", flat=True)
            )
        elif self.value() == "only":
            return queryset.filter(
                id__in=PrestigeCharacterClass.objects.values_list("id", flat=True)
            )
        return queryset
