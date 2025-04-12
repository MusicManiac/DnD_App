from django.contrib import admin

from skill.filters import CraftSkillFilter, ProfessionSkillFilter, PerformSkillFilter
from skill.models import Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "ability", "trained_only")
    list_filter = (
        "ability",
        "trained_only",
        CraftSkillFilter,
        ProfessionSkillFilter,
        PerformSkillFilter,
    )
    search_fields = ("name", "ability")
