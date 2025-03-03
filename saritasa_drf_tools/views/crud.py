from rest_framework import mixins as drf_mixins

from . import base, mixins


class CRUDViewSet(
    drf_mixins.RetrieveModelMixin,
    drf_mixins.ListModelMixin,
    drf_mixins.CreateModelMixin,
    mixins.UpdateModelWithoutPatchMixin,
    drf_mixins.DestroyModelMixin,
    base.BaseViewSet,
):
    """CRUD viewset for api views."""
