from django.contrib import admin

from character.models import (
    Attribute,
    Race,
    AttributeModifier,
    RaceAttributeModifier,
    Alignment,
    CharacterType,
    Language,
    RaceLanguage,
    TraitClassification,
    Trait,
    CharacterTypeTrait,
)


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "abbreviation", "description")
    search_fields = ()
    list_filter = ()


@admin.register(AttributeModifier)
class AttributeModifierAdmin(admin.ModelAdmin):
    list_display = ("id", "value", "attribute")
    search_fields = (
        "value",
        "attribute__name",
    )
    list_filter = ("attribute",)
    ordering = ("attribute__name", "value")


@admin.register(Alignment)
class AlignmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "abbreviation", "description")
    search_fields = ("name", "abbreviation")
    list_filter = ()


@admin.register(TraitClassification)
class TraitClassificationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name", "description")
    list_filter = ()


@admin.register(Trait)
class TraitAdmin(admin.ModelAdmin):
    list_display = ("id", "short_description", "long_description")
    search_fields = ("short_description", "long_description")
    list_filter = ("trait_classification",)


class CharacterTypeTraitInline(admin.TabularInline):
    model = CharacterTypeTrait
    extra = 2
    raw_id_fields = ["trait"]


@admin.register(CharacterType)
class CharacterTypeAdmin(admin.ModelAdmin):
    inlines = (CharacterTypeTraitInline,)
    list_display = ("id", "name", "description", "source")
    search_fields = ()
    list_filter = ()


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "source")
    search_fields = ("name",)


class RaceLanguageInline(admin.TabularInline):
    model = RaceLanguage
    extra = 2
    autocomplete_fields = ["language"]


class RaceAttributeModifierInline(admin.TabularInline):
    model = RaceAttributeModifier
    extra = 2
    raw_id_fields = ["attribute_modifier"]


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    inlines = (RaceAttributeModifierInline, RaceLanguageInline)
    list_display = (
        "id",
        "name",
        "description",
        "source",
    )
    search_fields = ("name",)
    list_filter = ()
