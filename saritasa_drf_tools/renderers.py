from django.conf import settings
from rest_framework import renderers
from rest_framework.request import override_method


class BrowsableAPIRenderer(renderers.BrowsableAPIRenderer):
    """Customization over drf's BrowsableAPIRenderer.

    Custom renderer to remove all extra forms which results in extra queries
    if needed.

    """

    def get_rendered_html_form(  # type: ignore
        self,
        data,  # noqa: ANN001
        view,  # noqa: ANN001
        method,  # noqa: ANN001
        request,  # noqa: ANN001
    ) -> str | bool | None:
        """Customize `get_rendered_html_form` logic.

        Depending on settings show forms just for `DELETE` and `OPTIONS`
        method. Useful if you have a lot of custom serializers fields,
        which does not support well form inputs. Also lowers sql queries count.

        """
        enable_rendered_html_form_setting = getattr(
            settings,
            "SARITASA_DRF_BROWSABLE_API_ENABLE_HTML_FORM",
            True,
        )
        if getattr(
            view,
            "enable_browsable_api_rendered_html_form",
            enable_rendered_html_form_setting,
        ):
            return super().get_rendered_html_form(
                data=data,
                view=view,
                method=method,
                request=request,
            )
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
