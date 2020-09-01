__all__ = ["NotFound", "Conflict"]

from rest_framework import status
from rest_framework.exceptions import APIException, NotFound


class Conflict(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "A conflict occurred."
    default_code = "conflict"
