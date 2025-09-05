from rest_framework import serializers


class ActionSerializerMixin:
    """Mixin which allows to define specific serializers per action.

    It requires a filled ``serializers_map`` attribute
    It should be used for ``ModelViewSet``
    Examples:
        class NoteViewSet(ActionSerializerMixin, viewsets.ModelViewSet):
            queryset = Note.objects.all()
            serializer_class = NoteSerializer
            serializers_map = {
                "update": serializers.UpdateNoteSerializer,
                "partial_update": serializers.UpdateNoteSerializer,
            }

    """

    action: str
    serializers_map: dict[str, type[serializers.Serializer]] = {}

    def get_serializer_class(self) -> type[serializers.Serializer]:
        """Get serializer for view's action.

        First we try to find corresponding `action` in `serializer_map` and
        in case if current method is absent in `serializer_map` we return
        `default` from `serializer_map`(if default is not set we use
        serializer_class from `super().get_serializer_class()`).

        Example:
        -------
            serializer_map = {
                "update": serializers.UpdateLeadSerializer,
                "partial_update": serializers.UpdateLeadSerializer,
            }

        """
        default_serializer_class = self.serializers_map.get("default")
        action_serializer_class = self.serializers_map.get(
            self.action,
            default_serializer_class,
        )

        return action_serializer_class or super().get_serializer_class()  # type: ignore
