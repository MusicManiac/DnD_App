from django.contrib import admin


class LockedInline(admin.TabularInline):
    """
    This inline is disabled until parent object is saved. Mostly used for custom complex M2M relations with very specific constrains.
    Or to auto populate M2M relations based on other fields in the parent object.
    """

    verbose_name_plural = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.model:
            self.verbose_name_plural = (
                self.model._meta.verbose_name_plural
                + " (This section is disabled until the object is saved.)"
            )

    def has_add_permission(self, request, obj=None):
        if obj and obj.pk:
            self.verbose_name_plural = self.model._meta.verbose_name_plural
            return True
        self.verbose_name_plural = (
            self.model._meta.verbose_name_plural
            + "(This section is disabled until the object is saved.)"
        )
        return False
