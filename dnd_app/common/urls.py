from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from utils.urls_classes import CustomAPIRootView
from .views import (
    SourceViewSet,
    DieViewSet,
    TraitClassificationViewSet,
    TraitViewSet,
    DurationUnitViewSet,
    AbilityViewSet,
    AlignmentViewSet,
    LanguageViewSet,
)


class CharacterClassAPIRootView(CustomAPIRootView):
    custom_name = "Common"
    custom_doc = "Router for the common module."


class CustomCommonRouter(routers.DefaultRouter):
    APIRootView = CharacterClassAPIRootView


router = CustomCommonRouter()
router.register(r"sources", SourceViewSet)
router.register(r"dice", DieViewSet)
router.register(r"trait_classifications", TraitClassificationViewSet)
router.register(r"traits", TraitViewSet)
router.register(r"duration_units", DurationUnitViewSet)
router.register(r"abilities", AbilityViewSet)
router.register(r"alignments", AlignmentViewSet)
router.register(r"languages", LanguageViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
