from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # admin page
    path("admin/", admin.site.urls),
    path(
        "api/",
        include(
            [
                # drf-spectacular
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
                # custom apps
                path("key/", include("key.urls")),
            ]
        ),
    ),
]
