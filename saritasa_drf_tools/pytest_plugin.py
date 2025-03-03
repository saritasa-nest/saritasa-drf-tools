import typing

import pytest


@pytest.fixture
def api_client_factory():  # noqa: ANN201
    """Create factory which will generate api clients."""
    from rest_framework import test

    def _create_api_client() -> test.APIClient:
        return test.APIClient()

    return _create_api_client


@pytest.fixture
def api_client(api_client_factory):  # noqa: ANN001, ANN201
    """Create api client."""
    return api_client_factory()


@pytest.fixture
def user() -> typing.Any:
    """Get ordinary user."""
    raise NotImplementedError("Set up `user` fixture")


@pytest.fixture
def user_api_client(  # noqa: ANN201
    api_client_factory,  # noqa: ANN001
    user,  # noqa: ANN001
):
    """Create api client."""
    api_client = api_client_factory()
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin() -> typing.Any:
    """Get admin user."""
    raise NotImplementedError("Set up `admin` fixture")


@pytest.fixture
def admin_api_client(  # noqa: ANN201
    api_client_factory,  # noqa: ANN001
    admin,  # noqa: ANN001
):
    """Create api client."""
    api_client = api_client_factory()
    api_client.force_authenticate(user=admin)
    return api_client
