from django.contrib.auth.models import AbstractUser
from django.core import exceptions
from django.db import models


class User(AbstractUser):
    """User model."""


class TestModel(models.Model):
    """Test model."""

    int_field = models.IntegerField(
        null=True,
    )

    text_field = models.TextField(
        default="",
        blank=True,
    )

    related_model = models.ForeignKey(
        null=True,
        to="app.TestRelatedModel",
        on_delete=models.CASCADE,
        related_name="test_models",
    )

    def __str__(self) -> str:
        """Return string representation."""
        return f"{self.pk}"

    def clean(self) -> None:
        """Verify text_field."""
        if self.text_field == "invalid":
            raise exceptions.ValidationError("Text field is invalid")


class TestRelatedModel(models.Model):
    """Test model."""

    text_field = models.TextField(
        default="",
        blank=True,
    )

    def __str__(self) -> str:
        """Return string representation."""
        return f"{self.pk}"
