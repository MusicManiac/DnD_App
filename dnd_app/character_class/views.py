from character_class.models import (
    BSBProgression,
    BABProgression,
    ClassAlignment,
    ClassTrait,
    ClassBsbProgression,
    ClassBonusLanguage,
    ClassSkill,
    PrestigeCharacterClass,
    PrestigeClassSkillRankRequirement,
    PrestigeClassRaceRequirement,
    PrestigeClassLanguageRequirement,
    PrestigeClassFeatRequirement,
    CharacterClass,
)
from character_class.serializers import (
    BSBProgressionSerializer,
    BABProgressionSerializer,
    ClassAlignmentSerializer,
    ClassTraitSerializer,
    ClassBsbProgressionSerializer,
    ClassBonusLanguageSerializer,
    ClassSkillSerializer,
    PrestigeCharacterClassSerializer,
    PrestigeClassSkillRankRequirementSerializer,
    PrestigeClassRaceRequirementSerializer,
    PrestigeClassLanguageRequirementSerializer,
    PrestigeClassFeatRequirementSerializer,
    CharacterClassSerializer,
)
from utils.views import CustomModelViewSet


class BSBProgressionViewSet(CustomModelViewSet):
    queryset = BSBProgression.objects.all()
    serializer_class = BSBProgressionSerializer


class BABProgressionViewSet(CustomModelViewSet):
    queryset = BABProgression.objects.all()
    serializer_class = BABProgressionSerializer


class ClassAlignmentViewSet(CustomModelViewSet):
    queryset = ClassAlignment.objects.all()
    serializer_class = ClassAlignmentSerializer
    custom_view_name = "(Class - Alignment) List"


class ClassSkillViewSet(CustomModelViewSet):
    queryset = ClassSkill.objects.all()
    serializer_class = ClassSkillSerializer
    custom_view_name = "(Class - Skill) List"


class ClassTraitViewSet(CustomModelViewSet):
    queryset = ClassTrait.objects.all()
    serializer_class = ClassTraitSerializer
    custom_view_name = "(Class - Trait) List"


class ClassBsbProgressionViewSet(CustomModelViewSet):
    queryset = ClassBsbProgression.objects.all()
    serializer_class = ClassBsbProgressionSerializer
    custom_view_name = "(Class - BSB Progression) List"


class ClassBonusLanguageViewSet(CustomModelViewSet):
    queryset = ClassBonusLanguage.objects.all()
    serializer_class = ClassBonusLanguageSerializer
    custom_view_name = "(Class - Bonus Language) List"


class CharacterClassViewSet(CustomModelViewSet):
    queryset = CharacterClass.objects.all()
    serializer_class = CharacterClassSerializer


class PrestigeCharacterClassViewSet(CustomModelViewSet):
    queryset = PrestigeCharacterClass.objects.all()
    serializer_class = PrestigeCharacterClassSerializer


class PrestigeClassSkillRankRequirementViewSet(CustomModelViewSet):
    queryset = PrestigeClassSkillRankRequirement.objects.all()
    serializer_class = PrestigeClassSkillRankRequirementSerializer
    custom_view_name = "(Prestige Class - Skill Rank Requirement) List"


class PrestigeClassRaceRequirementViewSet(CustomModelViewSet):
    queryset = PrestigeClassRaceRequirement.objects.all()
    serializer_class = PrestigeClassRaceRequirementSerializer
    custom_view_name = "(Prestige Class - Race Requirement) List"


class PrestigeClassLanguageRequirementViewSet(CustomModelViewSet):
    queryset = PrestigeClassLanguageRequirement.objects.all()
    serializer_class = PrestigeClassLanguageRequirementSerializer
    custom_view_name = "(Prestige Class - Language Requirement) List"


class PrestigeClassFeatRequirementViewSet(CustomModelViewSet):
    queryset = PrestigeClassFeatRequirement.objects.all()
    serializer_class = PrestigeClassFeatRequirementSerializer
    custom_view_name = "(Prestige Class - Feat Requirement) List"
