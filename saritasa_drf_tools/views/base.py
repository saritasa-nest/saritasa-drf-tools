from rest_framework.viewsets import GenericViewSet

from . import mixins


class BaseViewSet(  # type: ignore
    mixins.ActionPermissionsMixin,
    mixins.ActionSerializerMixin,
    GenericViewSet,
):
    """Base viewset for api."""
