from .models import APIKey


def get_api_keys_for_current_user(*, user):
    data = APIKey.objects.filter(user=user, is_active=True).order_by("-created_at")

    return data
