from utils.filters import DefaultIncludeExcludeFilter


class CraftSkillFilter(DefaultIncludeExcludeFilter):
    """
    Filter to include or exclude Craft skills in the admin interface.
    """

    title = "Craft skills"
    parameter_name = "craft_skills"

    def lookups(self, request, model_admin):
        return (
            ("include", "Include Craft skills"),
            ("exclude", "Exclude Craft skills"),
            ("only", "Only Craft skills"),
        )

    def queryset(self, request, queryset):
        if self.value() == "exclude":
            return queryset.exclude(name__startswith="Craft")
        elif self.value() == "only":
            return queryset.filter(name__startswith="Craft")
        return queryset


class ProfessionSkillFilter(DefaultIncludeExcludeFilter):
    """
    Filter to include or exclude Profession skills in the admin interface.
    """

    title = "Profession skills"
    parameter_name = "profession_skills"

    def lookups(self, request, model_admin):
        return (
            ("include", "Include Profession skills"),
            ("exclude", "Exclude Profession skills"),
            ("exclude", "Only Profession skills"),
        )

    def queryset(self, request, queryset):
        if self.value() == "exclude":
            return queryset.exclude(name__startswith="Profession")
        elif self.value() == "only":
            return queryset.filter(name__startswith="Profession")
        return queryset


class PerformSkillFilter(DefaultIncludeExcludeFilter):
    """
    Filter to include or exclude Profession skills in the admin interface.
    """

    title = "Perform skills"
    parameter_name = "perform_skills"

    def lookups(self, request, model_admin):
        return (
            ("include", "Include Perform skills"),
            ("exclude", "Exclude Perform skills"),
            ("only", "Only Perform skills"),
        )

    def queryset(self, request, queryset):
        if self.value() == "exclude":
            return queryset.exclude(name__startswith="Perform")
        elif self.value() == "only":
            return queryset.filter(name__startswith="Perform")
        return queryset
