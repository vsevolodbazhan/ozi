ACCEPTED_DISTANCE_THRESHOLD = 2


def distance_is_acceptable(
    distance: int, threshold: int = ACCEPTED_DISTANCE_THRESHOLD
) -> bool:
    return distance <= threshold


def normalize(text: str) -> str:
    return remove_whitespaces(text.lower())


def remove_whitespaces(text: str) -> str:
    return "".join(text.split())
