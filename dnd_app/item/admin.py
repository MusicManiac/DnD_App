from django.contrib import admin

from item.models import (
    WeaponMagicAbilityFeat,
    WeaponMagicAbilitySpell,
    ArmorMagicAbilityFeat,
    ArmorMagicAbilitySpell,
    WeaponWeaponCategory,
    WeaponWeaponMagicAbility,
    Weapon,
    WeaponDamageType,
    ArmorMagicAbility,
    WeaponMagicAbility,
    SpecialMaterial,
    Item,
    ArmorType,
    Armor,
    ArmorArmorMagicAbility,
)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "weight_in_lb",
        "price_in_gp",
    )
    list_filter = (
        "category",
        "size",
    )
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(SpecialMaterial)
class SpecialMaterialAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "source",
    )
    search_fields = ("name",)
    ordering = ("name",)


class MagicAbilityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "caster_level_required_for_creation",
    )
    search_fields = (
        "name",
        "description",
    )
    ordering = ("name",)
    list_filter = ("caster_level_required_for_creation",)


class WeaponMagicAbilityFeatInline(admin.TabularInline):
    model = WeaponMagicAbilityFeat
    extra = 1


class WeaponMagicAbilitySpellInline(admin.TabularInline):
    model = WeaponMagicAbilitySpell
    extra = 1


@admin.register(WeaponMagicAbility)
class WeaponMagicAbilityAdmin(MagicAbilityAdmin):
    inlines = (WeaponMagicAbilityFeatInline, WeaponMagicAbilitySpellInline)
    list_display = MagicAbilityAdmin.list_display + (
        "cost_increase_in_bonus",
        "cost_increase_in_gold",
        "magic_aura_strength",
        "magic_aura_type",
    )
    list_filter = MagicAbilityAdmin.list_filter + (
        "cost_increase_in_bonus",
        "magic_aura_strength",
        "magic_aura_type",
    )


class ArmorMagicAbilityFeatInline(admin.TabularInline):
    model = ArmorMagicAbilityFeat
    extra = 1


class ArmorMagicAbilitySpellInline(admin.TabularInline):
    model = ArmorMagicAbilitySpell
    extra = 1


@admin.register(ArmorMagicAbility)
class ArmorMagicAbilityAdmin(MagicAbilityAdmin):
    inlines = (ArmorMagicAbilityFeatInline, ArmorMagicAbilitySpellInline)
    list_display = MagicAbilityAdmin.list_display + (
        "cost_increase_in_bonus",
        "cost_increase_in_gold",
        "magic_aura_strength",
        "magic_aura_type",
    )
    list_filter = MagicAbilityAdmin.list_filter + (
        "cost_increase_in_bonus",
        "magic_aura_strength",
        "magic_aura_type",
    )


@admin.register(WeaponDamageType)
class WeaponDamageTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )
    search_fields = ("name",)
    ordering = ("name",)


class WeaponWeaponCategoryInline(admin.TabularInline):
    model = WeaponWeaponCategory
    extra = 1


class WeaponWeaponMagicAbilityInline(admin.TabularInline):
    model = WeaponWeaponMagicAbility
    extra = 1


@admin.register(Weapon)
class WeaponAdmin(ItemAdmin):
    inlines = (
        WeaponWeaponCategoryInline,
        WeaponWeaponMagicAbilityInline,
    )
    list_display = ItemAdmin.list_display + (
        "damage",
        "crit_multiplier",
        "crit_range",
        "range_increment_in_ft",
        "is_masterwork",
        "enchantment_bonus",
        "special_material",
        "weapon_damage_type",
    )
    list_filter = (
        *[field for field in ItemAdmin.list_filter if field != "category"],
        "crit_multiplier",
        "crit_range",
        "is_masterwork",
        "enchantment_bonus",
        "special_material",
        "weapon_damage_type",
    )
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(ArmorType)
class ArmorTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


class ArmorArmorMagicAbilityInline(admin.TabularInline):
    model = ArmorArmorMagicAbility
    extra = 1


@admin.register(Armor)
class ArmorAdmin(ItemAdmin):
    inlines = (ArmorArmorMagicAbilityInline,)
    list_display = (
        *[field for field in ItemAdmin.list_display if field != "description"],
        "armor_bonus",
        "max_dex_bonus",
        "armor_check_penalty",
        "spell_failure_chance",
        "armor_type",
        "special_material",
        "enchantment_bonus",
    )
    list_filter = (
        *[field for field in ItemAdmin.list_filter if field != "category"],
        "armor_bonus",
        "max_dex_bonus",
        "armor_check_penalty",
        "spell_failure_chance",
        "armor_type",
        "special_material",
    )
    search_fields = ("name",)
    ordering = ("name",)
