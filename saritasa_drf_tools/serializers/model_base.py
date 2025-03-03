from rest_framework import serializers

from . import mixins


class ModelBaseSerializer(
    mixins.FieldMappingOverride,
    mixins.CleanValidationMixin,
    mixins.UserAndRequestFromContextMixin,
    serializers.ModelSerializer,
):
    """Model Serializer with common logic."""
