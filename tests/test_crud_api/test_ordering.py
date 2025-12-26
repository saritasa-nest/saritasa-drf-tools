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

    def test_ordering_with_pk_added(
        self,
        user_api_client: test.APIClient,
    ) -> None:
        """Test ordering with pk added logic.

        If we sort by non-unique fields only and we use `add_pk_to_ordering`,
        in our view, we should get similar results on every request.

        """
        self.invoke_factory_batch(text_field="Text", size=5)
        request_params = {
            "method": "get",
            "api_client": user_api_client,
            "path": self.lazy_url(action="list"),
            "data": {
                "ordering": "text_field",
            },
        }
        first_response = self.make_request(**request_params)
        assert len(first_response.data["results"]) == 5
        second_response = self.make_request(**request_params)
        assert len(second_response.data["results"]) == 5
        assert (
            first_response.data["results"] == second_response.data["results"]
        )
