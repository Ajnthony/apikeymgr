from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient


class APIKeyTest(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.client = APIClient()

        User.objects.create_user(
            email="user1@test.com",
            password="1234",
            plan="free",
            is_suspended=False,
            is_staff=False,
            is_active=True,
        )
        User.objects.create_user(
            email="user2@test.com",
            password="1234",
            plan="pro",
            is_suspended=False,
            is_staff=False,
            is_active=True,
        )

    def test_user_created(self):
        user_one = get_user_model().objects.get(email="user1@test.com")
        user_two = get_user_model().objects.get(email="user2@test.com")

        self.assertIsNotNone(user_one.email)
        self.assertIsNotNone(user_two.email)

        self.assertEqual(user_one.is_suspended, False)
        self.assertEqual(user_two.is_suspended, False)

        self.assertEqual(user_one.is_active, True)
        self.assertEqual(user_two.is_active, True)

    def test_user_plan_match(self):
        user_one = get_user_model().objects.get(email="user1@test.com")
        user_two = get_user_model().objects.get(email="user2@test.com")

        self.assertEqual(user_one.plan, "free")
        self.assertEqual(user_two.plan, "pro")

    def test_incorrect_pw_should_fail_authentication(self):
        attempt = self.client.login(email="user1@test.com", password="2345")
        self.assertFalse(attempt)

    def test_correct_pw_should_authenticate(self):
        attempt = self.client.login(email="user1@test.com", password="1234")
        self.assertTrue(attempt)
