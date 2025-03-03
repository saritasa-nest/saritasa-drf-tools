import pytest
import pytest_lazy_fixtures
from django.core.exceptions import ImproperlyConfigured
from rest_framework import permissions, status, test

import saritasa_drf_tools.views

from . import tester


class TestCRUD(tester.CRUDApiActionTester):
    """Define tests."""

    @pytest.mark.parametrize(
        argnames=[
            "parametrize_user",
            "status_code",
        ],
        argvalues=[
            [
                None,
                status.HTTP_403_FORBIDDEN,
            ],
            [
                pytest_lazy_fixtures.lf("user"),
                status.HTTP_403_FORBIDDEN,
            ],
            [
                pytest_lazy_fixtures.lf("admin"),
                status.HTTP_201_CREATED,
            ],
        ],
    )
    def test_permission_map_specified_action_create(
        self,
        instance: tester.CRUDApiActionTester.model,
        parametrize_user: tester.CRUDApiActionTester.user_model | None,
        status_code: int,
    ) -> None:
        """Test that create action will properly handle permissions."""
        self.make_request(
            method="post",
            user=parametrize_user,
            expected_status=status_code,
            path=self.lazy_url(action="list"),
            data=self.serialize_data(action="create", data=instance),
        )

    @pytest.mark.parametrize(
        argnames=[
            "parametrize_user",
            "status_code",
        ],
        argvalues=[
            [
                None,
                status.HTTP_403_FORBIDDEN,
            ],
            [
                pytest_lazy_fixtures.lf("user"),
                status.HTTP_403_FORBIDDEN,
            ],
            [
                pytest_lazy_fixtures.lf("admin"),
                status.HTTP_200_OK,
            ],
        ],
    )
    def test_permission_map_specified_action_update(
        self,
        instance: tester.CRUDApiActionTester.model,
        parametrize_user: tester.CRUDApiActionTester.user_model | None,
        status_code: int,
    ) -> None:
        """Test that update action will properly handle permissions."""
        self.make_request(
            method="put",
            user=parametrize_user,
            expected_status=status_code,
            path=self.lazy_url(action="detail", pk=instance.pk),
            data=self.serialize_data(action="update", data=instance),
        )

    @pytest.mark.parametrize(
        argnames=[
            "parametrize_user",
            "status_code",
        ],
        argvalues=[
            [
                None,
                status.HTTP_403_FORBIDDEN,
            ],
            [
                pytest_lazy_fixtures.lf("user"),
                status.HTTP_403_FORBIDDEN,
            ],
            [
                pytest_lazy_fixtures.lf("admin"),
                status.HTTP_204_NO_CONTENT,
            ],
        ],
    )
    def test_permission_map_specified_action_delete(
        self,
        instance: tester.CRUDApiActionTester.model,
        parametrize_user: tester.CRUDApiActionTester.user_model | None,
        status_code: int,
    ) -> None:
        """Test that delete action will properly handle permissions."""
        self.make_request(
            method="delete",
            user=parametrize_user,
            expected_status=status_code,
            path=self.lazy_url(action="detail", pk=instance.pk),
        )

    @pytest.mark.parametrize(
        argnames=[
            "parametrize_user",
            "status_code",
        ],
        argvalues=[
            [
                None,
                status.HTTP_403_FORBIDDEN,
            ],
            [
                pytest_lazy_fixtures.lf("user"),
                status.HTTP_200_OK,
            ],
            [
                pytest_lazy_fixtures.lf("admin"),
                status.HTTP_200_OK,
            ],
        ],
    )
    def test_permission_map_default_action(
        self,
        parametrize_user: tester.CRUDApiActionTester.user_model | None,
        api_client: test.APIClient,
        status_code: int,
    ) -> None:
        """Test that detail action will properly handle default permissions."""
        self.make_request(
            method="get",
            user=parametrize_user,
            expected_status=status_code,
            path=self.lazy_url(action="detail", pk=self.invoke_factory().pk),
        )

    def test_permission_map_permission_classes(self) -> None:
        """Test invalid configuration.

        Test that mixin will raise an error if permission classes are used.

        """

        class InvalidView(saritasa_drf_tools.views.CRUDViewSet):
            permission_classes = (permissions.AllowAny,)  # type: ignore

        with pytest.raises(ImproperlyConfigured):
            InvalidView(action="list").get_permissions()
