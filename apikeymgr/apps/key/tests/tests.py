from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from apikeymgr.apps.key.models import APIKey


class APIKeyTest(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.client = APIClient()

        user_one = User.objects.create_user(
            email="user1@test.com",
            password="1234",
            plan="free",
            is_suspended=False,
            is_staff=False,
            is_active=True,
        )
        user_two = User.objects.create_user(
            email="user2@test.com",
            password="1234",
            plan="pro",
            is_suspended=False,
            is_staff=False,
            is_active=True,
        )

        APIKey.objects.create(id=1, user=user_one, api_key_hash="abc123")
        APIKey.objects.create(id=2, user=user_two, api_key_hash="def456")
        APIKey.objects.create(id=3, user=user_one, api_key_hash="ghi789")

    def test_number_of_api_keys_match(self):
        user_one = get_user_model().objects.get(email="user1@test.com")
        user_two = get_user_model().objects.get(email="user2@test.com")

        user_one_keys = APIKey.objects.filter(user=user_one)
        user_two_keys = APIKey.objects.filter(user=user_two)

        self.assertEqual(user_one_keys.count(), 2)
        self.assertEqual(user_two_keys.count(), 1)

    def test_api_key_has_fields(self):
        user_two = get_user_model().objects.get(email="user2@test.com")

        user_two_key = APIKey.objects.get(user=user_two)

        self.assertEqual(user_two_key.is_active, True)
        self.assertEqual(user_two_key.daily_use_count, 0)
        self.assertEqual(user_two_key.total_use_count, 0)
        self.assertEqual(user_two_key.revoked_at, None)

    def test_soft_delete_should_return_401_for_anonymous(self):
        # intentional no sign in
        response = self.client.patch("/api/key/1/deactivate/")
        status_code = response.status_code
        self.assertEqual(status_code, 401)
