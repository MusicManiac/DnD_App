from django.db import IntegrityError
from rest_framework import viewsets, status
from rest_framework.response import Response


class CustomModelViewSet(viewsets.ModelViewSet):
    """
    Custom viewset to override the get_view_name method.
    """

    custom_view_name = None

    def get_view_name(self):
        return (
            super().get_view_name()
            if self.custom_view_name is None
            else self.custom_view_name
        )

    def destroy(self, request, *args, **kwargs):
        object = self.get_object()
        try:
            object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except IntegrityError:
            return Response(
                {
                    "detail": "This object cannot be deleted because it has dependent objects."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
