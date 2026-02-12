from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # admin page
    # srv/admin/
    path("admin/", admin.site.urls),
    path(
        "api/",
        include(
            [
                # drf-spectacular
                # srv/api/schema/...
                path(
                    "schema/",
                    include(
                        [
                            path(
                                "",
                                SpectacularAPIView.as_view(),
                                name="schema",
                            ),
                            path(
                                "swagger-ui/",
                                SpectacularSwaggerView.as_view(),
                                name="swagger-ui",
                            ),
                            path(
                                "redoc/", SpectacularRedocView.as_view(), name="redoc"
                            ),
                        ]
                    ),
                ),
                # JWT token
                # srv/api/token/...
                path(
                    "token/",
                    include(
                        [
                            path(
                                "", TokenObtainPairView.as_view(), name="token-obtain"
                            ),
                            path(
                                "refresh/",
                                TokenRefreshView.as_view(),
                                name="token-refresh",
                            ),
                            path(
                                "verify/",
                                TokenVerifyView.as_view(),
                                name="token-verify",
                            ),
                        ]
                    ),
                ),
                # custom apps
                # srv/api/{app_name}/...
                path("key/", include("key.urls")),
            ]
        ),
    ),
]
