# urls.py
from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from utils.urls_classes import CustomAPIRootView
from .views import (
    MagicAuraStrengthViewSet,
    MagicSchoolViewSet,
    MagicSubSchoolViewSet,
    SpellDescriptorViewSet,
    SpellComponentViewSet,
    CastingTimeViewSet,
    SpellRangeViewSet,
    SpellViewSet,
    SpellSpellDescriptorViewSet,
    SpellLevelViewSet,
    SpellSpellComponentViewSet,
)


class SpellAPIRootView(CustomAPIRootView):
    custom_name = "Spell"
    custom_doc = "Router for the spells module."


class CustomSpellRouter(routers.DefaultRouter):
    APIRootView = SpellAPIRootView


router = CustomSpellRouter()
router.register(r"magic_aura_strength", MagicAuraStrengthViewSet)
router.register(r"magic_schools", MagicSchoolViewSet)
router.register(r"magic_subschools", MagicSubSchoolViewSet)
router.register(r"spell_descriptors", SpellDescriptorViewSet)
router.register(r"spell_components", SpellComponentViewSet)
router.register(r"casting_times", CastingTimeViewSet)
router.register(r"spell_ranges", SpellRangeViewSet)
router.register(r"spells", SpellViewSet)
router.register(r"spell_spell_descriptors", SpellSpellDescriptorViewSet)
router.register(r"spell_levels", SpellLevelViewSet)
router.register(r"spell_spell_components", SpellSpellComponentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
