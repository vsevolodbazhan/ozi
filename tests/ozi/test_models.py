import pytest
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from ozi.models import Client, Mailing

User = get_user_model()


@pytest.mark.django_db
class TestMailing:
    def test_string_representation(self, user, faker):
        mailing = Mailing.objects.create(user=user, name=faker.pystr())

        assert str(mailing) == mailing.name

    def test_verbose_name(self):
        verbose_name = Mailing._meta.verbose_name

        assert verbose_name == "Mailing"

    def test_verbose_name_plural(self):
        verbose_name_plural = Mailing._meta.verbose_name_plural

        assert verbose_name_plural == "Mailings"

    def test_unique_contraints(self, user, faker):
        name = faker.pystr()

        with pytest.raises(IntegrityError):
            for _ in range(2):
                Mailing.objects.create(user=user, name=name)


@pytest.mark.django_db
class TestClient:
    def test_string_representation(self, faker):
        client = Client.objects.create(bot=faker.pystr(), chat=faker.pystr())

        assert str(client) == f"{client.bot}, {client.chat}"

    def test_verbose_name(self):
        verbose_name = Client._meta.verbose_name

        assert verbose_name == "Client"

    def test_verbose_name_plural(self):
        verbose_name_plural = Client._meta.verbose_name_plural

        assert verbose_name_plural == "Clients"

    def test_unique_contraints(self, faker):
        bot, chat = faker.pystr(), faker.pystr()

        with pytest.raises(IntegrityError):
            for _ in range(2):
                Client.objects.create(bot=bot, chat=chat)

    def test_client_is_subscribed(self, user, faker):
        mailing = Mailing.objects.create(user=user, name=faker.pystr())
        client = Client.objects.create(bot=faker.pystr(), chat=faker.pystr())

        client.subscriptions.add(mailing)

        assert client.is_subscribed(mailing)

    def test_client_is_not_subscribed(self, user, faker):
        mailing = Mailing.objects.create(user=user, name=faker.pystr())
        client = Client.objects.create(bot=faker.pystr(), chat=faker.pystr())

        assert client.is_subscribed(mailing) is False
