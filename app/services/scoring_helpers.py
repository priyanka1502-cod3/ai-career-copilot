from typing import Any


def normalize_text(value: Any) -> str:
    """
    Convert nested candidate data into searchable lowercase text.
    Supports strings, lists, dictionaries, and other primitive values.
    """
    if value is None:
        return ""

    if isinstance(value, str):
        return value.lower().strip()

    if isinstance(value, list):
        return " ".join(normalize_text(item) for item in value)

    if isinstance(value, dict):
        return " ".join(normalize_text(item) for item in value.values())

    return str(value).lower().strip()


def has_meaningful_value(value: Any) -> bool:
    if value is None:
        return False

    if isinstance(value, str):
        return bool(value.strip())

    if isinstance(value, list):
        return len(value) > 0

    if isinstance(value, dict):
        return len(value) > 0

    return True


def get_first_available(
    candidate: dict[str, Any],
    possible_keys: list[str],
    default: Any = None,
) -> Any:
    """
    Return the first meaningful value found for the supplied keys.
    This makes scoring compatible with slightly different parser models.
    """
    for key in possible_keys:
        value = candidate.get(key)

        if has_meaningful_value(value):
            return value

    return default


def clamp_score(score: float) -> float:
    return round(max(0, min(score, 100)), 2)