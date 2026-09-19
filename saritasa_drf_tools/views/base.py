from rest_framework import serializers, viewsets

from . import mixins


class BaseViewSet(  # type: ignore
    mixins.ActionPermissionsMixin,
    mixins.ActionSerializerMixin,
    viewsets.GenericViewSet,
):
    """Base viewset for api."""

    def get_serializer(  # type: ignore
        self,
        *args,  # noqa: ANN002
        **kwargs,
    ) -> serializers.Serializer:
        """Get serializer instance for view's action."""
        return super().get_serializer(*args, **kwargs)
