# views.py
from rest_framework import viewsets

from utils.views import CustomModelViewSet
from .models import (
    MagicAuraStrength,
    MagicSchool,
    MagicSubSchool,
    SpellDescriptor,
    SpellComponent,
    CastingTime,
    SpellRange,
    Spell,
    SpellSpellDescriptor,
    SpellLevel,
    SpellSpellComponent,
)
from .serializers import (
    MagicAuraStrengthSerializer,
    MagicSchoolSerializer,
    MagicSubSchoolSerializer,
    SpellDescriptorSerializer,
    SpellComponentSerializer,
    CastingTimeSerializer,
    SpellRangeSerializer,
    SpellSerializer,
    SpellSpellDescriptorSerializer,
    SpellLevelSerializer,
    SpellSpellComponentSerializer,
)


class MagicAuraStrengthViewSet(CustomModelViewSet):
    queryset = MagicAuraStrength.objects.all()
    serializer_class = MagicAuraStrengthSerializer


class MagicSchoolViewSet(CustomModelViewSet):
    queryset = MagicSchool.objects.exclude(id__in=MagicSubSchool.objects.values("id"))
    serializer_class = MagicSchoolSerializer


class MagicSubSchoolViewSet(CustomModelViewSet):
    queryset = MagicSubSchool.objects.all()
    serializer_class = MagicSubSchoolSerializer


class SpellDescriptorViewSet(CustomModelViewSet):
    queryset = SpellDescriptor.objects.all()
    serializer_class = SpellDescriptorSerializer


class SpellComponentViewSet(CustomModelViewSet):
    queryset = SpellComponent.objects.all()
    serializer_class = SpellComponentSerializer


class CastingTimeViewSet(CustomModelViewSet):
    queryset = CastingTime.objects.all()
    serializer_class = CastingTimeSerializer


class SpellRangeViewSet(CustomModelViewSet):
    queryset = SpellRange.objects.all()
    serializer_class = SpellRangeSerializer


class SpellViewSet(CustomModelViewSet):
    queryset = Spell.objects.all()
    serializer_class = SpellSerializer


class SpellSpellDescriptorViewSet(CustomModelViewSet):
    queryset = SpellSpellDescriptor.objects.all()
    serializer_class = SpellSpellDescriptorSerializer
    custom_view_name = "(Spell - Spell Descriptor) List"


class SpellLevelViewSet(CustomModelViewSet):
    queryset = SpellLevel.objects.all()
    serializer_class = SpellLevelSerializer
    custom_view_name = "(Spell - Level) List"


class SpellSpellComponentViewSet(CustomModelViewSet):
    queryset = SpellSpellComponent.objects.all()
    serializer_class = SpellSpellComponentSerializer
    custom_view_name = "(Spell - Spell Component) List"
