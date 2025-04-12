from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from utils.urls_classes import CustomAPIRootView
from .views import (
    SkillViewSet,
)


class SkillAPIRootView(CustomAPIRootView):
    custom_name = "Skill"
    custom_doc = "Router for the skill module."


class CustomSkillRouter(routers.DefaultRouter):
    APIRootView = SkillAPIRootView


router = CustomSkillRouter()
router.register(r"skill", SkillViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
