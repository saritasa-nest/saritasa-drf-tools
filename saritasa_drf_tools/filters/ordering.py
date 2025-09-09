import collections.abc
import typing
import warnings

from django.conf import settings
from django.core import exceptions
from django.db import models
from rest_framework import filters, request, views


class OrderingFilterBackend(filters.OrderingFilter):
    """Custom OrderingFilter with additional features.

    Provides:
    - Better support of openapi via drf-spectacular.
    - Extra kwargs for ordering fields.

    """

    def get_ordering(
        self,
        request: request.Request,
        queryset: models.QuerySet,
        view: views.APIView,
    ) -> collections.abc.Sequence[models.OrderBy]:
        """Adjust ordering params.

        Wrap ordering fields in `models.OrderBy` and pass extra ordering kwargs

        """
        ordering = (
            super().get_ordering(
                request,
                queryset,
                view,
            )
            or ()
        )
        is_null_first = getattr(
            settings,
            "SARITASA_DRF_ORDERING_IS_NULL_FIRST",
            None,
        )
        is_null_last = getattr(
            settings,
            "SARITASA_DRF_ORDERING_IS_NULL_LAST",
            None,
        )

        ordering_fields_extra_kwargs = getattr(
            view,
            "ordering_fields_extra_kwargs",
            {},
        )
        fields_from_extra_kwargs = set(ordering_fields_extra_kwargs.keys())
        cleared_ordering_fields = {
            field.removeprefix("-") for field in ordering
        }
        if (
            unknown_fields := fields_from_extra_kwargs
            - cleared_ordering_fields
        ):
            view_action = getattr(view, "action", "list")
            warnings.warn(
                f"Unknown ordering fields: {','.join(unknown_fields)}"
                f" defined(ordering_fields_extra_kwargs) in {self.__class__}"
                f"({view_action}).",
                stacklevel=2,
            )
        adjusted_ordering: list[models.OrderBy] = []
        for order_field in ordering:
            cleared_order_field = order_field.removeprefix("-")
            order_by_kwargs = {
                "descending": order_field.startswith("-"),
                "nulls_first": is_null_first,
                "nulls_last": is_null_last,
            }
            order_by_kwargs.update(
                ordering_fields_extra_kwargs.get(cleared_order_field, {}),
            )
            adjusted_ordering.append(
                models.OrderBy(
                    expression=models.F(cleared_order_field),
                    **order_by_kwargs,
                ),
            )

        return adjusted_ordering

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

            view_action = getattr(view, "action", "list")
            drainage.warn(
                "`ordering_fields` contains non-existent"
                f" or non-related fields for action {view_action}."
                f" {error}",
            )
