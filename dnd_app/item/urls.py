from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from item.views import (
    ItemCategoryViewSet,
    ItemViewSet,
    SpecialMaterialViewSet,
    WeaponMagicAbilityViewSet,
    WeaponMagicAbilityFeatViewSet,
    WeaponMagicAbilitySpellViewSet,
    ArmorMagicAbilityViewSet,
    ArmorMagicAbilityFeatViewSet,
    ArmorMagicAbilitySpellViewSet,
    WeaponCategoryViewSet,
    WeaponDamageTypeViewSet,
    WeaponViewSet,
    WeaponWeaponCategoryViewSet,
    WeaponWeaponDamageTypeViewSet,
    WeaponWeaponMagicAbilityViewSet,
    ArmorTypeViewSet,
    ArmorViewSet,
    ArmorArmorMagicAbilityViewSet,
)
from utils.urls_classes import CustomAPIRootView


class FeatAPIRootView(CustomAPIRootView):
    custom_name = "Item"
    custom_doc = "Router for the item module."


class CustomItemRouter(routers.DefaultRouter):
    APIRootView = FeatAPIRootView


router = CustomItemRouter()
router.register(r"item_category", ItemCategoryViewSet)
router.register(r"item", ItemViewSet)
router.register(r"special_material", SpecialMaterialViewSet)
router.register(r"weapon_magic_ability", WeaponMagicAbilityViewSet)
router.register(r"weapon_magic_ability_feat", WeaponMagicAbilityFeatViewSet)
router.register(r"weapon_magic_ability_spell", WeaponMagicAbilitySpellViewSet)
router.register(r"armor_magic_ability", ArmorMagicAbilityViewSet)
router.register(r"armor_magic_ability_feat", ArmorMagicAbilityFeatViewSet)
router.register(r"armor_magic_ability_spell", ArmorMagicAbilitySpellViewSet)
router.register(r"weapon_category", WeaponCategoryViewSet)
router.register(r"weapon_damage_type", WeaponDamageTypeViewSet)
router.register(r"weapon", WeaponViewSet)
router.register(r"weapon_weapon_category", WeaponWeaponCategoryViewSet)
router.register(r"weapon_weapon_damage_type", WeaponWeaponDamageTypeViewSet)
router.register(r"weapon_weapon_magic_ability", WeaponWeaponMagicAbilityViewSet)
router.register(r"armor_type", ArmorTypeViewSet)
router.register(r"armor", ArmorViewSet)
router.register(r"armor_armor_magic_ability", ArmorArmorMagicAbilityViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
