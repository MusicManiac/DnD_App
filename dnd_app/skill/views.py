from utils.views import CustomModelViewSet
from .models import (
    Skill,
)
from .serializers import SkillSerializer


class SkillViewSet(CustomModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
