from rest_framework.serializers import ModelSerializer
from .models import APIKey
from user.serializers import UserSerializer

SHARED_FIELDS = ()


class APIKeySerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = APIKey
        fields = (
            "name",
            "id",
            "api_key_hash",
            "user",
            "is_active",
            "revoked_at",
            "created_at",
            "last_used_at",
        )

        read_only_fields = (
            "id",
            "api_key_hash",
            "user",
            "is_active",
            "revoked_at",
            "created_at",
            "expires_at",
            "last_used_at",
        )


# TODO
# create different serialisers for each view
