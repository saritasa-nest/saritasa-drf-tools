import pytest
from rest_framework import status, test

from . import tester


class TestCRUD(tester.CRUDApiActionTester):
    """Define tests."""

    @pytest.mark.parametrize(
        argnames=[
            "action",
            "method",
        ],
        argvalues=[
            [
                "create",
                "post",
            ],
            [
                "update",
                "put",
            ],
        ],
    )
    def test_clean_validation(
        self,
        instance: tester.CRUDApiActionTester.model,
        admin_api_client: test.APIClient,
        action: str,
        method: str,
    ) -> None:
        """Test that clean method of model will be called."""
        if action == "create":
            path = self.lazy_url(action="list")
        elif action == "update":
            path = self.lazy_url(action="detail", pk=instance.pk)

        self.make_request(
            method=method,
            api_client=admin_api_client,
            path=path,
            data=self.serialize_data(action=action, data=instance),
        )

    @pytest.mark.parametrize(
        argnames=[
            "action",
            "method",
        ],
        argvalues=[
            [
                "create",
                "post",
            ],
            [
                "update",
                "put",
            ],
        ],
    )
    def test_clean_validation_failed(
        self,
        instance: tester.CRUDApiActionTester.model,
        admin_api_client: test.APIClient,
        action: str,
        method: str,
    ) -> None:
        """Test that clean method of model will be called and return error."""
        if action == "create":
            path = self.lazy_url(action="list")
        elif action == "update":
            path = self.lazy_url(action="detail", pk=instance.pk)
        data = self.serialize_data(action=action, data=instance)
        data["text_field"] = "invalid"

        response = self.make_request(
            method=method,
            api_client=admin_api_client,
            expected_status=status.HTTP_400_BAD_REQUEST,
            path=path,
            data=data,
        )
        self.check_errors_from_response(
            response=response,
            field="non_field_errors",
            expected_errors=[
                "Text field is invalid",
            ],
        )


class TestDRFStandardizedErrorsCRUD(
    tester.DRFStandardizedErrorsCRUDApiActionTester,
):
    """Define tests."""

    @pytest.mark.parametrize(
        argnames=[
            "action",
            "method",
        ],
        argvalues=[
            [
                "create",
                "post",
            ],
            [
                "update",
                "put",
            ],
        ],
    )
    def test_clean_validation(
        self,
        instance: tester.CRUDApiActionTester.model,
        admin_api_client: test.APIClient,
        action: str,
        method: str,
    ) -> None:
        """Test that clean method of model will be called."""
        if action == "create":
            path = self.lazy_url(action="list")
        elif action == "update":
            path = self.lazy_url(action="detail", pk=instance.pk)
        data = self.serialize_data(action=action, data=instance)
        data["text_field"] = "invalid"

        response = self.make_request(
            method=method,
            api_client=admin_api_client,
            expected_status=status.HTTP_400_BAD_REQUEST,
            path=path,
            data=data,
        )
        self.check_errors_from_response(
            response=response,
            field="non_field_errors",
            expected_errors=[
                "Text field is invalid",
            ],
        )
