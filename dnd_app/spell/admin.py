from django.contrib import admin

from spell.models import (
    MagicAuraStrength,
    MagicSchool,
    MagicSubSchool,
    SpellDescriptor,
    SpellComponent,
    CastingTime,
    SpellRange,
    Spell,
    SpellSpellDescriptor,
    SpellSpellComponent,
    SpellLevel,
)


@admin.register(MagicAuraStrength)
class MagicAuraStrengthAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name",)


@admin.register(MagicSchool)
class MagicSchoolAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name",)


@admin.register(MagicSubSchool)
class MagicSubSchoolAdmin(MagicSchoolAdmin):
    pass


@admin.register(SpellDescriptor)
class SpellDescriptorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name",)


@admin.register(SpellComponent)
class SpellComponentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "short_name", "description")
    search_fields = ("name", "short_name")


@admin.register(CastingTime)
class CastingTimeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "approximate_time_in_seconds")
    search_fields = ("name",)


@admin.register(SpellRange)
class SpellRangeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name",)


class SpellSpellDescriptorInline(admin.TabularInline):
    model = SpellSpellDescriptor
    extra = 1


class SpellLevelInline(admin.TabularInline):
    model = SpellLevel
    extra = 1


class SpellSpellComponentInline(admin.TabularInline):
    model = SpellSpellComponent
    extra = 1


@admin.register(Spell)
class SpellAdmin(admin.ModelAdmin):
    inlines = (
        SpellSpellDescriptorInline,
        SpellLevelInline,
        SpellSpellComponentInline,
    )
    list_display = (
        "id",
        "name",
        "target",
        "effect",
        "area",
        "duration",
        "saving_throw",
        "spell_resistance",
        "school",
        "casting_time",
        "range",
        "subschool",
    )
    search_fields = (
        "name",
        "description",
    )
    list_filter = ("school", "casting_time", "range", "subschool")
