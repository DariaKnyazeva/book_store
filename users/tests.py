from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import UserRole

User = get_user_model()


class TestUser(TestCase):
    def test_create_user(self):
        """
        Make sure that Customer user role is created by default
        """
        user = User.objects.create_user(username="daria")
        self.assertEqual(UserRole.CUSTOMER, user.user_role)
