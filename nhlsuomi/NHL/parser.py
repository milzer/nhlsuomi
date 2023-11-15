from contextlib import suppress
from datetime import datetime
from typing import Iterable, List, Mapping, Optional, Tuple

from nhlsuomi import utils
from nhlsuomi.data import Game, Goalie, Skater
from nhlsuomi.logging import logger


def _parse_schedule_games(
    schedule: Mapping, state_filter: Optional[str] = None
) -> Iterable[Tuple[Mapping, str]]:
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
                logger.warning('Invalid game state: %s', state)
                continue

            if state_filter and state != state_filter:
                continue

            yield game, state


def parse_schedule_games(schedule: Mapping) -> Iterable[Game]:
    for game, state in _parse_schedule_games(schedule):
        yield Game(
            game['teams']['home']['team']['abbreviation'],
            game['teams']['home']['score'],
            game['teams']['away']['team']['abbreviation'],
            game['teams']['away']['score'],
            state == 'Final',
            game['gamePk'],
        )

def _parse_toi(toi: str) -> int:
    mm, ss = toi.split(':')
    return int(mm) * 60 + int(ss)


def parse_boxscore_players(
    boxscore: Mapping
) -> Tuple[List[Skater], List[Goalie]]:
    players = (
        *boxscore['teams']['home']['players'].values(),
        *boxscore['teams']['away']['players'].values(),
    )

    skaters: List[Skater] = []
    goalies: List[Goalie] = []

    for player in players:
        with suppress(KeyError):
            stats = player['stats']['skaterStats']

            skaters.append(
                Skater(
                    player['person']['firstName'],
                    player['person']['lastName'],
                    stats['goals'],
                    stats['assists'],
                    _parse_toi(stats['timeOnIce']),
                    stats['plusMinus'],
                    stats['shots'],
                    stats['hits'],
                    stats['penaltyMinutes'],
                    player['person']['nationality'],
                )
            )

        with suppress(KeyError):
            stats = player['stats']['goalieStats']

            goalies.append(
                Goalie(
                    player['person']['firstName'],
                    player['person']['lastName'],
                    stats['savePercentage'] / 100,
                    _parse_toi(stats['timeOnIce']),
                    stats['shots'],
                    player['person']['nationality'],
                )
            )

    return sorted(skaters), sorted(goalies)


def parse_schedule_upcoming(
    schedule: Mapping,
    timezone: str,
    from_h: int,
    to_h: int,
    fmt: str = '%d.%m. %H:%M',
) -> Iterable[Tuple[str, str, str]]:
    localizer = utils.dt_localizer(timezone)

    for game, _ in _parse_schedule_games(schedule, state_filter='Scheduled'):
        gamedate = datetime.strptime(game['gameDate'], '%Y-%m-%dT%H:%M:%SZ')
        local_datetime = localizer(gamedate)

        if from_h <= local_datetime.hour < to_h:
            home = game['teams']['home']['team']['name']
            away = game['teams']['away']['team']['name']

            yield (local_datetime.strftime(fmt), home, away)
