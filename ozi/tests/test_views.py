from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Token

from ..models import Client, Mailing
from ..utilities import build_config

User = get_user_model()
fake = Faker()


def set_up():
    user = User.objects.create(email=fake.email(), password=fake.password())
    token = Token.objects.get(user=user)
    config = build_config({"token": str(token)})

    return user, config


class TestMailing(APITestCase):
    def setUp(self):
        self.user, self.config = set_up()

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

    def test_list_mailings_requires_authentication(self):
        url = reverse("list-mailings")
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertCountEqual(response.data, ["detail"])


class TestClient(APITestCase):
    def setUp(self):
        self.user, self.config = set_up()
        self._client = Client.objects.create(bot=fake.pystr(), chat=fake.pystr())

    def test_list_subscriptions_with_no_subscriptions(self):
        url = reverse("list-subscriptions")
        data = {"bot_id": self._client.bot, "chat_id": self._client.chat, **self.config}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_subscriptions(self):
        for _ in range(5):
            mailing = Mailing.objects.create(user=self.user, name=fake.pystr())
            self._client.subscriptions.add(mailing)

        url = reverse("list-subscriptions")
        data = {"bot_id": self._client.bot, "chat_id": self._client.chat, **self.config}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual(response.data, ["subscriptions"])

    def test_list_subscriptions_requires_authentication(self):
        url = reverse("list-subscriptions")
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertCountEqual(response.data, ["detail"])
