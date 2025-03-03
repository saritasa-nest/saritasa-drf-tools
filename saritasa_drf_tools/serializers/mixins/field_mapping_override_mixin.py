from django.conf import settings
from django.db import models
from django.utils.module_loading import import_string
from rest_framework import serializers


class FieldMappingOverride:
    """Override or extend field mapping via SARITASA_DRF_FIELD_MAPPING."""

    @property
    def serializer_field_mapping(
        self,
    ) -> dict[type[models.Field], type[serializers.Field]]:
        """Extend serializer mapping with custom fields."""
        serializer_field_mapping = super().serializer_field_mapping  # type: ignore
        for (
            django_field,
            drf_field,
        ) in self.extract_serializer_field_mapping_from_settings().items():
            serializer_field_mapping[django_field] = drf_field
        return serializer_field_mapping

    def extract_serializer_field_mapping_from_settings(
        self,
    ) -> dict[type[models.Field], type[serializers.Field]]:
        """Extract field mapping from settings."""
        import_mapping = getattr(settings, "SARITASA_DRF_FIELD_MAPPING", {})
        return {
            import_string(django_field): import_string(drf_field)
            for django_field, drf_field in import_mapping.items()
        }
