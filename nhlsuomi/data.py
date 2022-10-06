from dataclasses import dataclass
from functools import total_ordering
from typing import Any, Tuple


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

    def __lt__(self, other):
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
