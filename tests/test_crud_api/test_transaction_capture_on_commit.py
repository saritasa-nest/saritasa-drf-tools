import pytest
from rest_framework import status, test

from . import tester


class TestCRUD(tester.CRUDApiActionTester):
    """Define tests."""

    @pytest.mark.parametrize(
        argnames="is_capture_on_commit_enabled",
        argvalues=[
            True,
            False,
        ],
    )
    def test_transaction_capture_on_commit(
        self,
        is_capture_on_commit_enabled: bool,
        admin: tester.CRUDApiActionTester.user_model,
        instance: tester.CRUDApiActionTester.model,
        api_client: test.APIClient,
    ) -> None:
        """Test that check transaction capture on commit works."""
        self.make_request(
            method="put",
            user=admin,
            expected_status=status.HTTP_200_OK,
            path=self.lazy_url(action="detail", pk=instance.pk),
            data=self.serialize_data(action="update", data=instance),
            api_client=api_client,
            capture_on_commit=is_capture_on_commit_enabled,
        )

        instance.refresh_from_db()
        if is_capture_on_commit_enabled:
            assert instance.text_field == f"Updated {instance.id}"
        else:
            assert instance.text_field != f"Updated {instance.id}"
