import pathlib
import json
import urllib.request

BASE_URL = 'https://statsapi.web.nhl.com'


def _fetch_url_as_dict(url: str, *, dumpfile: str = '') -> dict:
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


def fetch_games(date: str, *, dumpfile: str = '') -> dict:
    url = f'{BASE_URL}/api/v1/schedule?expand=schedule.teams&date={date}'
    return _fetch_url_as_dict(url, dumpfile=dumpfile)


def fetch_boxscore(game_id: str) -> dict:
    url = f'{BASE_URL}/api/v1/game/{game_id}/boxscore'
    return _fetch_url_as_dict(url)
