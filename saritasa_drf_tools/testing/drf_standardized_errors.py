import rest_framework.response
import rest_framework.status


class DRFStandardizedErrorsMixin:
    """Add support for drf_standardized_errors package."""

    def extract_errors_from_response(
        self,
        response: rest_framework.response.Response,
        field: str,
    ) -> list[str]:
        """Extract errors from response."""
        assert response.data  # noqa: S101
        assert "errors" in response.data, response.data  # noqa: S101
        field_errors = [
            error["detail"]
            for error in response.data["errors"]
            if error["attr"] == field
        ]
        assert field_errors, response.data  # noqa: S101
        return field_errors
