from django_filters import rest_framework

from .. import models


class TestModelFilter(rest_framework.FilterSet):
    """Filter class for `TestModel` model."""

    class Meta:
        model = models.TestModel
        fields = {  # noqa: RUF012
            "text_field": (
                "exact",
                "icontains",
            ),
            "related_model": (
                "exact",
                "in",
            ),
        }
