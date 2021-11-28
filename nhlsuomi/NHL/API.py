import json
import pathlib
import urllib.request
from datetime import datetime, timedelta
from typing import Mapping

from nhlsuomi.NHL import utils

BASE_URL = 'https://statsapi.web.nhl.com/api/v1'


def _fetch_url_as_dict(url: str, *, dumpfile: str = '') -> Mapping:
    with urllib.request.urlopen(url) as res:
        data = res.read()
        encoding = res.info().get_content_charset('utf-8')

        obj = json.loads(data.decode(encoding))

        if dumpfile:
            path = pathlib.Path.cwd() / dumpfile
            print(f'Dumping {path}...', end='')
            path.write_text(json.dumps(obj, indent=4))
            print('ok')

        return obj


def fetch_games(date: datetime.date, *, dumpfile: str = '') -> Mapping:
    date_str = utils.format_date(date)
    url = f'{BASE_URL}/schedule?expand=schedule.teams&date={date_str}'
    return _fetch_url_as_dict(url, dumpfile=dumpfile)


def fetch_boxscore(game_id: str) -> Mapping:
    url = f'{BASE_URL}/game/{game_id}/boxscore'
    return _fetch_url_as_dict(url)


def fetch_upcoming_schedule(days: int) -> Mapping:
    now = datetime.now()
    start = utils.format_date(now)
    end = utils.format_date(now + timedelta(days=days))
    url = f'{BASE_URL}/schedule?startDate={start}&endDate={end}'
    return _fetch_url_as_dict(url)
