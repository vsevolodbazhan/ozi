import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied

from accounts.models import Token

from ..authentication import ConfigAuthentication
from ..utilities import build_config

User = get_user_model()


@pytest.fixture
def user(db, faker):
    return User.objects.create(email=faker.email(), password=faker.password())


@pytest.fixture
def token(db, user):
    return Token.objects.get(user=user)


@pytest.fixture
def config(token):
    return build_config({"token": str(token)})


@pytest.fixture
def empty_config():
    return build_config({})


@pytest.fixture
def config_authentication():
    return ConfigAuthentication()


class DummyRequest:
    def __init__(self, data):
        self.data = data


def test_can_authenticate(user, token, config, config_authentication):
    request = DummyRequest(data=config)
    _user, _token = config_authentication.authenticate(request)

    assert _user == user
    assert _token == token


def test_token_is_required(config_authentication):
    request = DummyRequest(data={})

    with pytest.raises(PermissionDenied):
        config_authentication.authenticate(request)


def test_config_is_required(empty_config, config_authentication):
    request = DummyRequest(data=empty_config)

    with pytest.raises(PermissionDenied):
        config_authentication.authenticate(request)
