import pytest

from .models import User, Token


@pytest.fixture
def email(faker):
    return faker.email()


@pytest.fixture
def password(faker):
    return faker.password()


@pytest.mark.django_db
def test_user_creation(email, password):
    user = User.objects.create_user(email=email, password=password)

    assert user.email == email
    assert user.check_password(password)
    assert user.is_active
    assert user.is_staff is False
    assert user.is_superuser is False

    with pytest.raises(AttributeError):
        user.username

    with pytest.raises(ValueError):
        User.objects.create_user(email="", password=password)


@pytest.mark.django_db
def test_superuser_creation(email, password):
    user = User.objects.create_superuser(email=email, password=password)

    assert user.email == email
    assert user.check_password(password)
    assert user.is_active
    assert user.is_staff
    assert user.is_superuser

    with pytest.raises(AttributeError):
        user.username

    with pytest.raises(ValueError):
        User.objects.create_superuser(email=email, password=password, is_staff=False)

    with pytest.raises(ValueError):
        User.objects.create_superuser(
            email=email, password=password, is_superuser=False
        )


@pytest.mark.django_db
def test_token_is_created_with_user(email, password):
    user = User.objects.create_user(email=email, password=password)

    assert Token.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_string_representation(email, password):
    user = User.objects.create_user(email=email, password=password)

    assert str(user) == user.email


def test_verbose_name():
    verbose_name = User._meta.verbose_name

    assert verbose_name == "User"


def test_verbose_name_plural():
    verbose_name_plural = User._meta.verbose_name_plural

    assert verbose_name_plural == "Users"
