from rest_framework import test

from . import tester


class TestCRUD(tester.CRUDApiActionTester):
    """Define tests."""

    def test_ordering_with_none(
        self,
        user_api_client: test.APIClient,
    ) -> None:
        """Test that with extra configuration we can make null appear first."""
        self.invoke_factory_batch(size=2)
        instance_with_none = self.invoke_factory(int_field=None)
        response = self.make_request(
            method="get",
            api_client=user_api_client,
            path=self.lazy_url(action="list"),
            data={
                "ordering": "-int_field",
            },
        )
        assert len(response.data["results"]) == 3
        assert response.data["results"][0]["id"] == instance_with_none.pk
