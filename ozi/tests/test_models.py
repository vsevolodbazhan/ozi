from django.contrib.auth import get_user_model
from django.test import TestCase
from faker import Faker

from ..models import Client

User = get_user_model()
fake = Faker()


class TestClient(TestCase):
    def setUp(self):
        self.user = User.objects.create(email=fake.email(), password=fake.password())

    def test_string_representation(self):
        client = Client.objects.create(user=self.user, name=fake.pystr())

        self.assertEqual(str(client), client.name)

    def test_verbose_name(self):
        verbose_name = Client._meta.verbose_name

        self.assertEqual(verbose_name, "client")

    def test_verbose_name_plural(self):
        verbose_name_plural = Client._meta.verbose_name_plural

        self.assertEqual(verbose_name_plural, "clients")
