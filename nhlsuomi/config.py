from dataclasses import InitVar, astuple, dataclass, field
from typing import List, Mapping, Union


@dataclass
class RedditData:
    client_id: str = ''
    client_secret: str = ''


@dataclass
class ScheduleData:
    days: int = 0
    timezone: str = 'Europe/Helsinki'
    dt_format: str = '%d.%m. %H:%M'
    hours: List[int] = field(default_factory=lambda: [6, 23])


@dataclass
class ConfigData:
    data: InitVar[Mapping] = {}
    loglevel: Union[str, int] = 'INFO'
    nationalities: List[str] = field(default_factory=list)
    min_goals: int = 3
    min_points: int = 5
    template: str = 'template.html'
    output: str = 'nhl.html'
    hilights_age_limit: int = 0
    hilight_keywords: List[str] = field(default_factory=list)
    reddit: RedditData = field(default_factory=RedditData)
    schedule: ScheduleData = field(default_factory=ScheduleData)

    def __post_init__(self, data: Mapping):
        for key, value in data.items():
            if hasattr(self, key):
                if key == 'reddit':
                    setattr(self, key, RedditData(**value))
                elif key == 'schedule':
                    setattr(self, key, ScheduleData(**value))
                else:
                    setattr(self, key, value)
            else:
                raise ValueError(f'Invalid config key: {key}')

    @property
    def hilights_enabled(self):
        return all((
            *astuple(self.reddit),
            int(self.hilights_age_limit) > 0,
            isinstance(self.hilight_keywords, List),
            len(self.hilight_keywords) > 0
        ))

    @property
    def schedule_enabled(self):
        return all((
            *astuple(self.schedule),
            int(self.schedule.days) > 0,
            isinstance(self.schedule.hours, List),
            len(self.schedule.hours) == 2
        ))
