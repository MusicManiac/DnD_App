from django.contrib import admin
from .models import Source


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "year", "link", "description")
    search_fields = ("name", "year")
    list_filter = ()
