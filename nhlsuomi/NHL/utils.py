from datetime import datetime
from typing import Any, Callable

import pytz


def pluck(obj: dict, path: str, default: Any = None) -> Any:
    for key in path.split('.'):
        try:
            obj = obj[key]
        except (KeyError, TypeError):
            return default
    return obj


def dt_localizer(tz: str) -> Callable[[datetime], datetime]:
    timezone = pytz.timezone(tz)

    def fun(dt: datetime) -> str:
        if dt.tzinfo:
            raise ValueError('Not naive datetime')

        return dt + timezone.utcoffset(dt)

    return fun
