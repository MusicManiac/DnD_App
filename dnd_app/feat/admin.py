from django.contrib import admin

from feat.models import (
    Feat,
    TypeOfFeat,
    FeatTypeOfFeat,
    FeatAbilityPrerequisite,
    FeatFeatPrerequisite,
    FeatSkillPrerequisite,
)


@admin.register(TypeOfFeat)
class TypeOfFeatAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )
    search_fields = ("name", "description")
    ordering = ("name",)


class FeatTypeOfFeatInline(admin.TabularInline):
    model = FeatTypeOfFeat
    extra = 1


class FeatAbilityPrerequisiteInline(admin.TabularInline):
    model = FeatAbilityPrerequisite
    extra = 1


class FeatFeatPrerequisiteInline(admin.TabularInline):
    model = FeatFeatPrerequisite
    fk_name = "prerequisite_for_feat"
    extra = 1


class FeatSkillPrerequisiteInline(admin.TabularInline):
    model = FeatSkillPrerequisite
    extra = 1


@admin.register(Feat)
class FeatAdmin(admin.ModelAdmin):
    inlines = (
        FeatTypeOfFeatInline,
        FeatAbilityPrerequisiteInline,
        FeatFeatPrerequisiteInline,
        FeatSkillPrerequisiteInline,
    )
    list_display = (
        "name",
        "benefit",
    )
    search_fields = (
        "name",
        "benefit",
    )
    ordering = ("name",)
    list_filter = ("feat_type",)
