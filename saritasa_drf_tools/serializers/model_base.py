import typing

from django.contrib.auth import models as auth_models
from django.db import models
from rest_framework import serializers

from . import mixins


class ModelBaseSerializer[
    User: auth_models.AbstractBaseUser,
    Model: models.Model,
](
    mixins.FieldMappingOverride,
    mixins.CleanValidationMixin,
    mixins.UserAndRequestFromContextMixin[User],
    mixins.NestedFieldsMixin,
    serializers.ModelSerializer,
):
    """Model Serializer with common logic."""

    instance: Model | None = None

    def create(self, validated_data: dict[str, typing.Any]) -> Model:
        """Override for better typing."""
        return super().create(validated_data)

    def update(
        self,
        instance: Model,
        validated_data: dict[str, typing.Any],
    ) -> Model:
        """Override for better typing."""
        return super().update(instance, validated_data)

    def save(self, **kwargs) -> Model:
        """Override for better typing."""
        return super().save(**kwargs)
