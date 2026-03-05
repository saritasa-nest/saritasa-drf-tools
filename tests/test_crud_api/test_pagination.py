from django.test import override_settings
from rest_framework import test

from . import tester


class TestCRUD(tester.CRUDApiActionTester):
    """Define tests."""

    @override_settings(
        SARITASA_DRF_MAX_PAGINATION_SIZE=2,
    )
    def test_max_pagination_setting(
        self,
        user_api_client: test.APIClient,
    ) -> None:
        """Test that max pagination setting is working."""
        self.invoke_factory_batch(size=6)
        response = self.make_request(
            method="get",
            api_client=user_api_client,
            path=self.lazy_url(action="list"),
            data={
                "limit": 10000,
            },
        )
        assert (
            response.data["count"]
            == tester.CRUDApiActionTester.model.objects.count()  # type: ignore
        ), response.data
        assert len(response.data["results"]) == 2


class TestReadOnlyView(tester.ReadOnlyApiActionTester):
    """Define tests for read only view."""

    def test_max_pagination_setting_in_view(
        self,
        user_api_client: test.APIClient,
    ) -> None:
        """Test that max pagination setting in view is working."""
        self.invoke_factory_batch(size=6)
        response = self.make_request(
            method="get",
            api_client=user_api_client,
            path=self.lazy_url(action="list"),
            data={
                "limit": 10000,
            },
        )
        assert (
            response.data["count"] == self.model.objects.count()  # type: ignore
        ), response.data
        assert (
            len(response.data["results"]) == self.api_view.pagination_max_limit
        ), response.data

    def test_default_pagination_setting_in_view(
        self,
        user_api_client: test.APIClient,
    ) -> None:
        """Test that default pagination setting in view is working."""
        self.invoke_factory_batch(size=6)
        response = self.make_request(
            method="get",
            api_client=user_api_client,
            path=self.lazy_url(action="list"),
        )
        assert (
            response.data["count"] == self.model.objects.count()  # type: ignore
        ), response.data
        assert (
            len(response.data["results"])
            == self.api_view.pagination_default_limit
        ), response.data
