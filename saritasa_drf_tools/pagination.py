import typing

from django.conf import settings
from django.db import models
from rest_framework import pagination, request, views
from rest_framework.settings import api_settings


class LimitOffsetPagination(pagination.LimitOffsetPagination):
    """Customized paginator class to limit max objects in list APIs."""

    def paginate_queryset(
        self,
        queryset: models.QuerySet,
        request: request.Request,
        view: views.APIView | None = None,
    ) -> list[typing.Any] | None:
        """Set view for pagination."""
        self.view = view
        return super().paginate_queryset(queryset, request, view)

    @property
    def max_limit(self) -> int | None:
        """Get limit for page.

        Will become deprecated once this is merged
        https://github.com/encode/django-rest-framework/pull/9107

        """
        max_limit_from_view = getattr(
            self.view,
            "pagination_max_limit",
            None,
        )
        max_limit_from_settings = getattr(
            settings,
            "SARITASA_DRF_MAX_PAGINATION_SIZE",
            None,
        )
        return max_limit_from_view or max_limit_from_settings

    @property
    def default_limit(self) -> int | None:
        """Get default limit for page."""
        default_limit_from_view = getattr(
            self.view,
            "pagination_default_limit",
            None,
        )
        default_limit_from_settings: int = api_settings.PAGE_SIZE  # type: ignore
        return default_limit_from_view or default_limit_from_settings
