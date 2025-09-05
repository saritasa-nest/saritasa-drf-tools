import uuid

import factory

from . import models

DEFAULT_PASSWORD = "Test111!"  # noqa: S105


class UserFactory(factory.django.DjangoModelFactory[models.User]):
    """Factory to generate test User instance."""

    email = factory.declarations.LazyAttribute(
        lambda obj: f"{uuid.uuid4()}@saritasa-s3-tools.com",
    )
    username = factory.faker.Faker("user_name")
    first_name = factory.faker.Faker("first_name")
    last_name = factory.faker.Faker("last_name")
    password = factory.django.Password(password=DEFAULT_PASSWORD)

    class Meta:  # type: ignore
        model = models.User


class AdminUserFactory(UserFactory):
    """Factory to generate test User model with admin privileges."""

    is_superuser = True
    is_staff = True


class TestModelFactory(factory.django.DjangoModelFactory[models.TestModel]):
    """Factory to generate test TestModel instance."""

    int_field = factory.faker.Faker("pyint")

    class Meta:  # type: ignore
        model = models.TestModel
