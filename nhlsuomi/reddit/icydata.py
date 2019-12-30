import re
from collections import OrderedDict
from datetime import datetime, timedelta
from typing import Iterable, List, Mapping, Tuple

import praw
from more_itertools import unique_everseen

from nhlsuomi import VERSION

USER_AGENT = f'NHLSuomi/{VERSION}'
DEFAULT_LIMIT = 300


def fetch_submissions(client_id: str, client_secret: str,
                      username: str, password: str,
                      *,
                      limit: int = DEFAULT_LIMIT):

    reddit = praw.Reddit(user_agent=USER_AGENT,
                         client_id=client_id, client_secret=client_secret,
                         username=username, password=password)

    for submission in reddit.subreddit('icydata').new(limit=limit):
        yield {
            'title': submission.title,
            'created': submission.created,
            'url': submission.url
        }


def parse_hilights_recaps(submissions: Iterable[dict],
                          keywords: Iterable[str],
                          tzoffset_hours: int,
                          *,
                          _now: callable = datetime.now) -> Tuple[List, Mapping]:

    tzoffset = tzoffset_hours * 60 * 60
    targetdate = (_now() - timedelta(days=1)).strftime('%d.%m.%Y')
    hilights = []
    recaps = OrderedDict()
    team_abbrevs = {
        'S.J': 'SJS',
        'L.A': 'LAK',
        'N.J': 'NJD',
        'T.B': 'TBL'
    }

    for submission in submissions:
        title = submission['title']
        title_low = title.lower()
        url = submission['url']

        if 'recap:' in title_low:
            teams = re.search(
                r'(Recap:)\s*(?P<away>\S{3})\s*@\s*(?P<home>\S{3})',
                title
            )

            if teams:
                home = teams.group('home')
                away = teams.group('away')
                home = team_abbrevs.get(home, home)
                away = team_abbrevs.get(away, away)
                recaps[f'{home}{away}'] = url
        else:
            for keyword in keywords:
                if keyword.lower() in title_low:
                    date = datetime \
                        .utcfromtimestamp(submission['created']) \
                        .strftime('%d.%m.%Y')

                    if date == targetdate:
                        hilights.append((title, url))

    return list(unique_everseen(hilights)), recaps
