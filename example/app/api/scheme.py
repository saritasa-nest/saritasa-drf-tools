from drf_spectacular import utils

import saritasa_drf_tools.open_api

from . import views

saritasa_drf_tools.open_api.fix_api_view_warning(
    views.APIView,
)

utils.extend_schema_view(
    get=utils.extend_schema(
        responses=saritasa_drf_tools.open_api.DetailSerializer,
    ),
)(views.APIView)
