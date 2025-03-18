from django.conf import settings
from rest_framework import pagination


class LimitOffsetPagination(pagination.LimitOffsetPagination):
    """Customized paginator class to limit max objects in list APIs.

    Will become deprecated once this is merged
    https://github.com/encode/django-rest-framework/pull/9107

    """

    @property
    def max_limit(self) -> int | None:
        """Get limit for page."""
        return getattr(settings, "SARITASA_DRF_MAX_PAGINATION_SIZE", None)
