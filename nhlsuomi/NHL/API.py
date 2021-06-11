import json
import pathlib
import urllib.request
from datetime import datetime, timedelta
from typing import Mapping

BASE_URL = 'https://statsapi.web.nhl.com'


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


def fetch_games(date: str, *, dumpfile: str = '') -> Mapping:
    url = f'{BASE_URL}/api/v1/schedule?expand=schedule.teams&date={date}'
    return _fetch_url_as_dict(url, dumpfile=dumpfile)


def fetch_boxscore(game_id: str) -> Mapping:
    url = f'{BASE_URL}/api/v1/game/{game_id}/boxscore'
    return _fetch_url_as_dict(url)


def fetch_upcoming_schedule(days: int) -> Mapping:
    date_format = '%Y-%m-%d'
    now = datetime.now()
    start = now.strftime(date_format)
    end = (now + timedelta(days=days)).strftime(date_format)
    url = f'{BASE_URL}/api/v1/schedule?startDate={start}&endDate={end}'
    return _fetch_url_as_dict(url)
