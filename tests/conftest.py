import pytest

from accounts.models import User, Token


@pytest.fixture
def email(faker):
    return faker.email()


@pytest.fixture
def password(faker):
    return faker.password()


@pytest.fixture
def user(db, faker):
    return User.objects.create(email=faker.email(), password=faker.password())


@pytest.fixture
def token(db, user):
    return Token.objects.get(user=user)


@pytest.fixture
def config(token):
    return {"config": {"token": str(token)}}


@pytest.fixture
def empty_config():
    return {"config": {}}
