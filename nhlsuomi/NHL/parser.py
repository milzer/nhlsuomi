from contextlib import suppress
from typing import Iterable, List, Mapping, Optional, Set, Tuple

from nhlsuomi.data import Game, Goalie, Skater
from nhlsuomi.logging import logger


def _parse_schedule_games(schedule: Mapping) -> Iterable[Tuple[Mapping, str]]:
    for date in schedule['dates']:
        for game in date['games']:
            if game['status']['detailedState'] == 'Postponed':
                continue

            state = game['status']['abstractGameState']

            if state not in {'Preview', 'Live', 'Final'}:
                logger.warning(f'Invalid abstractGameState: {state}')
                continue

            yield game, state


def _parse_best_playback_url(playbacks: List[Mapping]) -> Optional[str]:
    # take the last item with name starting FLASH_ for now
    # assuming it's the best quality
    try:
        with suppress(StopIteration):
            best_playback = next(filter(
                lambda x: x['name'].startswith('FLASH_'),
                reversed(playbacks)
            ))
            return best_playback['url']

    except Exception:
        logger.exception('Playback parsing failed')

    return None


def _parse_recap_url(game: Mapping) -> Optional[str]:
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

        return _parse_best_playback_url(item['playbacks'])

    except Exception:
        logger.exception('Recap url parsing failed')

    return None


def parse_schedule_games(schedule: Mapping) -> Iterable[Game]:
    for game, state in _parse_schedule_games(schedule):
        recap_url = _parse_recap_url(game)

        yield Game(
            game['teams']['home']['team']['abbreviation'],
            game['teams']['home']['score'],
            game['teams']['away']['team']['abbreviation'],
            game['teams']['away']['score'],
            state == 'Final',
            game['gamePk'],
            recap_url
        )


def parse_schedule_highlights(schedule: Mapping, keywords: Set[str] = set()) -> Iterable[Tuple[str, str]]:
    keywords = {
        keyword.strip().casefold()
        for keyword
        in keywords
    }

    highlights = []

    for game, state in _parse_schedule_games(schedule):
        if state != 'Final':
            continue

        try:
            items = game['content']['highlights']['gameCenter']['items']
        except Exception:
            logger.exception('Highlight items not found')
            return []

        for item in items:
            try:
                title = item['blurb'] or item['title']

                if keywords:
                    lowercase_title = title.casefold()

                    for keyword in keywords:
                        if keyword in lowercase_title:
                            break
                    else:
                        # keyword not found so skip this highlight
                        continue

                id_ = int(item['id'])

                if url := _parse_best_playback_url(item['playbacks']):
                    highlights.append((id_, title, url))

            except Exception:
                logger.exception('Playback parsing failed')

    # sort by id
    yield from (
        (title, url)
        for (_, title, url)
        in sorted(highlights)
    )


def parse_boxscore_players(boxscore: Mapping, nationalities: Set[str] = set()) -> Iterable[Mapping]:
    players = (
        *boxscore['teams']['home']['players'].values(),
        *boxscore['teams']['away']['players'].values()
    )

    if nationalities:
        for player in players:
            if player['person']['nationality'] in nationalities:
                yield player
    else:
        yield from players


def _parse_toi(toi: str) -> int:
    mm, ss = toi.split(':')
    return int(mm) * 60 + int(ss)


def parse_players_skaters(players: Iterable[Mapping]) -> Iterable[Skater]:
    for player in players:
        with suppress(KeyError):
            stats = player['stats']['skaterStats']

            yield Skater(
                player['person']['firstName'],
                player['person']['lastName'],
                stats['goals'],
                stats['assists'],
                _parse_toi(stats['timeOnIce']),
                stats['plusMinus'],
                stats['shots'],
                stats['hits'],
                stats['penaltyMinutes']
            )


def parse_players_goalies(players: Iterable[Mapping]) -> Iterable[Goalie]:
    for player in players:
        with suppress(KeyError):
            stats = player['stats']['goalieStats']

            yield Goalie(
                player['person']['firstName'],
                player['person']['lastName'],
                stats['savePercentage'],
                _parse_toi(stats['timeOnIce']),
                stats['shots']
            )
