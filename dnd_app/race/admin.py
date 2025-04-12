from django.contrib import admin

from utils.admin_classes import LockedInline
from race.models import (
    Race,
    AbilityModifier,
    RaceAbilityModifier,
    CharacterType,
    RaceLanguage,
    CharacterTypeTrait,
    RaceType,
    RaceTrait,
    Size,
    RaceFavoredClass,
)


@admin.register(AbilityModifier)
class AbilityModifierAdmin(admin.ModelAdmin):
    list_display = ("id", "value", "ability")
    search_fields = (
        "value",
        "ability__name",
    )
    list_filter = ("ability",)


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "size_modifier",
        "grapple_modifier",
        "hide_modifier",
        "height_or_length",
        "weight",
        "space_ft",
        "natural_reach_tall_ft",
        "natural_reach_long_ft",
    )
    search_fields = ("name",)
    list_filter = ()


class CharacterTypeTraitInline(admin.TabularInline):
    model = CharacterTypeTrait
    extra = 2
    raw_id_fields = ["trait"]


@admin.register(CharacterType)
class CharacterTypeAdmin(admin.ModelAdmin):
    inlines = (CharacterTypeTraitInline,)
    list_display = ("id", "name", "description", "subtype", "source")
    search_fields = ()
    list_filter = ("subtype",)


class RaceTypeInline(admin.TabularInline):
    model = RaceType
    extra = 1
    raw_id_fields = ["character_type"]


class RaceAbilityModifierInline(LockedInline):
    model = RaceAbilityModifier
    extra = 2
    raw_id_fields = ["ability_modifier"]


class RaceTraitInline(admin.TabularInline):
    model = RaceTrait
    extra = 2
    raw_id_fields = ["trait"]

    class Media:
        css = {"all": ("css/trait_inline.css",)}


class RaceLanguageInline(admin.TabularInline):
    model = RaceLanguage
    extra = 2
    autocomplete_fields = ["language"]


class RaceFavoredClassInline(admin.TabularInline):
    model = RaceFavoredClass
    extra = 1
    autocomplete_fields = ["character_class"]


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    inlines = (
        RaceTypeInline,
        RaceAbilityModifierInline,
        RaceTraitInline,
        RaceLanguageInline,
        RaceFavoredClassInline,
    )
    list_display = (
        "id",
        "name",
        "size",
        "level_adjustment",
        "source",
    )
    search_fields = ("name",)
    list_filter = ()
