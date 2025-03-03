import saritasa_drf_tools.testing
from example.app import api, factories, models


class CRUDApiActionTester(
    saritasa_drf_tools.testing.ApiActionTester.init_subclass(
        model=models.TestModel,
        user_model=models.User,
        factory=factories.TestModelFactory,
        api_view=api.views.CRUDView,
        url_basename="crud-api",
    ),
):
    """Tester for crud API."""


class DRFStandardizedErrorsCRUDApiActionTester(
    saritasa_drf_tools.testing.ApiActionTester.init_subclass(
        model=models.TestModel,
        user_model=models.User,
        factory=factories.TestModelFactory,
        api_view=api.views.DRFStandardizedErrorsCRUDView,
        url_basename="drf-standardized-errors-crud-api",
        mixins=(saritasa_drf_tools.testing.DRFStandardizedErrorsMixin,),
    ),
):
    """Tester for drf standardized errors."""


class ReadOnlyApiActionTester(
    saritasa_drf_tools.testing.ApiActionTester.init_subclass(
        model=models.TestModel,
        user_model=models.User,
        factory=factories.TestModelFactory,
        api_view=api.views.ReadOnlyView,
        url_basename="read-only-api",
    ),
):
    """Tester for read only view."""
