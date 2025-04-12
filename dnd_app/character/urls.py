from django.urls import path, include
from rest_framework import routers

from character.views import (
    InventoryViewSet,
    InventoryItemViewSet,
    CharacterViewSet,
    CharacterAbilityScoreViewSet,
    CharacterCharacterClassViewSet,
    CharacterFeatViewSet,
    CharacterLanguageViewSet,
    CharacterInventoryViewSet,
    CharacterSkillViewSet,
)
from utils.urls_classes import CustomAPIRootView


class CharacterClassAPIRootView(CustomAPIRootView):
    custom_name = "Character"
    custom_doc = "Router for the character module."


class CustomCharacterRouter(routers.DefaultRouter):
    APIRootView = CharacterClassAPIRootView


router = CustomCharacterRouter()
router.register(r"inventory", InventoryViewSet)
router.register(r"inventory_item", InventoryItemViewSet)
router.register(r"character", CharacterViewSet)
router.register(r"character_ability_score", CharacterAbilityScoreViewSet)
router.register(r"character_character_class", CharacterCharacterClassViewSet)
router.register(r"character_feat", CharacterFeatViewSet)
router.register(r"character_language", CharacterLanguageViewSet)
router.register(r"character_inventory", CharacterInventoryViewSet)
router.register(r"character_skill", CharacterSkillViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
