from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from datetime import timedelta
from rest_framework.response import Response
from apikeymgr.apps.key.models import APIKey
from apikeymgr.apps.key.serializers import APIKeySerializer
from apikeymgr.apps.key.selectors import get_api_keys_for_current_user
from apikeymgr.apps.key.services import use_api_key


def get_expiry_date_default(EXPIRY_DATE_DEFAULT_DAYS=7):
    return timezone.now() + timedelta(days=EXPIRY_DATE_DEFAULT_DAYS)


class GetAPIKeysView(ListAPIView):
    """Get all API keys the signed in user owns"""

    serializer_class = APIKeySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_api_keys_for_current_user(user=self.request.user)

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = APIKeySerializer(qs, many=True)
        data = serializer.data

        return Response({"message": "success", "count": qs.count(), "data": data})


class GetAPIKeyView(RetrieveAPIView):
    """Get an API key by id, only if the signed in user owns it"""

    serializer_class = APIKeySerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        key = get_api_key_by_id(self.kwargs.get("pk"))

        if key.user == request.user:
            serializer = APIKeySerializer(key)
            data = serializer.data

            return Response({"message": "success", "data": data})
        return Response({"message": "error", "data": "Unauthorised"}, status=403)


class UseAPIKeyView(UpdateAPIView):
    """Simulates the API key usage - just increments count fields"""

    serializer_class = APIKeySerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["patch"]  # no PUT

    def partial_update(self, request, *args, **kwargs):
        api_key_id = kwargs["pk"]

        api_key = use_api_key(api_key_id=api_key_id)
        serializer = self.get_serializer(api_key)
        data = serializer.data

        return Response(
            {
                "message": "Successfully used API key",
                "data": data,
            }
        )


class UpdateAPIKeyNameView(UpdateAPIView):
    """Change the name for the API key"""

    serializer_class = APIKeySerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["patch"]  # no PUT

    def partial_update(self, request, *args, **kwargs):
        api_key_id = kwargs["pk"]
        new_name = kwargs["name"]

        api_key = update_key_name(pk=api_key_id, user=request.user, new_name=new_name)
        serializer = self.get_serializer(api_key)
        data = serializer.data

        return Response(
            {
                "message": "Successfully updated API key name",
                "data": data,
            }
        )


class GenerateAPIKeyView(CreateAPIView):
    """creates new API key"""

    serializer_class = APIKeySerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        raw, hashed = generate_api_key()

        new_key_hashed = APIKey(
            user=request.user, api_key_hash=hashed, expires_at=get_expiry_date_default()
        )

        new_key_hashed.save()

        # this is the only time the user can see the new raw key
        return Response(
            {
                "message": "Successfully created API key",
                "data_raw": raw,
                # "data_hashed": hashed,
            }
        )


class DeactivateAPIKeyView(UpdateAPIView):
    """soft deletes an API key"""

    serializer_class = APIKeySerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["patch"]  # no PUT

    def partial_update(self, request, *args, **kwargs):
        api_key_id = self.kwargs.get("pk")
        api_key = get_api_key_by_id(pk=api_key_id)

        if api_key.user == request.user:
            api_key = soft_delete_api_key(api_key_id=api_key_id)

            return Response(
                {
                    "message": f"successfully deleted API key {api_key['name']}",
                }
            )

        return Response(
            {
                "message": "Unauthorised",
            }
        )
