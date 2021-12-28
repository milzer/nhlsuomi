import unittest

from nhlsuomi.config import ConfigData, RedditData, ScheduleData


class Test_config(unittest.TestCase):
    def test_defaults(self):
        config = ConfigData()
        assert config.reddit == RedditData()
        assert config.schedule == ScheduleData()
        assert config.hilights_enabled == False
        assert config.schedule_enabled == False

    def test_init_unknown_keys(self):
        with self.assertRaises(ValueError):
            config = ConfigData({'foo': 'bar'})

    def test_hilights(self):
        redditdata = {
            'client_id': 'id',
            'client_secret': 'secret'
        }
        config = ConfigData({
            'reddit': redditdata,
            'hilight_keywords': ['word'],
            'hilights_age_limit': 18
        })
        assert config.reddit == RedditData(**redditdata)
        assert config.hilights_enabled == True

    def test_schedule(self):
        scheduledata = {
            'days': 7,
            'timezone': 'Europe/Tallinn',
            'dt_format': '%H:%M - %d.%m.',
            'hours': [5, 22]
        }
        config = ConfigData({'schedule': scheduledata})
        assert config.schedule_enabled == True
        config.schedule.days = 0
        assert config.schedule_enabled == False
