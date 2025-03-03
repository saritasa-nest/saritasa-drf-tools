from django.conf import settings
from rest_framework import pagination


class LimitOffsetPagination(pagination.LimitOffsetPagination):
    """Customized paginator class to limit max objects in list APIs."""

    @property
    def max_limit(self) -> int | None:
        """Get limit for page."""
        return getattr(settings, "SARITASA_DRF_MAX_PAGINATION_SIZE", None)
