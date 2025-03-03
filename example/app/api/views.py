from drf_standardized_errors import handler
from rest_framework import permissions, response, status, views

import saritasa_drf_tools.open_api
import saritasa_drf_tools.views

from .. import models
from . import filters, serializers


class CRUDView(saritasa_drf_tools.views.CRUDViewSet):
    """CRUD view."""

    queryset = models.TestModel.objects.select_related("related_model").all()
    serializers_map = {  # noqa: RUF012
        "default": serializers.TestModelDetailSerializer,
        "list": serializers.TestModelListSerializer,
    }
    base_permission_classes = (permissions.AllowAny,)
    extra_permission_classes = (permissions.IsAuthenticated,)
    extra_permissions_map = {  # noqa: RUF012
        "create": (permissions.IsAdminUser,),
        "update": (permissions.IsAdminUser,),
        "destroy": (permissions.IsAdminUser,),
    }

    search_fields = (
        "text_field",
        "related_model__text_field",
    )
    ordering_fields = (
        "id",
        "text_field",
        "related_model__text_field",
    )
    filterset_class = filters.TestModelFilter


class DRFStandardizedErrorsCRUDView(CRUDView):
    """CRUD view with enabled."""

    def get_exception_handler(self):  # noqa: ANN201
        """Customize exception handler."""
        return handler.exception_handler


class ReadOnlyView(saritasa_drf_tools.views.ReadOnlyViewSet):
    """Read only view."""

    queryset = models.TestModel.objects.select_related("related_model").all()
    serializer_class = serializers.TestModelListSerializer
    base_permission_classes = (permissions.IsAuthenticated,)
    search_fields = (
        "text_field",
        "related_model__text_field",
    )
    ordering_fields = (
        "id",
        "text_field",
        "related_model__text_field",
    )


class APIView(views.APIView):
    """Simple API view."""

    def get(
        self,
        request,  # noqa: ANN001
        *args,  # noqa: ANN002
        **kwargs,
    ) -> response.Response:
        """Return simple response."""
        return response.Response(
            saritasa_drf_tools.open_api.DetailSerializer(
                {"detail": "This is simple API"},
            ),
            status=status.HTTP_200_OK,
        )
