from rest_framework import renderers
from rest_framework.request import override_method


class BrowsableAPIRenderer(renderers.BrowsableAPIRenderer):
    """Customization over drf's BrowsableAPIRenderer.

    Custom renderer to remove all extra forms which results in extra queries.

    """

    def get_rendered_html_form(  # type: ignore
        self,
        data,  # noqa: ANN001
        view,  # noqa: ANN001
        method,  # noqa: ANN001
        request,  # noqa: ANN001
    ) -> bool | None:
        """Show forms just for `DELETE` and `OPTIONS` method.

        We have a lot of custom serializers fields, which does not support well
        form inputs, so we do not show any html forms.

        """
        with override_method(view, request, method) as overridden_request:
            if not self.show_form_for_method(
                view=view,
                method=method,
                request=overridden_request,
                obj=None,
            ):
                return None

            if method in ("DELETE", "OPTIONS"):
                return True  # Don't actually need to return a form
        return None
