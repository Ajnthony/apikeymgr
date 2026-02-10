from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import APIKey


class APIKeyAdmin(admin.ModelAdmin):
    ordering = ["created_at"]
    list_display = (
        "id",
        "name",
        "user",
        "is_active",
        "revoked_at",
        "created_at",
        "last_used_at",
        "expires_at",
    )

    readonly_fields = (
        "id",
        "user",
        "created_at",
        "last_used_at",
        "expires_at",
    )

    fieldsets = (
        (
            _("Basic info"),
            {
                "fields": (
                    "name",
                    "user",
                )
            },
        ),
        (
            _("Details"),
            {
                "fields": (
                    "is_active",
                    "revoked_at",
                    "created_at",
                    "last_used_at",
                    "expires_at",
                )
            },
        ),
    )


admin.site.register(APIKey, APIKeyAdmin)
