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

    def test_can_be_found_by_fuzzy_name(self, user):
        for i in range(5):
            Mailing.objects.create(user=user, name=f"Mailing {i + 1}")

        fuzzy_name = "mailin1"
        mailings = Mailing.objects.filter(user=user)

        mailing = Mailing.find_by_fuzzy_name(fuzzy_name, mailings)

        assert mailing.id == 1
        assert mailing.name == "Mailing 1"


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

    def test_can_get_subscribed(self, user, faker):
        client_1, client_2, _ = (
            self._create_client(faker),
            self._create_client(faker),
            self._create_client(faker),
        )
        mailing_1, mailing_2 = (
            self._create_mailing(user, faker),
            self._create_mailing(user, faker),
        )

        client_1.subscriptions.add(mailing_1)
        client_1.subscriptions.add(mailing_2)
        client_2.subscriptions.add(mailing_1)

        clients = Client.objects.get_subscribed(mailing_1)

        assert clients.count() == 2
        assert clients.first() == client_1
        assert clients.last() == client_2

    def _create_client(self, faker):
        return Client.objects.create(bot=faker.pystr(), chat=faker.pystr())

    def _create_mailing(self, user, faker):
        return Mailing.objects.create(user=user, name=faker.pystr())
