from rest_framework import serializers

from . import mixins


class BaseSerializer(
    mixins.UserAndRequestFromContextMixin,
    serializers.Serializer,
):
    """Serializer with common logic."""
