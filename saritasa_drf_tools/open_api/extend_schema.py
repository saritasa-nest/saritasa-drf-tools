from drf_spectacular.extensions import OpenApiViewExtension
from rest_framework.views import APIView


class ApiViewFix(OpenApiViewExtension):
    """Fixes warning `This is graceful fallback handling for APIViews`."""

    def view_replacement(self):  # noqa: ANN201
        """Generate replacement."""

        class Fixed(self.target_class):  # type: ignore
            """Add needed properties."""

            serializer_class = None
            queryset = None

        return Fixed


def fix_api_view_warning(class_to_fix: type[APIView]):  # noqa: ANN201
    """Fix warning `This is graceful fallback handling for APIViews`."""

    class FixedApiView(ApiViewFix):
        """Generated fixed class."""

        target_class = f"{class_to_fix.__module__}.{class_to_fix.__name__}"

    return FixedApiView
