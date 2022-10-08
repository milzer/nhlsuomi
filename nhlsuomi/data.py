from dataclasses import dataclass, field
from functools import total_ordering
from typing import List, Optional, Tuple


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
    def columns(self):
        points = f'{self.g}+{self.a}'

        toi_m, toi_s = divmod(self.toi, 60)
        toi = f'{toi_m:02d}:{toi_s:02d}'

        return (
            self.first_name,
            self.last_name,
            points,
            toi,
            self.plusminus,
            self.shots,
            self.hits,
            self.pim
        )

    def __lt__(self, other) -> bool:
        if isinstance(other, Player):
            return self._value < other._value
        else:
            return NotImplemented

    @property
    def _value(self) -> Tuple:
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
class Game:
    home_team: str
    home_score: int
    away_team: str
    away_score: int
    final: bool
    gamecenter_id: int
    players: List[Player] = field(default_factory=list)
    type: Optional[str] = None  # if something else than regular/playoff
    recap_url: Optional[str] = None

    def __lt__(self, other) -> bool:
        if isinstance(other, Game):
            return self._value < other._value
        else:
            return NotImplemented

    @property
    def _value(self) -> Tuple[bool, int, int, int]:
        points = [
            p.g + p.a
            for p in self.players
            if (p.g + p.a) > 0
        ]

        return (
            self.final,
            len(points),
            sum(points),
            len(self.players)
        )
