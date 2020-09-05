import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from ozi.models import Client, Mailing, Update

User = get_user_model()


@pytest.fixture
def mailing(db, user, faker):
    return Mailing.objects.create(user=user, name=faker.pystr())


@pytest.fixture
def _client(db, faker):
    return Client.objects.create(bot=faker.pystr(), chat=faker.pystr())


@pytest.fixture
def subscribed_client(db, mailing, faker):
    client = Client.objects.create(bot=faker.pystr(), chat=faker.pystr())
    client.subscriptions.add(mailing)
    return client


@pytest.fixture
def list_mailings_url():
    return reverse("list-mailings")


@pytest.fixture
def list_subscriptions_url():
    return reverse("list-subscriptions")


@pytest.fixture
def subscribe_client_url():
    return reverse("subscribe-client")


@pytest.fixture
def unsubscribe_client_url():
    return reverse("unsubscribe-client")


@pytest.fixture
def find_mailing_url():
    return reverse("find-mailing")


@pytest.fixture
def plan_update_url():
    return reverse("plan-update")


def test_list_mailings_with_no_mailings(list_mailings_url, client, config):
    response = client.post(list_mailings_url, config, content_type="application/json")

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_list_mailings(list_mailings_url, client, config, user, faker):
    for _ in range(5):
        Mailing.objects.create(user=user, name=faker.pystr())

    response = client.post(list_mailings_url, config, content_type="application/json")

    assert response.status_code == status.HTTP_200_OK
    assert set(response.data.keys()) == set(["mailings"])


def test_list_mailings_requires_authentication(list_mailings_url, client):
    response = client.post(list_mailings_url, content_type="application/json")

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert set(response.data.keys()) == set(["detail"])


def test_list_subscriptions_with_no_subscriptions(
    list_subscriptions_url, client, config, _client, faker
):
    data = {"bot_id": _client.bot, "chat_id": _client.chat, **config}
    response = client.post(
        list_subscriptions_url, data, content_type="application/json"
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_list_subscriptions(
    list_subscriptions_url, client, config, user, _client, faker
):
    for _ in range(5):
        mailing = Mailing.objects.create(user=user, name=faker.pystr())
        _client.subscriptions.add(mailing)

    data = {"bot_id": _client.bot, "chat_id": _client.chat, **config}
    response = client.post(
        list_subscriptions_url, data, content_type="application/json"
    )

    assert response.status_code == status.HTTP_200_OK
    assert set(response.data.keys()) == set(["subscriptions"])


def test_list_subscriptions_creates_client(
    list_subscriptions_url, client, config, faker
):
    data = {"bot_id": faker.pystr(), "chat_id": faker.pystr(), **config}
    response = client.post(
        list_subscriptions_url, data, content_type="application/json"
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Client.objects.count() == 1


def test_list_subscriptions_requires_authentication(list_subscriptions_url, client):
    response = client.post(list_subscriptions_url, content_type="application/json")

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert set(response.data.keys()) == set(["detail"])


def test_subscribe_client(subscribe_client_url, client, config, _client, mailing):
    url = reverse("subscribe-client")
    data = {
        "chat_id": _client.chat,
        "bot_id": _client.bot,
        "mailing_id": mailing.id,
        **config,
    }
    response = client.post(url, data, content_type="application/json")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert _client.subscriptions.count() == 1


def test_subscribe_client_creates_client(
    subscribe_client_url, client, config, mailing, faker
):
    data = {
        "chat_id": faker.pystr(),
        "bot_id": faker.pystr(),
        "mailing_id": mailing.id,
        **config,
    }
    response = client.post(subscribe_client_url, data, content_type="application/json")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Client.objects.count() == 1


def test_subscribe_client_requires_mailing(
    subscribe_client_url, client, config, _client, faker
):
    data = {
        "chat_id": _client.chat,
        "bot_id": _client.bot,
        "mailing_id": faker.pyint(),
        **config,
    }
    response = client.post(subscribe_client_url, data, content_type="application/json")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert set(response.data.keys()) == set(["detail"])


def test_subscribe_client_can_conflict(
    subscribe_client_url, client, config, subscribed_client, mailing
):
    data = {
        "chat_id": subscribed_client.chat,
        "bot_id": subscribed_client.bot,
        "mailing_id": mailing.id,
        **config,
    }
    response = client.post(subscribe_client_url, data, content_type="application/json")

    assert response.status_code == status.HTTP_409_CONFLICT
    assert set(response.data.keys()) == set(["detail"])


def test_subscribe_client_requires_authentication(
    subscribe_client_url, client, _client, mailing
):
    data = {
        "chat_id": _client.chat,
        "bot_id": _client.bot,
        "mailing_id": mailing.id,
    }
    response = client.post(subscribe_client_url, data, content_type="application/json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_unsubscribe_client(
    unsubscribe_client_url, client, config, subscribed_client, mailing
):
    data = {
        "chat_id": subscribed_client.chat,
        "bot_id": subscribed_client.bot,
        "mailing_id": mailing.id,
        **config,
    }
    response = client.post(
        unsubscribe_client_url, data, content_type="application/json"
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert subscribed_client.subscriptions.count() == 0


def test_unsubscribe_client_creates_client(
    unsubscribe_client_url, client, config, mailing, faker
):
    data = {
        "chat_id": faker.pystr(),
        "bot_id": faker.pystr(),
        "mailing_id": mailing.id,
        **config,
    }
    response = client.post(
        unsubscribe_client_url, data, content_type="application/json"
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert set(response.data.keys()) == set(["detail"])


def test_unsubscribe_client_can_conflict(
    unsubscribe_client_url, client, config, _client, mailing
):
    data = {
        "chat_id": _client.chat,
        "bot_id": _client.bot,
        "mailing_id": mailing.id,
        **config,
    }
    response = client.post(
        unsubscribe_client_url, data, content_type="application/json"
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert set(response.data.keys()) == set(["detail"])


def test_unsubscribe_client_requires_mailing(
    unsubscribe_client_url, client, config, _client, faker
):
    data = {
        "chat_id": _client.chat,
        "bot_id": _client.bot,
        "mailing_id": faker.pyint(),
        **config,
    }
    response = client.post(
        unsubscribe_client_url, data, content_type="application/json"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert set(response.data.keys()) == set(["detail"])


def test_unsubscribe_client_requires_authentication(
    unsubscribe_client_url, client, _client, mailing
):
    data = {
        "chat_id": _client.chat,
        "bot_id": _client.bot,
        "mailing_id": mailing.id,
    }
    response = client.post(
        unsubscribe_client_url, data, content_type="application/json"
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_find_mailing_by_exact_name(find_mailing_url, client, config, mailing):
    data = {"name": mailing.name, **config}
    response = client.post(find_mailing_url, data, content_type="application/json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["mailing_id"] == mailing.id


def test_find_mailing_by_fuzzy_name(find_mailing_url, client, config, mailing):
    data = {"name": mailing.name.lower() + "x", **config}
    response = client.post(find_mailing_url, data, content_type="application/json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["mailing_id"] == mailing.id


def test_find_mailing_can_fail(find_mailing_url, client, config, mailing, faker):
    data = {"name": mailing.name.lower() + faker.pystr(), **config}
    response = client.post(find_mailing_url, data, content_type="application/json")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert set(response.data.keys()) == set(["detail"])


def test_find_mailing_requires_authentication(find_mailing_url, client, faker):
    data = {"name": faker.pystr()}
    response = client.post(find_mailing_url, data, content_type="application/json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


class TestPlanUpdate:
    @pytest.fixture
    def hours(self, faker):
        return faker.pyint()

    @pytest.fixture
    def minutes(self, faker):
        return faker.pyint()

    @pytest.fixture
    def data(self, _client, mailing, hours, minutes, config):
        return {
            "mailingId": mailing.id,
            "botId": _client.bot,
            "chatId": _client.chat,
            "hours": hours,
            "minutes": minutes,
            **config,
        }

    @pytest.fixture
    def url(self, plan_update_url):
        return plan_update_url

    def test_plan_update_requires_authentication(self, url, client, data):
        data.pop("config")
        response = client.post(url, data, content_type="application/json")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_plan_update_creates_update(self, client, url, data):
        response = client.post(url, data, content_type="application/json")

        assert response.status_code == status.HTTP_202_ACCEPTED
        assert Update.objects.count() == 1

    def test_plan_update_creates_update_without_hours_and_minutes(
        self, client, url, data
    ):
        data.pop("hours")
        data.pop("minutes")
        response = client.post(url, data, content_type="application/json")

        assert response.status_code == status.HTTP_202_ACCEPTED
        assert Update.objects.count() == 1


class TestScheduleUpdate:
    @pytest.fixture
    def timestamp(self, faker):
        return faker.date_time()

    @pytest.fixture
    def repeat(self, faker):
        return faker.pyint()

    @pytest.fixture
    def data(self, _client, mailing, timestamp, repeat, config):
        return {
            "mailingId": mailing.id,
            "botId": _client.bot,
            "chatId": _client.chat,
            "time": timestamp.time(),
            "date": timestamp.date(),
            "repeat": repeat,
            **config,
        }

    @pytest.fixture
    def url(self):
        return reverse("schedule-update")

    def test_schedule_update_requires_authentication(self, client, url, data):
        data.pop("config")
        response = client.post(url, data, content_type="application/json")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_schedule_update_creates_update_without_time(self, client, url, data):
        data.pop("time")
        response = client.post(url, data, content_type="application/json")

        assert response.status_code == status.HTTP_202_ACCEPTED
        assert Update.objects.count() == 1

    def test_schedule_update_creates_update_without_date(self, client, url, data):
        data.pop("date")
        response = client.post(url, data, content_type="application/json")

        assert response.status_code == status.HTTP_202_ACCEPTED
        assert Update.objects.count() == 1

    def test_schedule_update_creates_update_without_repeat(self, client, url, data):
        data.pop("repeat")
        response = client.post(url, data, content_type="application/json")

        assert response.status_code == status.HTTP_202_ACCEPTED
        assert Update.objects.count() == 1

    def test_schedule_update_creates_update(self, client, url, data):
        response = client.post(url, data, content_type="application/json")

        assert response.status_code == status.HTTP_202_ACCEPTED
        assert Update.objects.count() == 1
