from django.utils.module_loading import import_string
from rest_framework import serializers, utils


class DataFieldsMixin:
    """Mixin which can set up data fields for related fields.

    By adding `data_fields` attribute to serializer's Meta class, you can
    set up serializer for a field. It will be added with suffix `_data`.

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
        data_fields = {
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
            **self.get_data_fields(),
        }

    def get_data_fields(self) -> dict[str, serializers.Serializer]:
        """Set up data fields."""
        meta = self.Meta  # type: ignore
        info = utils.model_meta.get_field_info(meta.model)  # type: ignore
        extra_kwargs = self.get_extra_kwargs()  # type: ignore
        meta_data_fields = getattr(
            meta,
            "data_fields",
            {},
        )
        data_fields_suffix = getattr(meta, "data_fields_suffix", "_data")
        data_fields = {}
        for data_field, data_field_class in meta_data_fields.items():
            field_name = f"{data_field}{data_fields_suffix}"
            extra_field_kwargs = extra_kwargs.get(field_name, {})
            _, field_kwargs = self.build_field(  # type: ignore
                field_name=data_field,
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
            if isinstance(data_field_class, str):
                data_field_class = import_string(data_field_class)
            data_fields[field_name] = data_field_class(
                source=data_field,
                **field_kwargs,
            )
        return data_fields
