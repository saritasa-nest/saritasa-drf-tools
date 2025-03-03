from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from .app.api import views

api_router = routers.DefaultRouter()
api_router.register(
    "crud-api",
    views.CRUDView,
    basename="crud-api",
)
api_router.register(
    "drf-standardized-errors-crud-api",
    views.DRFStandardizedErrorsCRUDView,
    basename="drf-standardized-errors-crud-api",
)
api_router.register(
    "read-only-api",
    views.ReadOnlyView,
    basename="read-only-api",
)

urlpatterns = [
    *api_router.urls,
    *static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    ),
    path(
        "simple-api-view/",
        views.APIView.as_view(),
        name="simple-api-view",
    ),
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        "api/schema/openapi-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="openapi-ui",
    ),
]
