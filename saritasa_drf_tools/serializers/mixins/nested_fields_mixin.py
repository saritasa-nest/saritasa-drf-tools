from django.utils.module_loading import import_string
from rest_framework import serializers, utils


class NestedFieldsMixin:
    """Mixin which can set up nested fields for related fields.

    By adding `nested_fields` attribute to serializer's Meta class, you can
    set up serializer for a field. It will be added with suffix `_data`. It's
    simplifies definition of nested fields in serializers while making them
    more consistent with specs generation tools like drf-spectacular. Also it
    helps to avoid import cycles by allowing to use string notation for
    serializer classes.

    Example:
    class Meta:
        model = models.User
        fields = (
            "id",
            "created",
            "modified",
            "username",
            "email",
            "country",
            "supervisors",
        )
        # There two ways to define serializer class: directly or via string.
        nested_fields = {
            "country": CountrySerializer,
            "supervisors": "apps.users.api.serializers.SimpleUserSerializer",
        }

    Would result in serializer with the following fields: fields from meta plus
    `created_by_data` and `supervisors_data` as read_only fields. Read_only and
    other params could be customized via `extra_kwargs`(Note: you need to use
    generated names).

    """

    def get_fields(
        self,
    ) -> dict[str, serializers.Serializer | serializers.Field]:
        """Get fields."""
        return {
            **super().get_fields(),  # type: ignore
            **self.get_nested_fields(),
        }

    def get_nested_fields(self) -> dict[str, serializers.Serializer]:
        """Set up data fields."""
        meta = self.Meta  # type: ignore
        info = utils.model_meta.get_field_info(meta.model)  # type: ignore
        extra_kwargs = self.get_extra_kwargs()  # type: ignore
        meta_nested_fields = getattr(
            meta,
            "nested_fields",
            {},
        )
        nested_fields_suffix = getattr(meta, "nested_fields_suffix", "_data")
        nested_fields = {}
        for nested_field, nested_field_class in meta_nested_fields.items():
            field_name = f"{nested_field}{nested_fields_suffix}"
            extra_field_kwargs = extra_kwargs.get(field_name, {})
            _, field_kwargs = self.build_field(  # type: ignore
                field_name=nested_field,
                info=info,
                model_class=meta.model,
                nested_depth=0,
            )
            field_kwargs["read_only"] = True
            field_kwargs.pop("queryset", None)
            field_kwargs = self.include_extra_kwargs(  # type: ignore
                kwargs=field_kwargs,
                extra_kwargs=extra_field_kwargs,
            )
            if isinstance(nested_field_class, str):
                try:
                    nested_field_class = import_string(nested_field_class)
                except ImportError as import_error:
                    raise ValueError(
                        "Could not import field class "
                        f"'{nested_field_class}' for {self.__class__}",
                    ) from import_error
            nested_fields[field_name] = nested_field_class(
                source=nested_field,
                **field_kwargs,
            )
        return nested_fields
