from rest_framework import mixins


class UpdateModelWithoutPatchMixin:
    """Same as UpdateModelMixin but without patch method.

    Disables `PATCH` methods. Frontend usually doesn't use it, we write
    serializers expecting to have all data we need to do the thing.
    But `PATCH` allows bypassing `required` restriction.

    """

    update = mixins.UpdateModelMixin.update
    perform_update = mixins.UpdateModelMixin.perform_update
