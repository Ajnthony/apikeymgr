from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import APIKey
from .serializers import APIKeySerializer
from .selectors import get_api_keys_for_current_user
from .services import use_api_key


class GetAPIKeysView(ListAPIView):
    serializer_class = APIKeySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_api_keys_for_current_user(user=self.request.user)

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = APIKeySerializer(qs, many=True)
        data = serializer.data

        return Response({"message": "success", "count": qs.count(), "data": data})


class UseAPIKeyView(UpdateAPIView):
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
