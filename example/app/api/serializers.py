import typing

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
        data_fields: typing.ClassVar = {
            "related_model": (
                "example.app.api.serializers.RelatedTestModelSerializer"
            ),
        }


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
        data_fields: typing.ClassVar = {
            "test_models": (
                "example.app.api.serializers.TestModelListSerializer"
            ),
        }
