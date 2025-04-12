from django.utils.safestring import mark_safe
from rest_framework import routers


class CustomAPIRootView(routers.APIRootView):
    """
    Controls appearance of the API root view
    """

    custom_name = "Name"
    custom_doc = "Description"

    def get_view_name(self) -> str:
        return self.custom_name

    def get_view_description(self, html=False) -> str:
        if html:
            return mark_safe(f"<p>{self.custom_doc}</p>")
        else:
            return self.custom_doc
