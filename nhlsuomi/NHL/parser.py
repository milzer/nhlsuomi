from typing import Iterable, Mapping, Optional

from nhlsuomi.data import Game
from nhlsuomi.logging import logger


def parse_recap_url(game: Mapping) -> Optional[str]:
    epg = game['content']['media']['epg']

    try:
        # find the recap content
        recap = next(filter(
            lambda x: x['title'] == 'Recap',
            epg
        ))

        # just take the first item with 'video' type
        item = next(filter(
            lambda x: x['type'] == 'video',
            recap['items']
        ))

        # take the last item with name starting FLASH_ for now
        # assuming it's the best quality
        playback = next(filter(
            lambda x: x['name'].startswith('FLASH_'),
            reversed(item['playbacks'])
        ))

        return playback['url']

    except Exception:
        logger.exception('Recap url parsing failed')

    return None


def parse_schedule_games(schedule: Mapping) -> Iterable[Game]:
    for date in schedule['dates']:
        for game in date['games']:
            if game['status']['detailedState'] == 'Postponed':
                continue

            state = game['status']['abstractGameState']

            if state not in {'Preview', 'Live', 'Final'}:
                logger.warning(f'Invalid abstractGameState: {state}')
                continue

            recap_url = parse_recap_url(game)

            yield Game(
                game['teams']['home']['team']['abbreviation'],
                game['teams']['home']['score'],
                game['teams']['away']['team']['abbreviation'],
                game['teams']['away']['score'],
                state == 'Final',
                game['gamePk'],
                recap_url
            )
