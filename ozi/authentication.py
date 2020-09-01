from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication


class ConfigAuthentication(TokenAuthentication):
    def authenticate(self, request):
        config = request.data.get("config")
        if config is None:
            detail = "No config provided."
            raise exceptions.AuthenticationFailed(detail)

        token = config.get("token")
        if token is None:
            detail = "No token provided."
            raise exceptions.AuthenticationFailed(detail)

        return self.authenticate_credentials(token)
