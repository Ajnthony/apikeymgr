import secrets
import hashlib
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse
from django.db.models import F
from apikeymgr.apps.key.models import APIKey
from .selectors import get_api_key_by_id

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


def use_api_key(*, api_key_id):
    """
    increments its count fields by 1 whenever called
    and updates last_used_at
    """
    api_key_obj = get_api_key_by_id(pk=api_key_id)

    if api_key_obj["is_active"]:
        api_key_obj["daily_use_count"] = F("daily_use_count") + 1
        api_key_obj["total_use_count"] = F("total_use_count") + 1
        api_key_obj["last_used_at"] = timezone.now()

        api_key_obj.save(
            update_fields=["daily_use_count", "total_use_count", "last_used_at"]
        )
        api_key_obj.refresh_from_db(
            fields=["daily_use_count", "total_use_count", "last_used_at"]
        )

        return api_key_obj


def soft_delete_api_key(*, api_key_id):
    """deactivates the API key, only if the owner is the signed in user"""

    api_key_obj = get_api_key_by_id(pk=api_key_id)

    if api_key_obj["is_active"]:
        api_key_obj["is_active"] = False
        api_key_obj["revoked_at"] = timezone.now()

        api_key_obj.save(update_fields=["is_active", "revoked_at"])
        api_key_obj.refresh_from_db(fields=["is_active", "revoked_at"])

        return api_key_obj
