import pytest
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

    @pytest.mark.parametrize(
        argnames="ordering",
        argvalues=[
            pytest.param(
                "text_field",
                id="with_ordering_by_non_unique_field",
            ),
            pytest.param(
                None,
                id="without_ordering",
            ),
        ],
    )
    def test_ordering_with_pk_added(
        self,
        ordering: str | None,
        user_api_client: test.APIClient,
    ) -> None:
        """Test ordering with pk added logic.

        When sorting by non-unique fields only (or without any ordering)
        with `add_pk_to_ordering` enabled in the view, same results
        should be returned on every request.

        """
        self.invoke_factory_batch(text_field="Text", size=5)
        request_params = {
            "method": "get",
            "api_client": user_api_client,
            "path": self.lazy_url(action="list"),
        }
        if ordering:
            request_params["data"] = {"ordering": ordering}
        first_response = self.make_request(**request_params)
        assert len(first_response.data["results"]) == 5
        second_response = self.make_request(**request_params)
        assert len(second_response.data["results"]) == 5
        assert (
            first_response.data["results"] == second_response.data["results"]
        )
