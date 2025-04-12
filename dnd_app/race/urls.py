from django.urls import path, include
from rest_framework import routers


from utils.urls_classes import CustomAPIRootView
from .views import (
    AbilityModifierViewSet,
    SizeViewSet,
    CharacterTypeViewSet,
    CharacterTypeTraitViewSet,
    RaceAbilityModifierViewSet,
    RaceViewSet,
    RaceTypeViewSet,
    RaceTraitViewSet,
    RaceLanguageViewSet,
    RaceFavoredClassViewSet,
)


class RaceAPIRootView(CustomAPIRootView):
    custom_name = "Race"
    custom_doc = "Router for the race module."


class CustomRaceRouter(routers.DefaultRouter):
    APIRootView = RaceAPIRootView


router = CustomRaceRouter()
router.register(r"ability_modifier", AbilityModifierViewSet)
router.register(r"size", SizeViewSet)
router.register(r"character_type", CharacterTypeViewSet)
router.register(r"character_type_trait", CharacterTypeTraitViewSet)
router.register(r"race_ability_modifier", RaceAbilityModifierViewSet)
router.register(r"race", RaceViewSet)
router.register(r"race_type", RaceTypeViewSet)
router.register(r"race_trait", RaceTraitViewSet)
router.register(r"race_language", RaceLanguageViewSet)
router.register(r"race_favored_class", RaceFavoredClassViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
