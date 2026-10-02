from django.contrib.auth.models import AbstractBaseUser
from rest_framework import request


class UserAndRequestFromContextMixin[User: AbstractBaseUser]:
    """Extracts user and request from context and sets it as attr ."""

    def __init__(
        self,
        *args,  # noqa: ANN002
        **kwargs,
    ) -> None:
        """Set current user."""
        super().__init__(*args, **kwargs)
        self._request: request.Request | None = self.context.get("request")  # type: ignore
        self._user: User | None = getattr(self._request, "user", None)
