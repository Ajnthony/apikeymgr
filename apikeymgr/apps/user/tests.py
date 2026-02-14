from django.test import TestCase, Client
from django.contrib.auth import get_user_model


class APIKeyTest(TestCase):
    def setUp(self):
        User = get_user_model()
        User.objects.create_user(
            # id=1,
            # full_name="",
            # username="user19345",
            email="user1@test.com",
            password="1234",
            # created_at=timezone.now,
            # updated_at=None,
            plan="free",
            is_suspended=False,
            is_staff=False,
            is_active=True,
        )
        User.objects.create_user(
            # id=2,
            # full_name="",
            # username="user23257",
            email="user2@test.com",
            password="1234",
            # created_at=timezone.now,
            # updated_at=None,
            plan="pro",
            is_suspended=False,
            is_staff=False,
            is_active=True,
        )

    def test_user_created(self):
        user_one = get_user_model().objects.get(email="user1@test.com")
        user_two = get_user_model().objects.get(email="user2@test.com")

        self.assertEqual(user_one.plan, "free")
        self.assertEqual(user_two.plan, "pro")
