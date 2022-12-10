from dataclasses import dataclass, field
from functools import total_ordering
from typing import List, Optional, Set, Tuple


def format_toi(seconds: int) -> str:
    m, s = divmod(seconds, 60)
    return f'{m:02d}:{s:02d}'


@total_ordering
@dataclass(eq=True)
class Skater:
    first_name: str
    last_name: str
    g: int
    a: int
    toi: int
    plusminus: int
    shots: int
    hits: int
    pim: int
    nationality: str

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
        if isinstance(other, Skater):
            return self.value() < other.value()
        else:
            return NotImplemented

    def value(self) -> Tuple[int, int, int, int, int, int, int, int]:
        return (
            -(self.g + self.a),
            -self.g,
            -self.a,
            -self.plusminus,
            -self.toi,
            -self.shots,
            -self.hits,
            -self.pim
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
    nationality: str

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
            not (self.toi > (40 * 60)),
            -int(self.spct * 1000),
            -self.shots
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
    skaters: List[Skater] = field(default_factory=list)
    goalies: List[Goalie] = field(default_factory=list)

    def __lt__(self, other) -> bool:
        if isinstance(other, Game):
            return self.value() < other.value()
        else:
            return NotImplemented

    def value(self) -> Tuple[bool, int, int, int, int]:
        goal_scorers = sum(skater.g > 0 for skater in self.skaters)

        points = [
            skater.g + skater.a
            for skater in self.skaters
            if (skater.g + skater.a) > 0
        ]

        return (
            not self.final,
            -goal_scorers,
            -len(points),
            -sum(points),
            -(len(self.skaters) + len(self.goalies))
        )

    @property
    def last_names(self) -> Set[str]:
        return {
            getattr(player, 'last_name')
            for player
            in (*self.skaters, *self.goalies)
        }
