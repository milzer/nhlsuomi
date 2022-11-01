from dataclasses import dataclass, field
from functools import total_ordering
from typing import List, Optional, Tuple


def format_toi(seconds: int) -> str:
    m, s = divmod(seconds, 60)
    return f'{m:02d}:{s:02d}'


@total_ordering
@dataclass(eq=True)
class Player:
    first_name: str
    last_name: str
    g: int
    a: int
    toi: int
    plusminus: int
    shots: int
    hits: int
    pim: int

    @property
    def columns(self) -> Tuple[str, str, str, str, int, int, int, int]:
        return (
            self.first_name,
            self.last_name,
            f'{self.g}+{self.a}',
            format_toi(self.toi),
            self.plusminus,
            self.shots,
            self.hits,
            self.pim
        )

    def __lt__(self, other) -> bool:
        if isinstance(other, Player):
            return self.value() < other.value()
        else:
            return NotImplemented

    def value(self) -> Tuple[int, int, int, int, int, int, int, int]:
        return (
            self.g + self.a,
            self.g,
            self.a,
            self.plusminus,
            self.toi,
            self.shots,
            self.hits,
            self.pim
        )

    @property
    def binoculars(self) -> bool:
        return (self.g + self.a) == 0


@total_ordering
@dataclass(eq=True)
class Goalie:
    first_name: str
    last_name: str
    spct: float
    toi: int
    shots: int

    @property
    def columns(self) -> Tuple[str, str, str, str, int]:
        return (
            self.first_name,
            self.last_name,
            f'{self.spct:.1%}',
            format_toi(self.toi),
            self.shots
        )

    def __lt__(self, other) -> bool:
        if isinstance(other, Goalie):
            return self.value() < other.value()
        else:
            return NotImplemented

    def value(self) -> Tuple[bool, int, int]:
        return (
            self.toi > 40 * 60,
            int(self.spct * 1000),
            self.shots
        )


@total_ordering
@dataclass(eq=True)
class Game:
    home_team: str
    home_score: int
    away_team: str
    away_score: int
    final: bool
    gamecenter_id: int
    recap_url: Optional[str] = None
    players: List[Player] = field(default_factory=list)
    goalies: List[Goalie] = field(default_factory=list)

    def __lt__(self, other) -> bool:
        if isinstance(other, Game):
            return self.value() < other.value()
        else:
            return NotImplemented

    def value(self) -> Tuple[bool, int, int, int]:
        points = [
            p.g + p.a
            for p in self.players
            if (p.g + p.a) > 0
        ]

        return (
            self.final,
            len(points),
            sum(points),
            len(self.players) + len(self.goalies)
        )
