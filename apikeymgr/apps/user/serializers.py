from rest_framework import serializers
from apikeymgr.apps.user.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20, write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "full_name",
            "username",
            "email",
            "created_at",
            "updated_at",
            "is_suspended",
            "password",
        )

        read_only_fields = (
            "id",
            "created_at",
            "email",
            "is_suspended",
            "email",
            "updated_at",
        )
