from django.contrib import admin
from .models import (
    Source,
    Die,
    TraitClassification,
    Trait,
    DurationUnit,
    Ability,
    Alignment,
    Language,
)


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "year", "link", "description")
    search_fields = ("name", "year")
    list_filter = ()


@admin.register(Die)
class DieAdmin(admin.ModelAdmin):
    list_display = ("id", "sides")
    search_fields = ("sides",)
    list_filter = ()


@admin.register(TraitClassification)
class TraitClassificationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name", "description")
    list_filter = ()


@admin.register(Trait)
class TraitAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "short_description",
        "trait_classification",
    )
    search_fields = ("short_description", "long_description")
    list_filter = ("trait_classification",)


@admin.register(DurationUnit)
class DurationUnitAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "duration_in_seconds")
    search_fields = ("name",)
    list_filter = ()


@admin.register(Ability)
class AbilityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "abbreviation", "description")
    search_fields = ()
    list_filter = ()


@admin.register(Alignment)
class AlignmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "abbreviation", "description")
    search_fields = ("name", "abbreviation")
    list_filter = ()


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "alphabet", "is_secret", "source")
    search_fields = ("name",)
    list_filter = ("alphabet", "is_secret")
