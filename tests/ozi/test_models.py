import json
import secrets

import pytest
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.utils import timezone

from ozi.constants import NUMBER_OF_SECONDS_IN_MINUTE
from ozi.models import Client, Hook, Mailing, Task, Update

User = get_user_model()


def create_client(faker):
    return Client.objects.create(bot=faker.pystr(), chat=faker.pystr())


def create_mailing(user, faker):
    return Mailing.objects.create(user=user, name=faker.pystr())


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
            create_client(faker),
            create_client(faker),
            create_client(faker),
        )
        mailing_1, mailing_2 = (
            create_mailing(user, faker),
            create_mailing(user, faker),
        )

        client_1.subscriptions.add(mailing_1)
        client_1.subscriptions.add(mailing_2)
        client_2.subscriptions.add(mailing_1)

        clients = Client.objects.get_subscribed([mailing_1])

        assert clients.count() == 2
        assert clients.filter(id=client_1.id).exists()
        assert clients.filter(id=client_2.id).exists()


@pytest.mark.django_db
class TestUpdate:
    @pytest.fixture
    def timestamp(self):
        return timezone.now()

    @pytest.fixture
    def mailing(self, user, faker):
        return create_mailing(user, faker)

    @pytest.fixture
    def client(self, faker):
        return create_client(faker)

    @pytest.fixture
    def repeat(self, faker):
        return faker.pyint()

    @pytest.fixture
    def task(self, faker, timestamp, user, mailing, client, repeat):
        return Task.objects.create(
            task_name=faker.pystr(),
            task_params=json.dumps(
                [
                    [],
                    {
                        "user_id": str(user.id),
                        "mailing_id": str(mailing.id),
                        "client_id": str(client.id),
                    },
                ]
            ),
            task_hash=secrets.token_hex(16),
            run_at=timestamp,
            repeat=repeat,
        )

    def test_string_representation(self, task, user, mailing, client, timestamp, faker):
        update = Update.objects.create(
            task=task, user=user, mailing=mailing, client=client
        )

        assert (
            str(update)
            == f"{mailing.name} ({timestamp.time()}, {timestamp.date()}, {client})"
        )

    def test_verbose_name(self):
        verbose_name = Update._meta.verbose_name

        assert verbose_name == "Update"

    def test_verbose_name_plural(self):
        verbose_name_plural = Update._meta.verbose_name_plural

        assert verbose_name_plural == "Updates"

    def test_update_creates_with_task(self, task):
        assert Update.objects.count() == 1
        assert Update.objects.first().task == task

    def test_task_delets_with_update(self, task):
        update = Update.objects.first()
        update.delete()

        assert Update.objects.count() == 0
        assert Task.objects.count() == 0

    def test_update_repeat_string_is_set(self, task, repeat):
        update = Update.objects.first()
        update.repeat = f"Every {repeat // NUMBER_OF_SECONDS_IN_MINUTE} minute(s)"


@pytest.mark.django_db
class TestHook:
    def test_string_representation(self, faker):
        hook = Hook.objects.create(target=faker.url())

        assert str(hook) == hook.target

    def test_verbose_name(self):
        verbose_name = Hook._meta.verbose_name

        assert verbose_name == "Hook"

    def test_verbose_name_plural(self):
        verbose_name_plural = Hook._meta.verbose_name_plural

        assert verbose_name_plural == "Hooks"
