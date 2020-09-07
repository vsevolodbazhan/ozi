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


class TestListMailings:
    @pytest.fixture
    def data(self, config):
        return config

    @pytest.fixture
    def url(self):
        return reverse("list-mailings")

    def test_list_mailings_with_no_mailings(self, client, url, data):
        response = client.post(url, data, content_type="application/json")

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_list_mailings(self, client, url, data, user, faker):
        for _ in range(5):
            Mailing.objects.create(user=user, name=faker.pystr())

        response = client.post(url, data, content_type="application/json")

        assert response.status_code == status.HTTP_200_OK
        assert set(response.data.keys()) == set(["mailings"])

    def test_list_mailings_requires_authentication(self, client, url, data):
        response = client.post(url, content_type="application/json")

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert set(response.data.keys()) == set(["detail"])


class TestListSubscriptions:
    @pytest.fixture
    def data(self, _client, config):
        return {"bot_id": _client.bot, "chat_id": _client.chat, **config}

    @pytest.fixture
    def url(self):
        return reverse("list-subscriptions")

    def test_list_subscriptions_with_no_subscriptions(self, client, url, data):
        response = client.post(url, data, content_type="application/json")

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_list_subscriptions(self, client, url, data, user, _client, faker):
        for _ in range(5):
            mailing = Mailing.objects.create(user=user, name=faker.pystr())
            _client.subscriptions.add(mailing)

        response = client.post(url, data, content_type="application/json")

        assert response.status_code == status.HTTP_200_OK
        assert set(response.data.keys()) == set(["subscriptions"])

    def test_list_subscriptions_creates_client(self, client, url, data):
        response = client.post(url, data, content_type="application/json")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Client.objects.count() == 1

    def test_list_subscriptions_requires_authentication(self, client, url, data):
        data.pop("config")
        response = client.post(url, content_type="application/json")

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert set(response.data.keys()) == set(["detail"])


class TestSubscribeClient:
    @pytest.fixture
    def data(self, mailing, _client, config):
        return {
            "bot_id": _client.bot,
            "chat_id": _client.chat,
            "mailing_id": mailing.id,
            **config,
        }

    @pytest.fixture
    def data_subscribed(self, mailing, subscribed_client, config):
        return {
            "bot_id": subscribed_client.bot,
            "chat_id": subscribed_client.chat,
            "mailing_id": mailing.id,
            **config,
        }

    @pytest.fixture
    def url(self):
        return reverse("subscribe-client")

    def test_subscribe_client_requires_authentication(self, client, url, data):
        data.pop("config")
        response = client.post(url, data, content_type="application/json")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_subscribe_client(self, client, url, data, _client):
        response = client.post(url, data, content_type="application/json")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert _client.subscriptions.count() == 1

    def test_subscribe_client_creates_client(self, client, url, data, faker):
        data["chat_id"] = faker.pystr()
        data["bot_id"] = faker.pystr()
        response = client.post(url, data, content_type="application/json")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Client.objects.count() == 2

    def test_subscribe_client_requires_mailing(self, client, url, data, faker):
        data["mailing_id"] = faker.pyint()
        response = client.post(url, data, content_type="application/json")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert set(response.data.keys()) == set(["detail"])

    def test_subscribe_client_can_conflict(self, client, url, data_subscribed):
        response = client.post(
            url, data=data_subscribed, content_type="application/json"
        )

        assert response.status_code == status.HTTP_409_CONFLICT
        assert set(response.data.keys()) == set(["detail"])


class TestUnsubscribeClient:
    @pytest.fixture
    def data(self, mailing, _client, config):
        return {
            "bot_id": _client.bot,
            "chat_id": _client.chat,
            "mailing_id": mailing.id,
            **config,
        }

    @pytest.fixture
    def data_subscribed(self, mailing, subscribed_client, config):
        return {
            "bot_id": subscribed_client.bot,
            "chat_id": subscribed_client.chat,
            "mailing_id": mailing.id,
            **config,
        }

    @pytest.fixture
    def url(self):
        return reverse("unsubscribe-client")

    def test_subscribe_client_requires_authentication(self, client, url, data):
        data.pop("config")
        response = client.post(url, data, content_type="application/json")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_unsubscribe_client(self, client, url, data_subscribed, subscribed_client):
        response = client.post(
            url,
            data=data_subscribed,
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert subscribed_client.subscriptions.count() == 0

    def test_unsubscribe_client_creates_client(self, client, url, data, faker):
        data["chat_id"] = faker.pystr()
        data["bot_id"] = faker.pystr()
        response = client.post(url, data, content_type="application/json")

        assert response.status_code == status.HTTP_409_CONFLICT
        assert set(response.data.keys()) == set(["detail"])

    def test_unsubscribe_client_can_conflict(self, client, url, data):
        response = client.post(url, data, content_type="application/json")

        assert response.status_code == status.HTTP_409_CONFLICT
        assert set(response.data.keys()) == set(["detail"])

    def test_unsubscribe_client_requires_mailing(self, client, url, data, faker):
        data["mailing_id"] = faker.pyint()
        response = client.post(url, data, content_type="application/json")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert set(response.data.keys()) == set(["detail"])


class TestFindMailing:
    @pytest.fixture
    def data(self, mailing, config):
        return {"name": mailing.name, **config}

    @pytest.fixture
    def url(self):
        return reverse("find-mailing")

    def test_find_mailing_requires_authentication(self, client, url, data):
        data.pop("config")
        response = client.post(url, data, content_type="application/json")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_find_mailing_by_exact_name(self, client, url, data, mailing):
        response = client.post(url, data, content_type="application/json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["mailing_id"] == mailing.id

    def test_find_mailing_by_fuzzy_name(self, client, url, data, mailing):
        data["name"] = mailing.name.lower() + "x"
        response = client.post(url, data, content_type="application/json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["mailing_id"] == mailing.id

    def test_find_mailing_can_fail(self, client, url, data, mailing, faker):
        data["name"] = mailing.name.lower() + faker.pystr()
        response = client.post(url, data, content_type="application/json")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert set(response.data.keys()) == set(["detail"])


class TestPlanUpdate:
    CHATS_COUNT = 5

    @pytest.fixture
    def hours(self, faker):
        return faker.pyint()

    @pytest.fixture
    def minutes(self, faker):
        return faker.pyint()

    @pytest.fixture
    def common_data(self, _client, mailing, hours, minutes, config):
        return {
            "mailing_id": str(mailing.id),
            "bot_id": _client.bot,
            "hours": hours,
            "minutes": minutes,
            **config,
        }

    @pytest.fixture
    def for_client_data(self, _client, common_data):
        common_data["chat_id"] = _client.chat
        return common_data

    @pytest.fixture
    def for_all_data(self, common_data, faker):
        chats = ", ".join(faker.pystr() for _ in range(self.CHATS_COUNT))
        common_data["chats"] = chats
        return common_data

    @pytest.fixture
    def for_client_url(self):
        return reverse("plan-update-for-client")

    @pytest.fixture
    def for_all_url(self):
        return reverse("plan-update-for-all")

    def test_plan_update_for_client_requires_authentication(
        self, client, for_client_url, for_client_data
    ):
        for_client_data.pop("config")
        response = client.post(
            for_client_url, for_client_data, content_type="application/json"
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_plan_update_for_client_creates_update(
        self, client, for_client_url, for_client_data
    ):
        response = client.post(
            for_client_url, for_client_data, content_type="application/json"
        )

        assert response.status_code == status.HTTP_202_ACCEPTED
        assert Update.objects.count() == 1

    def test_plan_update_for_client_creates_update_without_hours_and_minutes(
        self, client, for_client_url, for_client_data
    ):
        for_client_data.pop("hours")
        for_client_data.pop("minutes")
        response = client.post(
            for_client_url, for_client_data, content_type="application/json"
        )

        assert response.status_code == status.HTTP_202_ACCEPTED
        assert Update.objects.count() == 1

    def test_plan_update_for_all_requires_authentication(
        self, for_all_url, client, for_all_data
    ):
        for_all_data.pop("config")
        response = client.post(
            for_all_url, for_all_data, content_type="application/json"
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_plan_update_for_all_creates_update(
        self, client, for_all_url, for_all_data
    ):
        response = client.post(
            for_all_url, for_all_data, content_type="application/json"
        )

        assert response.status_code == status.HTTP_202_ACCEPTED
        assert Update.objects.count() == self.CHATS_COUNT

    def test_plan_update_for_all_creates_update_without_hours_and_minutes(
        self, client, for_all_url, for_all_data
    ):
        for_all_data.pop("hours")
        for_all_data.pop("minutes")
        response = client.post(
            for_all_url, for_all_data, content_type="application/json"
        )

        assert response.status_code == status.HTTP_202_ACCEPTED
        assert Update.objects.count() == self.CHATS_COUNT

    def test_plan_update_for_creates_clients(self, client, for_all_url, for_all_data):
        client_count = Client.objects.count()

        response = client.post(
            for_all_url, for_all_data, content_type="application/json"
        )

        assert response.status_code == status.HTTP_202_ACCEPTED
        assert Client.objects.count() == self.CHATS_COUNT + client_count

    def test_plan_update_for_all_creates_update_without_chats(
        self, client, for_all_url, for_all_data, _client, mailing
    ):
        _client.subscriptions.add(mailing)

        for_all_data.pop("chats")
        response = client.post(
            for_all_url, for_all_data, content_type="application/json"
        )

        assert response.status_code == status.HTTP_202_ACCEPTED
        assert Client.objects.count() == 1


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
        return reverse("schedule-update-for-client")

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
