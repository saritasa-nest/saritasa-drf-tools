from rest_framework import serializers


class CustomCharField(serializers.CharField):
    """A custom serializer field simply for testing purposes."""
