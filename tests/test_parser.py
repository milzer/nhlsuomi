import unittest

from nhlsuomi.data import Game
from nhlsuomi.NHL.parser import (_parse_recap_url, parse_schedule_games,
                                 parse_schedule_highlights)
from tests.data import schedule


class TestParser(unittest.TestCase):
    def test_parse_games(self):
        expected_games = [
            Game(home_team='CBJ', home_score=2, away_team='TBL', away_score=5, final=True, gamecenter_id=2022020021, recap_url='https://wsczoominwestus.prod-cdn.clipro.tv/publish/7198093/11122224/9da0b7c8-bda5-4e35-9aee-271c83481534.mp4'),
            Game(home_team='DET', home_score=3, away_team='MTL', away_score=0, final=True, gamecenter_id=2022020022, recap_url='https://wsczoominwestus.prod-cdn.clipro.tv/publish/7197984/11121969/37d382a3-84f8-4a83-80a5-80adc943eae6.mp4'),
            Game(home_team='WPG', home_score=4, away_team='NYR', away_score=1, final=True, gamecenter_id=2022020023, recap_url='https://wsczoominwestus.prod-cdn.clipro.tv/publish/7199879/11127267/b40fd922-ae70-4491-915b-052d264e0c7f.mp4'),
            Game(home_team='SJS', home_score=1, away_team='CAR', away_score=2, final=True, gamecenter_id=2022020024, recap_url='https://wsczoominwestus.prod-cdn.clipro.tv/publish/7202248/11131522/9c937498-356a-4066-8cef-f86d76166e0d.mp4'),
        ]

        actual_games = list(parse_schedule_games(schedule))
        self.assertListEqual(actual_games, expected_games)


    def test_parse_recap_url(self):
        game = schedule['dates'][0]['games'][0]
        url = _parse_recap_url(game)
        self.assertEqual(url, 'https://wsczoominwestus.prod-cdn.clipro.tv/publish/7198093/11122224/9da0b7c8-bda5-4e35-9aee-271c83481534.mp4')

    def test_parse_all_highlights(self):
        actual_highlights = list(parse_schedule_highlights(schedule))
        self.assertEqual(len(actual_highlights), 21)

    def test_parse_keyword_highlights(self):
        expected_highlights = [
            ('TBL@CBJ: Perry scores PPG in 1st period', 'https://wsczoominwestus.prod-cdn.clipro.tv/editor/849ad95b-62b0-4c87-8bc8-2cd921945b37.mp4'),
            ('TBL@CBJ: Stamkos scores in 1st period', 'https://wsczoominwestus.prod-cdn.clipro.tv/editor/01bc71df-6839-4d32-98c7-c0107461f9b5.mp4'),
            ('TBL@CBJ: Stamkos deflects home his second goal', 'https://wsczoominwestus.prod-cdn.clipro.tv/editor/eb719f38-ee19-4f3f-95c2-ae48dc5ffd50.mp4'),
        ]
        actual_highlights = list(parse_schedule_highlights(schedule, {'perry', 'stamkos'}))
        self.assertListEqual(actual_highlights, expected_highlights)