import json
import time
import urllib.request
from datetime import date, timedelta
from typing import Mapping, Optional
from urllib.error import URLError
from urllib.parse import urlencode

from nhlsuomi.logging import logger

BASE_URL = 'https://statsapi.web.nhl.com/api/v1'


def _fetch_json(url: str, *, retries: int = 3) -> Mapping:
    for retry in range(retries + 1):
        try:
            action = 'Retry' if retry else 'Fetch'
            logger.info(f'{action} {url}')

            with urllib.request.urlopen(url) as res:
                data = res.read()
                encoding = res.info().get_content_charset('utf-8')
                return json.loads(data.decode(encoding))

        except URLError as e:
            logger.warning(f'Fetch failed: {e}')
            time.sleep(10)

    raise RuntimeError('Too many retries')


def get_schedule(date: Optional[date] = None, days: int = 1) -> Mapping:
    args = {
        'gameType': ','.join(('R', 'P', 'A', 'WCOH_PRELIM', 'WCOH_FINAL')),
        'expand': ','.join(
            (
                'schedule.teams',
                'schedule.game.content.highlights.all',
                'schedule.game.content.media.epg',
            )
        ),
    }

    if date:
        if days > 1:
            args['startDate'] = date.isoformat()

            date += timedelta(days - 1)
            args['endDate'] = date.isoformat()
        else:
            args['date'] = date.isoformat()

    return _fetch_json(f'{BASE_URL}/schedule?{urlencode(args)}')


def get_boxscore(gameid: int) -> Mapping:
    return _fetch_json(f'{BASE_URL}/game/{gameid}/boxscore')
