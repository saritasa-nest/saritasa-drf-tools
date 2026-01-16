import typing

from django.db import transaction

import saritasa_drf_tools.serializers

from .. import models


class TestModelListSerializer(
    saritasa_drf_tools.serializers.ModelBaseSerializer,
):
    """List Serializer."""

    class Meta:
        model = models.TestModel
        fields = (
            "id",
            "text_field",
            "related_model",
        )


class RelatedTestModelSerializer(
    saritasa_drf_tools.serializers.ModelBaseSerializer,
):
    """Serializer for related model."""

    class Meta:
        model = models.TestRelatedModel
        fields = ("id",)


class TestModelDetailSerializer(
    saritasa_drf_tools.serializers.ModelBaseSerializer,
):
    """Detail Serializer."""

    class Meta:
        model = models.TestModel
        fields = (
            "id",
            "text_field",
            "related_model",
        )
        nested_fields = {
            "related_model": (
                "example.app.api.serializers.RelatedTestModelSerializer"
            ),
        }

    def update(
        self,
        instance: models.TestModel,
        validated_data: dict[str, typing.Any],
    ) -> models.TestModel:
        """Extend update logic to add `on_commit` hook."""
        instance = super().update(
            instance=instance,
            validated_data=validated_data,
        )

        def update_instance_text_field(instance: models.TestModel) -> None:
            """Update instance text field after commit."""
            instance.text_field = f"Updated {instance.id}"
            instance.save()

        transaction.on_commit(
            lambda: update_instance_text_field(instance),
        )

        return instance


class RelatedTestModelWithManyRelatedSerializer(
    saritasa_drf_tools.serializers.ModelBaseSerializer,
):
    """Serializer for related mode with list of test models."""

    class Meta:
        model = models.TestRelatedModel
        fields = (
            "id",
            "text_field",
            "test_models",
        )
        nested_fields = {
            "test_models": (
                "example.app.api.serializers.TestModelListSerializer"
            ),
        }
