from django.test import TestCase, Client
from django.utils import timezone
from .models import APIKey
from user.models import User


class APIKeyTest(TestCase):
    def setUp(self):
        user_one = User.objects.create(
            id=1,
            full_name="",
            username="user19345",
            email="user1@test.com",
            created_at=timezone.now,
            updated_at=None,
            plan="free",
            is_suspended=False,
            is_staff=False,
            is_active=True,
        )
        user_two = User.objects.create(
            id=2,
            full_name="",
            username="user23257",
            email="user2@test.com",
            created_at=timezone.now,
            updated_at=None,
            plan="pro",
            is_suspended=False,
            is_staff=False,
            is_active=True,
        )

        APIKey.objects.create(id=1, user=user_one, api_key_hash="abc123")
        APIKey.objects.create(id=2, user=user_two, api_key_hash="def456")
        APIKey.objects.create(id=3, user=user_one, api_key_hash="ghi789")

    def test_api_key_has_fields(self):
        user_one_keys = APIKey.objects.filter(user=1)
        user_two_keys = APIKey.objects.filter(user=2)

        self.assertEqual(user_one_keys.count(), 2)
        self.assertEqual(user_two_keys.count(), 1)
