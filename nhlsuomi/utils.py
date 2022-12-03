from datetime import datetime
from typing import Callable

import pytz


def dt_localizer(tz: str) -> Callable[[datetime], datetime]:
    timezone = pytz.timezone(tz)

    def localizer_func(dt: datetime) -> datetime:
        if dt.tzinfo:
            raise ValueError('Not naive datetime')

        try:
            return dt + timezone.utcoffset(dt)
        except TypeError:
            return dt

    return localizer_func
