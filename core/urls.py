from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from .views import handle_request



# generate swagger UI schema
schema_view = get_schema_view(
    openapi.Info(
        title="Subsidio API",
        default_version="v1",
        description="Subsidio API",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

api_patterns = [
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="documentation",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path('bets/', include('bets.urls'))
]


urlpatterns = [
    # path('', handle_request, name='handle_request'),
    path('admin/', admin.site.urls),
    path("api/", include(api_patterns)),
]
