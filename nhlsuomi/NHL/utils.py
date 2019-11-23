from typing import Any


def pluck(obj: dict, path: str, default: Any = None) -> Any:
    for key in path.split('.'):
        try:
            obj = obj[key]
        except (KeyError, TypeError):
            return default
    return obj
