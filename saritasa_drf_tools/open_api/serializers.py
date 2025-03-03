import typing

from rest_framework import serializers


class OpenApiSerializer(serializers.Serializer):
    """Serializer that should be used for customizing open_api spec.

    Made to avoid warnings about unimplemented methods

    """

    def create(self, validated_data: dict[str, typing.Any]) -> typing.Any:
        """Made to avoid warnings about unimplemented methods."""

    def update(
        self,
        instance: typing.Any,
        validated_data: dict[str, typing.Any],
    ) -> typing.Any:
        """Made to avoid warnings about unimplemented methods."""


class DetailSerializer(OpenApiSerializer):
    """To show in spec responses like this {detail: text}."""

    detail = serializers.CharField(help_text="Message from backend")
