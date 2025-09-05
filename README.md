# saritasa-drf-tools

![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/saritasa-nest/saritasa-drf-tools/checks.yaml)
[![PyPI](https://img.shields.io/pypi/v/saritasa-drf-tools)](https://pypi.org/project/saritasa-drf-tools/)
![PyPI - Status](https://img.shields.io/pypi/status/saritasa-drf-tools)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/saritasa-drf-tools)
![PyPI - Django Version](https://img.shields.io/pypi/frameworkversions/django/saritasa-drf-tools)
![PyPI - License](https://img.shields.io/pypi/l/saritasa-drf-tools)
![PyPI - Downloads](https://img.shields.io/pypi/dm/saritasa-drf-tools)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Tools For [DRF](https://www.django-rest-framework.org/) Used By Saritasa

## Table of contents

* [Installation](#installation)
* [Features](#features)
* [Optional dependencies](#optional-dependencies)
* [Serializers](#serializers)
* [Views](#views)
* [Pagination](#pagination)
* [Filters](#filters)
* [Renderers](#renderers)
* [OpenAPI](#openapi)
* [Tester](#tester)

## Installation

```bash
pip install saritasa-drf-tools
```

or if you are using [uv](https://docs.astral.sh/uv/)

```bash
uv add saritasa-drf-tools
```

or if you are using [poetry](https://python-poetry.org/)

```bash
poetry add saritasa-drf-tools
```

## Features

* Views - collection of mixins and viewsets classes
* Serializers - collection of mixins and serializers classes
* Filters - Custom filter backends that improve integration with
  [drf-spectacular](https://github.com/tfranzel/drf-spectacular)
* OpenAPI - tools for [drf-spectacular](https://github.com/tfranzel/drf-spectacular)
* `pytest` - plugin which provides different `api_client` fixtures.
* Testing classes(**Warning: Very experimental**) - Test class which contains shortcut to reduce boilerplate across tests.

For examples and to just check it out in action you can use [example folder](/example).

## Optional dependencies

* `[filters]` - Add this to enable `django-filters` support
* `[openapi]` - Add this to enable `drf-spectacular` support

## Views

### Views mixins

* `ActionPermissionsMixin`: Mixin which allows to define specific permissions per actions
  For example you have:

  ```python
  class CRUDView(
    ActionPermissionsMixin,
    ActionMixins, # Anything you need
    GenericViewSet,
  ):
    """CRUD view."""
    base_permission_classes = (permissions.AllowAny,)
    extra_permission_classes = (permissions.IsAuthenticated,)
    extra_permissions_map = {
        "create": (permissions.IsAdminUser,),
        "update": (permissions.IsAdminUser,),
        "destroy": (permissions.IsAdminUser,),
    }
  ```

  * `base_permission_classes` - Will be applied to any action (Usually you want this in base class of your project)
  * `extra_permission_classes` - Will be added to `base_permission_classes`
  * `extra_permission_map` - Will be added to (`base_permission_classes` + `extra_permission_classes`) on
    action you specify in mapping

  To learn more read class docs.

* `ActionSerializerMixin`: Mixin which allows to define specific serializers per action.
  For example you have

  ```python
  class CRUDView(
    ActionPermissionsMixin,
    ActionMixins, # Anything you need
    GenericViewSet,
  ):
    """CRUD view."""

    queryset = models.TestModel.objects.select_related("related_model").all()
    serializers_map = {
        "default": serializers.TestModelDetailSerializer,
        "list": serializers.TestModelListSerializer,
    }
  ```

  That means that on `list` view will use `TestModelListSerializer`, but on any other
  actions `TestModelDetailSerializer`. This will also will be reflected in
  generated openapi specs via [drf-spectacular](https://github.com/tfranzel/drf-spectacular)

  To learn more read class docs.

* `UpdateModelWithoutPatchMixin`: Same as UpdateModelMixin but without patch method

### Viewset classes

* `BaseViewSet`: Viewset with `ActionPermissionsMixin` and `ActionSerializerMixin`
* `CRUDViewSet`: Viewset with crud endpoint based on BaseViewSet
* `ReadOnlyViewSet`: Viewset with read endpoint based on BaseViewSet

## Pagination

* `LimitOffsetPagination`: Customized paginator class to limit max objects in list APIs.
  Use `SARITASA_DRF_MAX_PAGINATION_SIZE` to set default max for whole project.

## Serializers

### Serializers mixins

* `CleanValidationMixin`: Enable model `clean` validation in serializer
* `FieldMappingOverride`: Override or extend field mapping via `SARITASA_DRF_FIELD_MAPPING`.
  For example you can set following in settings.

  ```python
  SARITASA_DRF_FIELD_MAPPING = {
    "django.db.models.TextField": "example.app.api.fields.CustomCharField",
  }
  ```

  And now all `TextField` of your models will have `CustomCharField` in
  serializers.

* `UserAndRequestFromContextMixin`: Extracts user and request from context
  and sets it as attr of serializer instance.
* `NestedFieldsMixin`: Allows to define nested data fields for serializers via `Meta` class.

### Serializers classes

* `BaseSerializer`: Serializer with `UserAndRequestFromContextMixin`
* `ModelBaseSerializer`: ModelSerializer with `mixins.FieldMappingOverride`,
  `mixins.CleanValidationMixin`, `mixins.UserAndRequestFromContextMixin`,
  `mixins.NestedFieldsMixin`.

## Filters

Needs `filters` and `openapi` to be included to work properly.

* `OrderingFilterBackend`: Add supported fields to `ordering` param's description
  in specs generated by [drf-spectacular](https://github.com/tfranzel/drf-spectacular). Will raise warning specs validation
  on empty `ordering_fields` or if queryset is unable to order itself using `ordering_fields`.
  Example of description:

  ```text
  Which fields to use when ordering the results. A list fields separated by ,. Example: field1,field2

  Supported fields: id, text_field, related_model__text_field.

  To reverse order just add - to field. Example:field -> -field
  ```

  Also has support for `nulls_first` and `nulls_last` ordering.
  You can either set these options globally in your settings:

  ```python
  SARITASA_DRF_ORDERING_IS_NULL_FIRST = True
  SARITASA_DRF_ORDERING_IS_NULL_LAST = True
  ```

  Or you can set them per view:

  ```python
  class MyView(views.APIView):
      ordering_fields_extra_kwargs = {
          "my_field": {
              "nulls_first": True,
              "nulls_last": False,
          },
      }
  ```

* `SearchFilterBackend`: Add supported fields to `search` param's description
  in specs generated by [drf-spectacular](https://github.com/tfranzel/drf-spectacular). Will raise warning specs validation
  on empty `search_fields` or if queryset is unable to perform search using `search_fields`.

  Example of description:

  ```text
  A search term.

  Performed on this fields: text_field, related_model__text_field.
  ```

* `DjangoFilterBackend`: Customized `DjangoFilterBackend` to reduce queries count when viewing api requests via browser

## Renderers

* `BrowsableAPIRenderer`: Customization over drf's BrowsableAPIRenderer.
  With `SARITASA_DRF_BROWSABLE_API_ENABLE_HTML_FORM`(Default: `True`) or
  setting `enable_browsable_api_rendered_html_form`(If not present will use global setting)
  in view you can disable all extra forms which results in extra SQL queries.

## OpenAPI

Needs `openapi` to be included to work properly.

* `OpenApiSerializer`: Serializer that should be used for customizing open_api spec.
  Made to avoid warnings about unimplemented methods.
* `DetailSerializer`: To show in spec responses like this `{detail: text}`.
* `fix_api_view_warning`: Fix warning `This is graceful fallback handling for APIViews`.

## Pytest

Plugin provides following fixtures:

* `api_client_factory` - factory which generated `rest_framework.test.ApiClient` instance
* `api_client` - uses `api_client_factory` to generate `rest_framework.test.ApiClient` instance
* `user_api_client`(Needs `user` fixture) uses `api_client_factory` to generate `rest_framework.test.ApiClient` instance
  forces auth to `user`
* `admin_api_client`(Needs `admin` fixture) uses `api_client_factory` to generate `rest_framework.test.ApiClient` instance
  forces auth to `admin`

## Tester

**Warning**: Very experimental.

`saritasa_drf_tools.testing.ApiActionTester` - is a tester class which contains
fixtures and shortcuts to simply and reduce boilerplate in tests for viewsets.

All you need to is create `tester.py`(you what ever you want it's just recommendation).
In this file declare new class which inherits `ApiActionTester`.

```python
class CRUDApiActionTester(
    saritasa_drf_tools.testing.ApiActionTester.init_subclass(
        model=models.TestModel, # Model of queryset in viewset
        user_model=models.User, # Model of user used across project
        factory=factories.TestModelFactory, # Factory which is used to generate instances for model
        api_view=api.views.CRUDView, # Class of viewset against which we will be writing tests
        url_basename="crud-api", # Base name of urls of viewset. {url_basename}-{action}
    ),
):
    """Tester for crud API."""
```

Next you can write test just like this. (For more examples check this [folder](tests/test_crud_api))

```python
class TestCRUD(tester.CRUDApiActionTester):
    """Define tests."""

    @pytest.mark.parametrize(
        argnames=[
            "parametrize_user",
            "status_code",
        ],
        argvalues=[
            [
                None,
                status.HTTP_403_FORBIDDEN,
            ],
            [
                pytest_lazy_fixtures.lf("user"),
                status.HTTP_403_FORBIDDEN,
            ],
            [
                pytest_lazy_fixtures.lf("admin"),
                status.HTTP_201_CREATED,
            ],
        ],
    )
    def test_permission_map_specified_action_create(
        self,
        instance: tester.CRUDApiActionTester.model,
        parametrize_user: tester.CRUDApiActionTester.user_model | None,
        status_code: int,
    ) -> None:
        """Test that create action will properly handle permissions."""
        self.make_request(
            method="post",
            user=parametrize_user,
            expected_status=status_code,
            path=self.lazy_url(action="list"),
            data=self.serialize_data(action="create", data=instance),
        )
```
