from __future__ import annotations

import pathlib
from dataclasses import dataclass, field

import yaml

from nhlsuomi.logging import logger


@dataclass(eq=False)
class Config:
    template: str = 'template.html'
    output: str = 'output.html'
    jsondump: str | None = None
    nationalities: set[str] = field(default_factory=set)
    date_offset: int = -1
    schedule_days: int = 21
    schedule_timezone: str = 'Europe/Helsinki'
    schedule_datetime_format: str = '%d.%m. %H:%M'
    schedule_hours_from: int = 6
    schedule_hours_to: int = 23
    refresh_minutes: int = 20
    quit_minutes: int = 360

    @staticmethod
    def load(config_path: pathlib.Path) -> Config:
        logger.info(f'Load config from {config_path.resolve()}')
        loaded_values = yaml.safe_load(config_path.read_text()) or {}
        return Config(**loaded_values)
