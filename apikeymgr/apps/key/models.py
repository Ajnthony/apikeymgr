import uuid
from django.db import models
from django.conf import settings


class APIKey(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False
    )
    api_key = models.CharField(max_length=128, unique=True, editable=False)
    name = models.CharField(max_length=30)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} API key for {self.user}"
