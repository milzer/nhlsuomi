from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, IntEnum
from typing import Mapping

from nhlsuomi.NHL import utils


class GameStatus(IntEnum):
    SCHEDULED = 0
    IN_PROGRESS = 1
    FINAL = 2
    POSTPONED = 3

    @staticmethod
    def parse_statuscode(statuscode: str) -> GameStatus:
        if statuscode in {'1', '2', '8'}:
            return GameStatus.SCHEDULED
        elif statuscode in {'3', '4', '5', '6'}:
            return GameStatus.IN_PROGRESS
        elif statuscode == '9':
            return GameStatus.POSTPONED
        elif statuscode == '7':
            return GameStatus.FINAL

        raise ValueError(f'Invalid game statuscode: {statuscode}')


class GameType(Enum):
    REGULAR = 'R'
    PLAYOFF = 'P'
    PRESEASON = 'PR'
    ALLSTAR = 'A'


@dataclass
class Game:
    status: GameStatus
    id: int
    type: GameType
    home_team: str
    home_score: int
    away_team: str
    away_score: int

    @classmethod
    def from_dict(cls, game: Mapping) -> Game:
        return Game(
            GameStatus.parse_statuscode(utils.pluck(game, 'status.statusCode')),
            game['gamePk'],
            GameType(game['gameType']),
            utils.pluck(game, 'teams.home.team.abbreviation', '???'),
            utils.pluck(game, 'teams.home.score'),
            utils.pluck(game, 'teams.away.team.abbreviation', '???'),
            utils.pluck(game, 'teams.away.score')
        )
