"""
URL configuration for Bsf_nutrifeed project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny


schema_view = get_schema_view(
    openapi.Info(
        title="BSF-Nutrifeed API",
        default_version="V1",
        description=(
            "Backend API for BSF-Nutrifeed platform"
            "Solution for sustainable poultry feed production"
        ),
        contact=openapi.Contact(email="Sjaypeter.sjp@gmail.com"),
        license=openapi.License(name="MIT")

    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    #Auth
    path("api/auth", include("users.urls")),
    path("api/auth/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    #Core resources
    path("api/feed", include("feed_production.urls")),
    path("api/monitoring", include("monitoring.urls")),

    #Swagger/ Redoc
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc"),
    path("swagger.json",schema_view.without_ui(cache_timeout=0), name="swagger-json"),
]
