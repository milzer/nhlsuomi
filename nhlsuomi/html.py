from datetime import datetime
from typing import Iterable, Optional, Tuple

from jinja2 import Template

from nhlsuomi.data import Game, Skater


def render(
    template: str,
    games: Iterable[Game],
    skater_highlights: Iterable[Skater],
    schedule: Iterable[Tuple[str, str, str]],
    timestamp: Optional[str] = None,
) -> str:
    html = Template(template).render(
        timestamp=timestamp or datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
        games=games,
        highlight_skaters=skater_highlights,
        schedule=schedule,
    )

    return '\n'.join(
        filter(None, (line.strip() for line in html.splitlines()))
    )
