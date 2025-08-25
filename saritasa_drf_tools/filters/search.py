import collections.abc
import typing

from django.core import exceptions
from rest_framework import filters, views


class SearchFilterBackend(filters.SearchFilter):
    """Custom SearchFilter for better support of openapi."""

    def get_schema_operation_parameters(
        self,
        view: views.APIView,
    ) -> list[dict[str, typing.Any]]:
        """Prepare parameters for openapi schema.

        Check that view has `search_fields`.

        Check that `search_fields` contains valid set of fields. Actually,
        this check may perform some SQL queries during spec generation. Also,
        spec generation is not the best place for checking of source code
        (comparing to linters/django system checks/tests), but DRF doesn't
        validate `search_fields` for views while backend running.

        Extend view description with list of `search_fields`.

        """
        operation_parameters = super().get_schema_operation_parameters(
            view=view,
        )
        # Not using get_search_fields since it is requires additional params
        search_fields: collections.abc.Sequence[str] | None = getattr(
            view,
            "search_fields",
            None,
        )
        if not search_fields:  # pragma: no cover
            from drf_spectacular import drainage

            drainage.warn(
                f"`search_fields` are not set up for {view.__class__}",
            )
            return operation_parameters

        self._validate_search_fields(view)

        formatted_fields = ", ".join(f"`{field}`" for field in search_fields)
        operation_parameters[0]["description"] = (
            f"A search term.\n\nPerformed on this fields: {formatted_fields}."
        )
        return operation_parameters

    def _validate_search_fields(
        self,
        view: views.APIView,
    ) -> None:
        """Validate `search_fields` in view."""
        queryset = view.get_queryset()  # type: ignore
        try:
            search_dict = {}
            for search_field in view.search_fields:  # type: ignore
                search_arg = self.construct_search(
                    str(search_field),
                    queryset=queryset,
                )
                search_dict[search_arg] = "test"
            queryset.filter(**search_dict)
        except exceptions.FieldError as error:  # pragma: no cover
            from drf_spectacular import drainage

            view_action = getattr(view, "action", "list")
            drainage.warn(
                "`search_fields` contains non-existent or"
                f" non-related fields for action {view_action}."
                f" {error}",
            )
