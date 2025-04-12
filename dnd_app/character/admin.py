from django.contrib import admin

from character.forms import CharacterForm, CharacterCharacterClassForm
from character.models import (
    Character,
    CharacterAbilityScore,
    CharacterCharacterClass,
    CharacterFeat,
    CharacterLanguage,
    Inventory,
    CharacterSkill,
    InventoryItem,
    CharacterInventory,
)
from utils.admin_classes import LockedInline


class InventoryItemInline(admin.TabularInline):
    model = InventoryItem
    extra = 5
    raw_id_fields = ("item",)
    readonly_fields = ("item_stack_weight", "item_stack_value")


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    inlines = (InventoryItemInline,)
    list_display = (
        "id",
        "character_ids",
        "name",
        "capacity",
        "total_weight",
        "total_value",
        "available_capacity",
    )
    search_fields = ("name",)

    # Custom method to display related Character IDs
    def character_ids(self, obj):
        # Get the related CharacterInventory objects and return the Character IDs
        return ", ".join(
            str(ci.character.id) for ci in obj.characterinventory_set.all()
        )

    character_ids.short_description = "Character ID(s)"


class CharacterAbilityScoreInline(LockedInline):
    model = CharacterAbilityScore
    extra = 0
    min_num = 6
    max_num = 6
    verbose_name_plural = "Ability Scores"
    readonly_fields = ("modifier",)
    raw_id_fields = ("ability",)


class CharacterCharacterClassInline(admin.TabularInline):
    form = CharacterCharacterClassForm
    model = CharacterCharacterClass
    extra = 0
    min_num = 1
    verbose_name_plural = "Character Classes"


class CharacterFeatInline(LockedInline):
    model = CharacterFeat
    extra = 0
    raw_id_fields = ("feat",)


class CharacterLanguageInline(LockedInline):
    model = CharacterLanguage
    extra = 0
    raw_id_fields = ("language",)


class CharacterInventoryInline(admin.TabularInline):
    model = CharacterInventory
    extra = 1
    raw_id_fields = ("inventory",)


class CharacterSkillInline(LockedInline):
    model = CharacterSkill
    extra = 0
    readonly_fields = ("total_bonus",)


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    form = CharacterForm
    inlines = (
        CharacterAbilityScoreInline,
        CharacterCharacterClassInline,
        CharacterFeatInline,
        CharacterLanguageInline,
        CharacterInventoryInline,
        CharacterSkillInline,
    )
    list_display = ("id", "name", "race", "alignment", "level")
    readonly_fields = (
        "class_levels",
        "fortitude_save",
        "reflex_save",
        "will_save",
        "multiattack_bab",
        "initiative",
        "list_of_languages",
    )
    search_fields = ("name",)
    list_filter = ("alignment", "level")
    raw_id_fields = ("additionally_learned_languages",)
