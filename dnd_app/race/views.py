from race.models import (
    AbilityModifier,
    Race,
    CharacterTypeTrait,
    CharacterType,
    Size,
    RaceType,
    RaceAbilityModifier,
    RaceTrait,
    RaceLanguage,
    RaceFavoredClass,
)
from race.serializers import (
    RaceSerializer,
    RaceTypeSerializer,
    AbilityModifierSerializer,
    SizeSerializer,
    CharacterTypeSerializer,
    CharacterTypeTraitSerializer,
    RaceAbilityModifierSerializer,
    RaceTraitSerializer,
    RaceLanguageSerializer,
    RaceFavoredClassSerializer,
)
from utils.views import CustomModelViewSet


class AbilityModifierViewSet(CustomModelViewSet):
    queryset = AbilityModifier.objects.all()
    serializer_class = AbilityModifierSerializer


class SizeViewSet(CustomModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer


class CharacterTypeViewSet(CustomModelViewSet):
    queryset = CharacterType.objects.all()
    serializer_class = CharacterTypeSerializer


class CharacterTypeTraitViewSet(CustomModelViewSet):
    queryset = CharacterTypeTrait.objects.all()
    serializer_class = CharacterTypeTraitSerializer
    custom_view_name = "(Character Type - Trait) List"


class RaceViewSet(CustomModelViewSet):
    queryset = Race.objects.all()
    serializer_class = RaceSerializer


class RaceTypeViewSet(CustomModelViewSet):
    queryset = RaceType.objects.all()
    serializer_class = RaceTypeSerializer
    custom_view_name = "(Race - Type) List"


class RaceAbilityModifierViewSet(CustomModelViewSet):
    queryset = RaceAbilityModifier.objects.all()
    serializer_class = RaceAbilityModifierSerializer
    custom_view_name = "(Race - Ability Modifier) List"


class RaceTraitViewSet(CustomModelViewSet):
    queryset = RaceTrait.objects.all()
    serializer_class = RaceTraitSerializer
    custom_view_name = "(Race - Trait) List"


class RaceLanguageViewSet(CustomModelViewSet):
    queryset = RaceLanguage.objects.all()
    serializer_class = RaceLanguageSerializer
    custom_view_name = "(Race - Language) List"


class RaceFavoredClassViewSet(CustomModelViewSet):
    queryset = RaceFavoredClass.objects.all()
    serializer_class = RaceFavoredClassSerializer
    custom_view_name = "(Race - Favored Class) List"
