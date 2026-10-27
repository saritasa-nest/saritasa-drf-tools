from django.contrib.auth import models as auth_models
from rest_framework import serializers

from . import mixins


class BaseSerializer[User: auth_models.AbstractBaseUser](
    mixins.UserAndRequestFromContextMixin[User],
    serializers.Serializer,
):
    """Serializer with common logic."""
