from contextlib import suppress
from datetime import datetime
from typing import Iterable, List, Mapping, Optional, Set, Tuple

from nhlsuomi import utils
from nhlsuomi.data import Game, Goalie, Skater
from nhlsuomi.logging import logger


def _parse_schedule_games(schedule: Mapping, state_filter: Optional[str] = None) -> Iterable[Tuple[Mapping, str]]:
    for date in schedule['dates']:
        for game in date['games']:
            detailed_state = game['status']['detailedState']

            if detailed_state == 'Postponed':
                continue
            elif detailed_state == 'Scheduled':
                state = detailed_state
            else:
                state = game['status']['abstractGameState']

            if state not in {'Preview', 'Live', 'Final', 'Scheduled'}:
                logger.warning(f'Invalid game state: {state}')
                continue

            if state_filter and state != state_filter:
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
    try:
        epg = game['content']['media']['epg']
    except KeyError:
        # content.media is not always present, just ignore those cases
        return None

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

    except StopIteration:
        pass

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
    if not keywords:
        return []

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
        except KeyError:
            # content.highlights is not always present, just ignore those cases
            return []

        for item in items:
            try:
                title = item['title']

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

    # use dict sorted by id so only the latest highlight is returned in case
    # of duplicate titles

    yield from {
        title: url
        for (_, title, url)
        in sorted(highlights)
    }.items()


def _parse_toi(toi: str) -> int:
    mm, ss = toi.split(':')
    return int(mm) * 60 + int(ss)


def parse_boxscore_players(boxscore: Mapping) -> Tuple[List[Skater], List[Goalie]]:
    players = (
        *boxscore['teams']['home']['players'].values(),
        *boxscore['teams']['away']['players'].values()
    )

    skaters: List[Skater] = []
    goalies: List[Goalie] = []

    for player in players:
        with suppress(KeyError):
            stats = player['stats']['skaterStats']

            skaters.append(Skater(
                player['person']['firstName'],
                player['person']['lastName'],
                stats['goals'],
                stats['assists'],
                _parse_toi(stats['timeOnIce']),
                stats['plusMinus'],
                stats['shots'],
                stats['hits'],
                stats['penaltyMinutes'],
                player['person']['nationality']
            ))

        with suppress(KeyError):
            stats = player['stats']['goalieStats']

            goalies.append(Goalie(
                player['person']['firstName'],
                player['person']['lastName'],
                stats['savePercentage'] / 100,
                _parse_toi(stats['timeOnIce']),
                stats['shots'],
                player['person']['nationality']
            ))

    return sorted(skaters), sorted(goalies)


def parse_schedule_upcoming(schedule: Mapping,
                            timezone: str,
                            from_h: int,
                            to_h: int,
                            format: str = '%d.%m. %H:%M') -> Iterable[Tuple[str, str, str]]:
    localizer = utils.dt_localizer(timezone)

    for game, _ in _parse_schedule_games(schedule, state_filter='Scheduled'):
        gamedate = datetime.strptime(game['gameDate'], '%Y-%m-%dT%H:%M:%SZ')
        local_datetime = localizer(gamedate)

        if from_h <= local_datetime.hour < to_h:
            home = game['teams']['home']['team']['name']
            away = game['teams']['away']['team']['name']

            yield (local_datetime.strftime(format), home, away)
