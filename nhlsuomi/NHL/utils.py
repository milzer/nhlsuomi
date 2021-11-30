from datetime import date, datetime
from typing import Any, Callable, Mapping

import pytz

_SENTINEL = object()

def pluck(obj: Mapping, path: str, default: Any = _SENTINEL) -> Any:
    for key in path.split('.'):
        try:
            obj = obj[key]
        except (KeyError, TypeError) as e:
            if default == _SENTINEL:
                raise LookupError(path) from e
            else:
                return default
    return obj


def dt_localizer(tz: str) -> Callable[[datetime], datetime]:
    timezone = pytz.timezone(tz)

    def fun(dt: datetime) -> datetime:
        if dt.tzinfo:
            raise ValueError('Not naive datetime')

        offset = timezone.utcoffset(dt)

        if offset is not None:
            return dt + offset
        else:
            # TODO: raise an exception here?
            return dt

    return fun


def format_date(d: date) -> str:
    return d.strftime('%Y-%m-%d')
