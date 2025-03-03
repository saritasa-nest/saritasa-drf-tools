from rest_framework import mixins as drf_mixins

from . import base


class ReadOnlyViewSet(
    drf_mixins.RetrieveModelMixin,
    drf_mixins.ListModelMixin,
    base.BaseViewSet,
):
    """Read only viewset for api views."""
