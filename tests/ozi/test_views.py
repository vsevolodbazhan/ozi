import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from ozi.models import Client, Mailing

User = get_user_model()


@pytest.fixture
def _client(db, faker):
    return Client.objects.create(bot=faker.pystr(), chat=faker.pystr())


def test_list_mailings_with_no_mailings(client, config):
    url = reverse("list-mailings")
    response = client.post(url, config, content_type="application/json")

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_list_mailings(client, config, user, faker):
    for _ in range(5):
        Mailing.objects.create(user=user, name=faker.pystr())

    url = reverse("list-mailings")
    response = client.post(url, config, content_type="application/json")

    assert response.status_code == status.HTTP_200_OK
    assert set(response.data.keys()) == set(["mailings"])


def test_list_mailings_requires_authentication(client):
    url = reverse("list-mailings")
    response = client.post(url, content_type="application/json")

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert set(response.data.keys()) == set(["detail"])


def test_list_subscriptions_with_no_subscriptions(client, config, _client, faker):
    url = reverse("list-subscriptions")
    data = {"bot_id": _client.bot, "chat_id": _client.chat, **config}
    response = client.post(url, data, content_type="application/json")

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_list_subscriptions(client, config, user, _client, faker):
    for _ in range(5):
        mailing = Mailing.objects.create(user=user, name=faker.pystr())
        _client.subscriptions.add(mailing)

    url = reverse("list-subscriptions")
    data = {"bot_id": _client.bot, "chat_id": _client.chat, **config}
    response = client.post(url, data, content_type="application/json")

    assert response.status_code == status.HTTP_200_OK
    assert set(response.data.keys()) == set(["subscriptions"])


def test_list_subscriptions_creates_client(client, config, faker):
    url = reverse("list-subscriptions")
    data = {"bot_id": faker.pystr(), "chat_id": faker.pystr(), **config}

    response = client.post(url, data, content_type="application/json")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Client.objects.count() == 1


def test_list_subscriptions_requires_authentication(client):
    url = reverse("list-subscriptions")
    response = client.post(url, content_type="application/json")

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert set(response.data.keys()) == set(["detail"])
