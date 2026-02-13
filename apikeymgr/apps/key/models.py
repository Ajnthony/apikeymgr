import uuid
from django.db import models
from django.conf import settings


class APIKey(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False
    )
    api_key_hash = models.CharField(max_length=128, unique=True, editable=False)
    name = models.CharField(max_length=30, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)
    daily_use_count = models.IntegerField(default=0)
    total_use_count = models.IntegerField(default=0)
    revoked_at = models.DateTimeField(default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self):
        return f"{self.name} API key for {self.user}"
