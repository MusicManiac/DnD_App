from django.urls import path, include
from rest_framework import routers

from character_class.views import (
    CharacterClassViewSet,
    ClassAlignmentViewSet,
    ClassSkillViewSet,
    ClassTraitViewSet,
    ClassBsbProgressionViewSet,
    ClassBonusLanguageViewSet,
    BSBProgressionViewSet,
    BABProgressionViewSet,
    PrestigeCharacterClassViewSet,
    PrestigeClassSkillRankRequirementViewSet,
    PrestigeClassRaceRequirementViewSet,
    PrestigeClassLanguageRequirementViewSet,
    PrestigeClassFeatRequirementViewSet,
)
from utils.urls_classes import CustomAPIRootView


class CharacterClassAPIRootView(CustomAPIRootView):
    custom_name = "Character Class"
    custom_doc = "Router for the Character Class module."


class CustomCharacterClassRouter(routers.DefaultRouter):
    APIRootView = CharacterClassAPIRootView


router = CustomCharacterClassRouter()
router.register(r"bsb_progression", BSBProgressionViewSet)
router.register(r"bab_progression", BABProgressionViewSet)
router.register(r"character_classes", CharacterClassViewSet)
router.register(r"class_alignments", ClassAlignmentViewSet)
router.register(r"class_skills", ClassSkillViewSet)
router.register(r"class_traits", ClassTraitViewSet)
router.register(r"class_bsb_progressions", ClassBsbProgressionViewSet)
router.register(r"class_bonus_languages", ClassBonusLanguageViewSet)
router.register(r"prestige_character_classes", PrestigeCharacterClassViewSet)
router.register(
    r"prestige_class_skill_rank_requirements", PrestigeClassSkillRankRequirementViewSet
)
router.register(
    r"prestige_class_race_requirements", PrestigeClassRaceRequirementViewSet
)
router.register(
    r"prestige_class_language_requirements", PrestigeClassLanguageRequirementViewSet
)
router.register(
    r"prestige_class_feat_requirements", PrestigeClassFeatRequirementViewSet
)


urlpatterns = [
    path("", include(router.urls)),
]
