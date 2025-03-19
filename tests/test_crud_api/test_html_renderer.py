from django.test import override_settings
from rest_framework import test

from . import tester


class TestCRUD(tester.CRUDApiActionTester):
    """Define tests."""

    def test_html_renderer(
        self,
        instance_batch: list[tester.CRUDApiActionTester.model],
        admin_api_client: test.APIClient,
    ) -> None:
        """Test that renderer working."""
        self.make_request(
            method="get",
            api_client=admin_api_client,
            path=self.lazy_url(action="list"),
            headers={"accept": "text/html"},
        )

    @override_settings(
        SARITASA_DRF_BROWSABLE_API_ENABLE_HTML_FORM=False,
    )
    def test_html_renderer_disable_forms(
        self,
        instance_batch: list[tester.CRUDApiActionTester.model],
        admin_api_client: test.APIClient,
    ) -> None:
        """Test that renderer working with disable forms."""
        self.make_request(
            method="get",
            api_client=admin_api_client,
            path=self.lazy_url(action="list"),
            headers={"accept": "text/html"},
        )


class TestReadOnly(tester.ReadOnlyApiActionTester):
    """Define tests."""

    def test_html_renderer_no_filterset_class(
        self,
        instance_batch: list[tester.ReadOnlyApiActionTester.model],
        admin_api_client: test.APIClient,
    ) -> None:
        """Test that renderer working with no filterset class."""
        self.make_request(
            method="get",
            api_client=admin_api_client,
            path=self.lazy_url(action="list"),
            headers={"accept": "text/html"},
        )
