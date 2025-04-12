from utils.views import CustomModelViewSet
from .models import (
    TypeOfFeat,
    Feat,
    FeatTypeOfFeat,
    FeatAbilityPrerequisite,
    FeatFeatPrerequisite,
    FeatSkillPrerequisite,
)
from .serializers import (
    TypeOfFeatSerializer,
    FeatSerializer,
    FeatTypeOfFeatSerializer,
    FeatAbilityPrerequisiteSerializer,
    FeatFeatPrerequisiteSerializer,
    FeatSkillPrerequisiteSerializer,
)


class TypeOfFeatViewSet(CustomModelViewSet):
    queryset = TypeOfFeat.objects.all()
    serializer_class = TypeOfFeatSerializer


class FeatViewSet(CustomModelViewSet):
    queryset = Feat.objects.all()
    serializer_class = FeatSerializer


class FeatTypeOfFeatViewSet(CustomModelViewSet):
    queryset = FeatTypeOfFeat.objects.all()
    serializer_class = FeatTypeOfFeatSerializer
    custom_view_name = "(Feat - Type of Feat) List"


class FeatAbilityPrerequisiteViewSet(CustomModelViewSet):
    queryset = FeatAbilityPrerequisite.objects.all()
    serializer_class = FeatAbilityPrerequisiteSerializer
    custom_view_name = "(Feat - Ability Prerequisite) List"


class FeatFeatPrerequisiteViewSet(CustomModelViewSet):
    queryset = FeatFeatPrerequisite.objects.all()
    serializer_class = FeatFeatPrerequisiteSerializer
    custom_view_name = "(Feat - Feat Prerequisite) List"


class FeatSkillPrerequisiteViewSet(CustomModelViewSet):
    queryset = FeatSkillPrerequisite.objects.all()
    serializer_class = FeatSkillPrerequisiteSerializer
    custom_view_name = "(Feat - Skill Prerequisite) List"
