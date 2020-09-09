from accounts.models import Token
from django.contrib.auth import get_user_model

__all__ = ["get_token_model", "get_user_model"]


def get_token_model():
    return Token
