from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Token

from ..models import Mailing
from ..utilities import build_config

User = get_user_model()
fake = Faker()


class TestMailing(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email=fake.email(), password=fake.password())
        self.token = Token.objects.get(user=self.user)
        self.config = build_config({"token": str(self.token)})

    def test_list_mailings_with_no_mailings(self):
        url = reverse("list-mailings")
        response = self.client.post(url, self.config)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_mailings(self):
        for _ in range(5):
            Mailing.objects.create(user=self.user, name=fake.pystr())

        url = reverse("list-mailings")
        response = self.client.post(url, self.config)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual(response.data, ["mailings"])

    def test_requires_authentication(self):
        url = reverse("list-mailings")
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertCountEqual(response.data, ["detail"])
