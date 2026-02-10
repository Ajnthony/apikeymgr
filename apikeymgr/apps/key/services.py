import secrets
import hashlib
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse
from .models import APIKey

API_KEY_LENGTH = 32


def generate_api_key():
    raw = secrets.token_urlsafe(API_KEY_LENGTH)
    hashed = hashlib.sha256(raw.encode()).hexdigest()

    return raw, hashed


def rotate_api_key(*, api_key=APIKey, immediate=True):
    new_raw, new_hashed = generate_api_key()

    new_key = APIKey.objects.create(user=api_key.user, api_key_hash=new_hashed)

    if immediate:
        api_key.is_active = False
        api_key.revoked_at = timezone.now()
        api_key.save(update_fields=["is_active", "revoked_at"])

        return new_key, new_raw


def update_key_name(*, pk, user, new_name):
    api_key_obj = get_object_or_404(APIKey, pk=pk)

    if api_key_obj.user == user:
        api_key_obj.name = new_name
        api_key_obj.save()

        return api_key_obj

    return HttpResponse("Access denied", status=403)
