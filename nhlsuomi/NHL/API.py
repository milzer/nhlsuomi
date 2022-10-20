import json
import urllib.request
from datetime import date, timedelta
from typing import Mapping, Optional
from urllib.parse import urlencode


BASE_URL = 'https://statsapi.web.nhl.com/api/v1'


def _fetch_json(url: str) -> Mapping:
    with urllib.request.urlopen(url) as res:
        data = res.read()
        encoding = res.info().get_content_charset('utf-8')
        return json.loads(data.decode(encoding))


def schedule(date: Optional[date] = None, days: int = 1) -> Mapping:
    args = {
        'gameType': ','.join(('R', 'P', 'A', 'WCOH_PRELIM', 'WCOH_FINAL')),
        'expand' : ','.join(('schedule.teams', 'schedule.game.content.highlights.all'))
    }

    if date:
        if days > 1:
            args['startDate'] = date.isoformat()

            date += timedelta(days-1)
            args['endDate'] = date.isoformat()
        else:
            args['date'] = date.isoformat()

    return _fetch_json(f'{BASE_URL}/schedule?{urlencode(args)}')


def boxscore(gameid: int) -> Mapping:
    return _fetch_json(f'{BASE_URL}/game/{gameid}/boxscore')
