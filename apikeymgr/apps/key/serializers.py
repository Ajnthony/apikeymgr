from rest_framework.serializers import ModelSerializer
from .models import APIKey
from user.serializers import UserSerializer


class APIKeySerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = APIKey
        fields = (
            "name",
            "expires_at",
            "id",
            "api_key_hash",
            "user",
            "is_active",
            "revoked_at",
            "created_at",
            "last_used_at",
        )

        readonly_fields = (
            "id",
            "api_key_hash",
            "user",
            "is_active",
            "revoked_at",
            "created_at",
            "last_used_at",
        )
