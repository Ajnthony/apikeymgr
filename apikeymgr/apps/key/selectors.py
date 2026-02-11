from django.shortcuts import get_object_or_404
from .models import APIKey


def get_api_keys_for_current_user(*, user):
    data = APIKey.objects.filter(user=user, is_active=True).order_by("-created_at")

    return data


def get_api_key_by_id(*, pk):
    api_key = get_object_or_404(APIKey, id=pk)

    return api_key
