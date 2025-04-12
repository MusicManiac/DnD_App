from django.urls import path, include
from django.utils.safestring import mark_safe
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from utils.urls_classes import CustomAPIRootView
from .views import (
    TypeOfFeatViewSet,
    FeatViewSet,
    FeatTypeOfFeatViewSet,
    FeatAbilityPrerequisiteViewSet,
    FeatFeatPrerequisiteViewSet,
    FeatSkillPrerequisiteViewSet,
)


class FeatAPIRootView(CustomAPIRootView):
    custom_name = "Feat"
    custom_doc = "Router for the feat module."


class CustomFeatRouter(routers.DefaultRouter):
    APIRootView = FeatAPIRootView


router = CustomFeatRouter()
router.register(r"types_of_feats", TypeOfFeatViewSet)
router.register(r"feats", FeatViewSet)
router.register(r"feat_types_of_feats", FeatTypeOfFeatViewSet)
router.register(r"feat_ability_prerequisites", FeatAbilityPrerequisiteViewSet)
router.register(r"feat_feat_prerequisites", FeatFeatPrerequisiteViewSet)
router.register(r"feat_skill_prerequisites", FeatSkillPrerequisiteViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
