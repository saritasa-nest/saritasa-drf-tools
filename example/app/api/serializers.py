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
            "related_model_id",
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
    """List Serializer."""

    related_model = RelatedTestModelSerializer(
        read_only=True,
    )

    class Meta:
        model = models.TestModel
        fields = (
            "id",
            "text_field",
            "related_model_id",
            "related_model",
        )
