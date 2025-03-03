import collections.abc
import http
import typing

import django.contrib.auth.models
import django.db.models
import django.urls
import factory as factory_boy
import pytest
import rest_framework.generics
import rest_framework.response
import rest_framework.serializers
import rest_framework.status
import rest_framework.test

DjangoUserModelT = typing.TypeVar(
    "DjangoUserModelT",
    bound=django.contrib.auth.models.AbstractBaseUser,
)
DjangoModelT = typing.TypeVar(
    "DjangoModelT",
    bound=django.db.models.Model,
)
RestAPIViewT = typing.TypeVar(
    "RestAPIViewT",
    bound=rest_framework.generics.GenericAPIView,
)
DjangoUserModelParam = typing.TypeVar(
    "DjangoUserModelParam",
    bound=django.contrib.auth.models.AbstractBaseUser,
)
DjangoModelParam = typing.TypeVar(
    "DjangoModelParam",
    bound=django.db.models.Model,
)
RestAPIViewParam = typing.TypeVar(
    "RestAPIViewParam",
    bound=rest_framework.generics.GenericAPIView,
)


class ApiActionTester(
    typing.Generic[
        DjangoModelT,
        DjangoUserModelT,
        RestAPIViewT,
    ],
):
    """Class helper for testing api."""

    url_basename: str
    type factory_type = type[
        factory_boy.django.DjangoModelFactory[DjangoModelT]  # type: ignore
    ]
    factory: factory_type
    type model_type = type[DjangoModelT]  # type: ignore
    model: model_type
    type user_model_type = type[DjangoUserModelT]  # type: ignore
    user_model: user_model_type
    type api_view_type = type[RestAPIViewT]  # type: ignore
    api_view: api_view_type

    @classmethod
    def init_subclass(
        cls: type[
            """ApiActionTester[
                typing.Any,
                typing.Any,
                typing.Any
            ]
            """
        ],
        factory: type[factory_boy.django.DjangoModelFactory[DjangoModelParam]],
        model: type[DjangoModelParam],
        user_model: type[DjangoUserModelParam],
        api_view: type[RestAPIViewParam],
        url_basename: str,
        mixins: collections.abc.Sequence[type] = (),
    ) -> type[
        """ApiActionTester[
            DjangoModelParam,
            DjangoUserModelParam,
            RestAPIViewParam
        ]
        """
    ]:
        """Init subclass.

        A more simple and parametrized way to create sub class. It allows for
        more generics specification

        """
        cls_factory = factory
        cls_model = model
        cls_user_model = user_model
        cls_api_view = api_view

        class Tester(
            *mixins,  # type: ignore
            cls[  # type: ignore
                model,  # type: ignore
                user_model,  # type: ignore
                api_view,  # type: ignore
            ],
            url_basename=url_basename,
        ):
            factory = cls_factory
            model = cls_model
            user_model = cls_user_model
            api_view = cls_api_view

        return Tester

    def __init_subclass__(
        cls,
        url_basename: str | None = None,
    ) -> None:
        """Set up api action tester class."""
        if not url_basename:
            return
        cls.url_basename = url_basename

    def lazy_url(
        self,
        action: str = "",
        **kwargs,
    ) -> str:
        """Get lazy url to action."""
        viewname = "-".join(filter(None, (self.url_basename, action)))
        return django.urls.reverse_lazy(
            viewname=viewname,
            kwargs=kwargs,
        )

    def get_serializer(
        self,
        action: str,
    ) -> type[rest_framework.serializers.Serializer]:
        """Get serializer for api view."""
        return self.api_view(action=action).get_serializer_class()

    def serialize_data(
        self,
        action: str,
        data: DjangoModelT | dict[str, typing.Any],
    ) -> rest_framework.serializers.ReturnDict:
        """Serialize data by using view's action serializer."""
        return self.get_serializer(action=action)(instance=data).data  # type: ignore

    def extract_errors_from_response(
        self,
        response: rest_framework.response.Response,
        field: str,
    ) -> list[str]:
        """Extract errors from response."""
        assert response.data  # noqa: S101
        assert field in response.data, response.data  # noqa: S101
        return response.data[field]

    def check_errors_from_response(
        self,
        response: rest_framework.response.Response,
        field: str,
        expected_errors: collections.abc.Sequence[str],
    ) -> None:
        """Extract errors and check that expected errors are present."""
        errors = set(
            self.extract_errors_from_response(
                response=response,
                field=field,
            ),
        )
        assert errors == set(expected_errors), errors ^ set(expected_errors)  # noqa: S101

    def invoke_factory(self, **kwargs) -> DjangoModelT:
        """Generate instance."""
        return self.factory.create(**kwargs)

    def invoke_factory_build(self, **kwargs) -> DjangoModelT:
        """Build instance."""
        return self.factory.build(**kwargs)

    def invoke_factory_batch(
        self,
        size: int = 5,
        **kwargs,
    ) -> list[DjangoModelT]:
        """Generate instances."""
        return self.factory.create_batch(
            size=size,
            **kwargs,
        )  # type: ignore

    def get_api_client(self) -> rest_framework.test.APIClient:
        """Get api client for requests."""
        return rest_framework.test.APIClient()

    def make_request(
        self,
        method: http.HTTPMethod,
        path: str,
        data: dict[str, typing.Any] | list[typing.Any] | None = None,
        expected_status: int | None = None,
        api_client: rest_framework.test.APIClient | None = None,
        user: DjangoModelT | None = None,
        **kwargs,
    ) -> rest_framework.response.Response:
        """Make api request."""
        api_client = api_client or self.get_api_client()
        if user:
            api_client.force_authenticate(user)
        response: rest_framework.response.Response = getattr(
            api_client,
            method.lower(),
        )(
            path=path,
            data=data,
            **kwargs,
        )
        if not expected_status and method == http.HTTPMethod.POST.lower():
            expected_status = rest_framework.status.HTTP_201_CREATED
        if not expected_status and method == http.HTTPMethod.DELETE.lower():
            expected_status = rest_framework.status.HTTP_204_NO_CONTENT
        if not expected_status:
            expected_status = rest_framework.status.HTTP_200_OK
        assert response.status_code == expected_status, (  # noqa: S101
            response.status_code,
            response.data,
        )
        return response

    @pytest.fixture
    def instance_kwargs(self) -> dict[str, typing.Any]:
        """Get kwargs for instance generation."""
        return {}

    @pytest.fixture
    def instance(
        self,
        instance_kwargs: dict[str, typing.Any],
    ) -> DjangoModelT:
        """Generate instance."""
        return self.factory(**instance_kwargs)  # type: ignore

    @pytest.fixture
    def instance_batch_kwargs(self) -> dict[str, typing.Any]:
        """Get kwargs for instance batch generation."""
        return {}

    @pytest.fixture
    def instance_batch(
        self,
        instance_batch_kwargs: dict[str, typing.Any],
    ) -> list[DjangoModelT]:
        """Create instances batch for testing."""
        instance_batch_kwargs.setdefault("size", 5)
        return self.factory.create_batch(**instance_batch_kwargs)
