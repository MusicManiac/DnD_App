from django.contrib.admin import SimpleListFilter


class DefaultIncludeExcludeFilter(SimpleListFilter):
    """
    Base class for custom filters in the admin interface.
    """

    def choices(self, changelist):
        default_value = "include"
        if self.value() is None:
            self.used_parameters[self.parameter_name] = default_value
        for lookup, title in self.lookup_choices:
            yield {
                "selected": self.value() == lookup,
                "query_string": changelist.get_query_string(
                    {self.parameter_name: lookup}
                ),
                "display": title,
            }
