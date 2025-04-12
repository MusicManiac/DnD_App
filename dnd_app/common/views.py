from utils.views import CustomModelViewSet
from .models import (
    Source,
    Die,
    TraitClassification,
    Trait,
    DurationUnit,
    Ability,
    Alignment,
    Language,
)
from .serializers import (
    SourceSerializer,
    DieSerializer,
    TraitClassificationSerializer,
    TraitSerializer,
    DurationUnitSerializer,
    AbilitySerializer,
    AlignmentSerializer,
    LanguageSerializer,
)


class SourceViewSet(CustomModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer


class DieViewSet(CustomModelViewSet):
    queryset = Die.objects.all()
    serializer_class = DieSerializer


class TraitClassificationViewSet(CustomModelViewSet):
    queryset = TraitClassification.objects.all()
    serializer_class = TraitClassificationSerializer


class TraitViewSet(CustomModelViewSet):
    queryset = Trait.objects.all()
    serializer_class = TraitSerializer


class DurationUnitViewSet(CustomModelViewSet):
    queryset = DurationUnit.objects.all()
    serializer_class = DurationUnitSerializer


class AbilityViewSet(CustomModelViewSet):
    queryset = Ability.objects.all()
    serializer_class = AbilitySerializer


class AlignmentViewSet(CustomModelViewSet):
    queryset = Alignment.objects.all()
    serializer_class = AlignmentSerializer


class LanguageViewSet(CustomModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
