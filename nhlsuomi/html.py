from datetime import datetime
from typing import Iterable, Optional, Tuple

from jinja2 import Template

from nhlsuomi.data import Game


def render(template: str,
           games: Iterable[Game],
           highlights: Iterable[Tuple[str, str]],
           schedule: Iterable[Tuple[datetime, str, str]],
           timestamp: Optional[str] = None) -> str:

    html = Template(template).render(
        timestamp=timestamp or datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
        games=games,
        highlights=highlights,
        schedule=schedule
    )

    return '\n'.join(filter(None, (line.strip() for line in html.splitlines())))
