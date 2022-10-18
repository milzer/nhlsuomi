import json
import urllib.request
from datetime import date, timedelta
from typing import Mapping, Optional
from urllib.parse import urlencode


def _build_url(path: str, **query_args):
    return f'https://statsapi.web.nhl.com/api/v1{path}?{urlencode(query_args)}'


def _fetch_json(url: str) -> Mapping:
    with urllib.request.urlopen(url) as res:
        data = res.read()
        encoding = res.info().get_content_charset('utf-8')
        return json.loads(data.decode(encoding))


def schedule(date: Optional[date] = None, days_more: int = 0) -> Mapping:
    # NOTE: maybe support these game types as well when the time comes WCOH_PRELIM, WCOH_FINAL
    query_args = {
        'gameType': 'R,P,A'
    }

    if date:
        if days_more > 0:
            query_args['startDate'] = date.isoformat()
            query_args['endDate'] = (date + timedelta(days=days_more)).isoformat()
        else:
            query_args['date'] = date.isoformat()

    url = _build_url('/schedule', **query_args)
    return _fetch_json(url)


def boxscore(gameid: int) -> Mapping:
    url = _build_url(f'/game/{gameid}/boxscore')
    return _fetch_json(url)


def teams() -> Mapping:
    url = _build_url('/teams')
    return _fetch_json(url)
