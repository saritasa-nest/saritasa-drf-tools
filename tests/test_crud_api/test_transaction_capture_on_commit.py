from rest_framework import status, test

from . import tester


class TestCRUD(tester.CRUDApiActionTester):
    """Define tests."""

    def test_transaction_capture_on_commit(
        self,
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
        )
        instance.refresh_from_db()
        assert instance.text_field == f"Updated {instance.id}"
