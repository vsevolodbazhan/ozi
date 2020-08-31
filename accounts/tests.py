from django.test import TestCase
from faker import Faker

from .models import User

fake = Faker()


class TestModels(TestCase):
    def test_user_creation(self):
        email, password = fake.email(), fake.password()

        user = User.objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(AttributeError):
            user.username

        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password=password)

    def test_superuser_creation(self):
        email, password = fake.email(), fake.password()

        user = User.objects.create_superuser(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

        with self.assertRaises(AttributeError):
            user.username

        with self.assertRaises(ValueError):
            User.objects.create_superuser(email=email, password=email, is_staff=False)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email=email, password=email, is_superuser=False
            )

    def test_user_is_represented_by_email(self):
        email, password = fake.email(), fake.password()
        user = User.objects.create_user(email=email, password=password)

        self.assertEqual(str(user), user.email)
