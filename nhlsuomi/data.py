from dataclasses import dataclass, field
from functools import total_ordering
from typing import Any, List, Optional, Tuple


@total_ordering
@dataclass(eq=False)
class Player:
    name: str
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
            self.name,
            points,
            toi,
            self.plusminus,
            self.shots,
            self.hits,
            self.pim
        )

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Player):
            return self._value == other._value
        else:
            return NotImplemented

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


@total_ordering
@dataclass(eq=False)
class Game:
    home_team: str
    home_score: int
    away_team: str
    away_score: int
    type: str
    gamecenter_id: str
    recap_url: Optional[str] = None
    players: List[Player] = field(default_factory=list)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Game):
            return self._value == other._value
        else:
            return NotImplemented

    def __lt__(self, other) -> bool:
        if isinstance(other, Game):
            return self._value < other._value
        else:
            return NotImplemented

    @property
    def _value(self) -> Tuple[int, int, int]:
        points = [
            (p.g, p.a)
            for p in self.players
            if (p.g + p.a) > 0
        ]

        return (
            len(points),  # number of scorers
            sum(g + a for g, a in points),  # total points
            len(self.players)
        )
