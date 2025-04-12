from django.contrib import admin

from character_class.filters import ClassHitDieFilter, PrestigeClassFilter
from character_class.forms import CharacterClassForm
from character_class.models import (
    CharacterClass,
    ClassAlignment,
    BSBProgression,
    BABProgression,
    ClassSkill,
    ClassTrait,
    ClassBsbProgression,
    ClassBonusLanguage,
    PrestigeCharacterClass,
    PrestigeClassSkillRankRequirement,
    PrestigeClassRaceRequirement,
    PrestigeClassLanguageRequirement,
    PrestigeClassFeatRequirement,
)


class ClassAlignmentInline(admin.TabularInline):
    model = ClassAlignment
    extra = 3


class ClassSkillInline(admin.TabularInline):
    model = ClassSkill
    extra = 5


class ClassTraitInline(admin.TabularInline):
    model = ClassTrait
    extra = 5
    raw_id_fields = ["trait"]

    class Media:
        css = {"all": ("css/trait_inline.css",)}


class ClassBsbProgressionInline(admin.TabularInline):
    model = ClassBsbProgression
    min = 3
    max = 3


class ClassBonusLanguageInline(admin.TabularInline):
    model = ClassBonusLanguage
    extra = 1


@admin.register(CharacterClass)
class ClassAdmin(admin.ModelAdmin):
    form = CharacterClassForm
    inlines = (
        ClassAlignmentInline,
        ClassSkillInline,
        ClassTraitInline,
        ClassBsbProgressionInline,
        ClassBonusLanguageInline,
    )
    list_display = (
        "id",
        "name",
        "skill_points_per_level",
        "hit_die",
    )
    search_fields = ("name",)
    list_filter = (
        ClassHitDieFilter,
        PrestigeClassFilter,
        "skill_points_per_level",
        "required_alignment",
        "bab_progression",
    )
    ordering = ("name",)


@admin.register(BSBProgression)
class BSBProgressionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "save_bonus_table",
    )
    search_fields = ("name",)


@admin.register(BABProgression)
class BABProgressionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "attack_bonus_table",
    )
    search_fields = ("name",)


@admin.register(ClassBsbProgression)
class ClassBsbProgressionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "character_class",
        "bsb_progression",
    )
    search_fields = ("character_class__name",)
    list_filter = ("bsb_progression",)
    raw_id_fields = ("character_class",)


class PrestigeClassSkillRankRequirementInline(admin.TabularInline):
    model = PrestigeClassSkillRankRequirement
    extra = 1


class PrestigeClassRaceRequirementInline(admin.TabularInline):
    model = PrestigeClassRaceRequirement
    extra = 1


class PrestigeClassLanguageRequirementInline(admin.TabularInline):
    model = PrestigeClassLanguageRequirement
    extra = 1


class PrestigeClassFeatRequirementInline(admin.TabularInline):
    model = PrestigeClassFeatRequirement
    extra = 1


@admin.register(PrestigeCharacterClass)
class PrestigeCharacterClassAdmin(ClassAdmin):
    inlines = ClassAdmin.inlines + (
        PrestigeClassSkillRankRequirementInline,
        PrestigeClassRaceRequirementInline,
        PrestigeClassLanguageRequirementInline,
        PrestigeClassFeatRequirementInline,
    )
