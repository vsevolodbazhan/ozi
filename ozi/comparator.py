__all__ = ["distance_is_acceptable", "normalize", "levenshtein_distance"]

from django.conf import settings
from Levenshtein import distance as levenshtein_distance


def distance_is_acceptable(distance: int) -> bool:
    return distance <= settings.ACCEPTED_LEVENSHTEIN_DISTANCE_THRESHOLD


def normalize(text: str) -> str:
    return remove_whitespaces(text.lower())


def remove_whitespaces(text: str) -> str:
    return "".join(text.split())
