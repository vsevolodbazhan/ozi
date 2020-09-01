from django.contrib.auth import get_user_model
from django.test import TestCase
from faker import Faker
from rest_framework.exceptions import PermissionDenied

from accounts.models import Token

from ..authentication import ConfigAuthentication
from ..utilities import build_config

User = get_user_model()
fake = Faker()


class TestConfigAuthentication(TestCase):
    class DummyRequest:
        def __init__(self, data):
            self.data = data

    def setUp(self):
        self.user = User.objects.create(email=fake.email(), password=fake.password())
        self.token = Token.objects.get(user=self.user)
        self.authentication = ConfigAuthentication()

    def test_can_authenticate(self):
        data = build_config({"token": str(self.token)})
        request = self.DummyRequest(data=data)

        user, token = self.authentication.authenticate(request)

        self.assertEqual(user, self.user)
        self.assertEqual(token, self.token)

    def test_config_is_required(self):
        data = {}
        request = self.DummyRequest(data=data)

        with self.assertRaises(PermissionDenied):
            self.authentication.authenticate(request)

    def test_token_is_required(self):
        data = build_config({})
        request = self.DummyRequest(data=data)

        with self.assertRaises(PermissionDenied):
            self.authentication.authenticate(request)
