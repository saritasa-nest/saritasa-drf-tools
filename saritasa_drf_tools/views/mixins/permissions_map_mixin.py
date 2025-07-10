import collections.abc
import typing

from django.core import exceptions
from rest_framework import permissions

type PermissionType = (
    type[permissions.BasePermission] | permissions.OperandHolder
)
type PermissionsTypesSequence = collections.abc.Sequence[PermissionType]


class ActionPermissionsMixin:
    """Mixin which allows to define specific permissions per actions.

    Attributes
    ----------
        `base_permission_classes` - Base permissions which are supposed to be
            defined in base class and typically should not be overridden.
            If define `base_permission_classes` without any extra permissions
            (`extra_permission_classes`, `extra_permissions_map`) then it acts
            exactly like `permission_classes` from drf.
        `extra_permission_classes` - Extra permissions which are supposed to
            be overridden if needed. This attribute allows to set extra
            permissions in child classes.
        `extra_permissions_map` - Mapping which allows to set specific
            permissions per action. If permissions for the action were found in
            `extra_permissions_map` then will be returned permissions from
            `base_permission_classes` + specific permission for the action from
            this map.
            If permissions for the action were not found in this map then
            `base_permission_classes` with `extra_permission_classes` will be
            used the same way it would work as if `extra_permissions_map` was
            not provided at all.

    It can be used both ways:

    1) With providing `base_permission_classes` + `extra_permission_classes`:
    ```
    class BaseViewSet(ActionPermissionsMixin, viewsets.ModelViewSet):
        base_permission_classes = (
            IsAuthenticated,
        )


    class DogViewSet(BaseViewset):
        # In order to access this viewset user should have `IsAuthenticated`
        # permission from base viewset and `CanSayWoof` permission
        # from this viewset
        extra_permission_classes = (
            CanSayWoof,
        )
    ```

    2) With providing `extra_permissions_map`:
    ```
    class DogViewSet(BaseViewset):
        # In order to get access to these actions user should also have
        # `IsAuthenticated` permission from
        # `BaseViewset.base_permission_classes`
        extra_permissions_map = {
            "bark": (
                CanSayWoof,
            ),
            # Only permissions from `base_permission_classes` will be used for
            # this action
            "sit": (),
        }
        # For all actions which were not found in `extra_permissions_map`
        # will be used permissions from `base_permission_classes` +
        # `extra_permission_classes`
        extra_permission_classes = (
            CanEatBones,
        )
    ```

    """

    action: str

    base_permission_classes: PermissionsTypesSequence = (
        permissions.IsAdminUser,
    )

    extra_permission_classes: PermissionsTypesSequence = ()

    extra_permissions_map: dict[str, PermissionsTypesSequence]

    # `permission_classes` is not supported so declaring as final to provide
    # warnings on adding this attribute to classes
    permission_classes: typing.Final = None

    def get_permissions(self) -> list[permissions.BasePermission]:
        """Return permissions list for current `.action` attribute value.

        It returns permission from `base_permission_classes` +
        permissions list from `extra_permissions_map` using view's action as
        key.
        If view doesn't have `extra_permissions_map` just return
        `base_permission_classes` + `extra_permission_classes`

        Returns
        -------
            All permissions for the action

        """
        if getattr(self, "permission_classes", None) is not None:
            raise exceptions.ImproperlyConfigured(
                "`permission_classes` is not supported.\n"
                "Use `base_permission_classes` + `extra_permission_classes` "
                "or `base_permission_classes` + `extra_permissions_map` "
                "instead.\n"
                "Check `ActionPermissionsMixin` docs for additional "
                "information",
            )

        action = getattr(self, "action", None)
        action_extra_permission_classes = (
            self.get_action_extra_permission_classes(action=action)
        )

        return self.get_unique_permissions(
            permissions=(
                *self.base_permission_classes,
                *action_extra_permission_classes,
            ),
        )

    def get_action_extra_permission_classes(
        self,
        action: str | None,
    ) -> PermissionsTypesSequence:
        """Return extra permissions for the action.

        If the action is provided in `extra_permissions_map` then return
        permissions for this action, otherwise return just all permissions from
        `extra_permission_classes`.

        """
        extra_permissions_map = getattr(self, "extra_permissions_map", {})
        return extra_permissions_map.get(action, self.extra_permission_classes)

    def get_unique_permissions(
        self,
        permissions: PermissionsTypesSequence,
    ) -> list[permissions.BasePermission]:
        """Return tuple of unique permissions with keeping original order.

        TODO: use `dict.fromkeys()` when
        https://github.com/encode/django-rest-framework/pull/9417
        will be merged

        """
        unique_permissions = []

        for permission in permissions:
            if permission not in unique_permissions:
                unique_permissions.append(permission)

        return [permission() for permission in unique_permissions]
