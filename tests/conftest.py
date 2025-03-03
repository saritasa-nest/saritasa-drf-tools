import pytest
import pytest_django

from example.app import factories, models


@pytest.fixture(scope="session", autouse=True)
def django_db_setup(django_db_setup) -> None:  # noqa: ANN001
    """Set up test db for testing."""


@pytest.fixture(autouse=True)
def _enable_db_access_for_all_tests(django_db_setup, db) -> None:  # noqa: ANN001
    """Enable access to DB for all tests."""


@pytest.fixture(scope="module")
def user(
    django_db_blocker: pytest_django.DjangoDbBlocker,
) -> models.User:
    """Create user."""
    with django_db_blocker.unblock():
        return factories.UserFactory()  # type: ignore


@pytest.fixture(scope="module")
def admin(
    django_db_blocker: pytest_django.DjangoDbBlocker,
) -> models.User:
    """Create admin."""
    with django_db_blocker.unblock():
        return factories.AdminUserFactory()  # type: ignore
