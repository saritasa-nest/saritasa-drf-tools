import collections.abc
import typing

from django.core import exceptions
from rest_framework import filters, views


class OrderingFilterBackend(filters.OrderingFilter):
    """Custom OrderingFilter for better support of openapi."""

    def get_schema_operation_parameters(
        self,
        view: views.APIView,
    ) -> list[dict[str, typing.Any]]:
        """Prepare parameters for openapi schema.

        Check that view has `ordering_fields`.

        Check that `ordering_fields` contains valid set of fields. Actually,
        this check may perform some SQL queries during spec generation. Also,
        spec generation is not the best place for checking of source code
        (comparing to linters/django system checks/tests), but DRF doesn't
        validate `ordering_fields` for views while backend running.

        Extend view description with list of `ordering_fields`.

        """
        operation_parameters = super().get_schema_operation_parameters(
            view=view,
        )
        # Not using get_valid_fields since it is requires additional params
        ordering_fields: collections.abc.Sequence[str] | None = getattr(
            view,
            "ordering_fields",
            None,
        )
        if not ordering_fields:  # pragma: no cover
            from drf_spectacular import drainage

            drainage.warn(
                f"`ordering_fields` are not set up for {view.__class__}",
            )
            return operation_parameters

        self._validate_ordering_fields(view)

        formatted_fields = ", ".join(f"`{field}`" for field in ordering_fields)
        operation_parameters[0]["description"] = (
            "Which fields to use when ordering the results. A list "
            "fields separated by `,`. Example: `field1,field2`\n\n"
            f"Supported fields: {formatted_fields}.\n\n"
            "To reverse order just add `-` to field. Example:"
            "`field` -> `-field`"
        )
        return operation_parameters

    def _validate_ordering_fields(
        self,
        view: views.APIView,
    ) -> None:
        """Validate `ordering_fields` in view."""
        try:
            view.get_queryset().order_by(*view.ordering_fields)  # type: ignore
        except exceptions.FieldError as error:  # pragma: no cover
            from drf_spectacular import drainage

            drainage.warn(
                "`ordering_fields` contains non-existent"
                " or non-related fields."
                f" {error}",
            )
