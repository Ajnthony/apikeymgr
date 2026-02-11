from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    ordering = ["created_at"]
    list_display = (
        "id",
        "full_name",
        "username",
        "email",
        "created_at",
        "updated_at",
        "is_suspended",
        "plan",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            _("Basic info"),
            {
                "fields": (
                    "full_name",
                    "username",
                    "email",
                    "plan",
                    "is_suspended",
                )
            },
        ),
        (_("Password"), {"fields": ("password",)}),
        (
            _("Details"),
            {
                "fields": (
                    "id",
                    "created_at",
                    "updated_at",
                    "is_superuser",
                )
            },
        ),
    )

    add_fieldsets = (
        _("User details"),
        {
            "classes": ("wide"),
            "fields": (
                "email",
                "password",
                "password2",
            ),
        },
    )


admin.site.register(get_user_model(), UserAdmin)
