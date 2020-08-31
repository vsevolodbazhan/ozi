from django.test import TestCase
from faker import Faker

from .models import User

fake = Faker()


class TestModels(TestCase):
    def setUp(self):
        self.email = fake.email()
        self.password = fake.password()

    def test_user_creation(self):
        user = User.objects.create_user(email=self.email, password=self.password)

        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password(self.password))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(AttributeError):
            user.username

        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password=self.password)

    def test_superuser_creation(self):
        user = User.objects.create_superuser(email=self.email, password=self.password)

        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password(self.password))
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

        with self.assertRaises(AttributeError):
            user.username

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email=self.email, password=self.password, is_staff=False
            )

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email=self.email, password=self.password, is_superuser=False
            )

    def test_string_representation(self):
        user = User.objects.create_user(email=self.email, password=self.password)

        self.assertEqual(str(user), user.email)

    def test_verbose_name(self):
        verbose_name = User._meta.verbose_name

        self.assertEqual(verbose_name, "user")

    def test_verbose_name_plural(self):
        verbose_name_plural = User._meta.verbose_name_plural

        self.assertEqual(verbose_name_plural, "users")
