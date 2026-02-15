from django.urls import path, include
from apikeymgr.apps.key.views import (
    GetAPIKeysView,
    GetAPIKeyView,
    UseAPIKeyView,
    UpdateAPIKeyNameView,
    GenerateAPIKeyView,
    DeactivateAPIKeyView,
    AdminDeleteAPIKeyView,
)

app_name = "key"

urlpatterns = [
    path(
        "",
        include(
            [
                path("", GetAPIKeysView.as_view(), name="get-api-keys"),
                path("<str:pk>/", GetAPIKeyView.as_view(), name="get-api-key"),
                path("<str:pk>/call/", UseAPIKeyView.as_view(), name="use-api-key"),
                path(
                    "<str:pk>/deactivate/",
                    DeactivateAPIKeyView.as_view(),
                    name="deactivate-api-key",
                ),
                path(
                    "<str:pk>/update-name/",
                    UpdateAPIKeyNameView.as_view(),
                    name="update-api-key-name",
                ),
                path(
                    "<str:pk>/delete/",
                    AdminDeleteAPIKeyView.as_view(),
                    name="delete-api-key",
                ),
                path("", GenerateAPIKeyView.as_view(), name="generate-api-key"),
            ]
        ),
    )
]
