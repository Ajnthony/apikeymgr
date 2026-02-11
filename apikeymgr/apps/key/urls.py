from django.urls import path, include
from .views import GetAPIKeysView, UseAPIKeyView

app_name = "key"

urlpatterns = [
    path(
        "",
        include(
            [
                path("", GetAPIKeysView.as_view(), name="get-api-keys"),
                path("<str:pk>/", UseAPIKeyView.as_view(), name="use-api-key"),
            ]
        ),
    )
]
