from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase
from faker import Faker

from ..models import Client, Mailing

User = get_user_model()
fake = Faker()


class TestMailing(TestCase):
    def setUp(self):
        self.user = User.objects.create(email=fake.email(), password=fake.password())

    def test_string_representation(self):
        mailing = Mailing.objects.create(user=self.user, name=fake.pystr())

        self.assertEqual(str(mailing), mailing.name)

    def test_verbose_name(self):
        verbose_name = Mailing._meta.verbose_name

        self.assertEqual(verbose_name, "Mailing")

    def test_verbose_name_plural(self):
        verbose_name_plural = Mailing._meta.verbose_name_plural

        self.assertEqual(verbose_name_plural, "Mailings")

    def test_unique_contraints(self):
        name = fake.pystr()

        with self.assertRaises(IntegrityError):
            for _ in range(2):
                Mailing.objects.create(user=self.user, name=name)


class TestClient(TestCase):
    def test_string_representation(self):
        client = Client.objects.create(bot=fake.pystr(), chat=fake.pystr())

        self.assertEqual(str(client), f"{client.bot}, {client.chat}")

    def test_verbose_name(self):
        verbose_name = Client._meta.verbose_name

        self.assertEqual(verbose_name, "Client")

    def test_verbose_name_plural(self):
        verbose_name_plural = Client._meta.verbose_name_plural

        self.assertEqual(verbose_name_plural, "Clients")

    def test_unique_contraints(self):
        bot, chat = fake.pystr(), fake.pystr()

        with self.assertRaises(IntegrityError):
            for _ in range(2):
                Client.objects.create(bot=bot, chat=chat)
