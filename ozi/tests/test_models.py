from django.contrib.auth import get_user_model
from django.test import TestCase
from faker import Faker

from ..models import Mailing

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

        self.assertEqual(verbose_name, "mailing")

    def test_verbose_name_plural(self):
        verbose_name_plural = Mailing._meta.verbose_name_plural

        self.assertEqual(verbose_name_plural, "mailing")
