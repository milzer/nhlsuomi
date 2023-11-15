# pylint: disable=protected-access,line-too-long
import unittest

from nhlsuomi.data import Game, Goalie, Skater
from nhlsuomi.nhl import parser
from tests import data


class TestParser(unittest.TestCase):
    def test_parse_games(self):
        expected_games = [
            Game(
                home_team='CBJ',
                home_score=2,
                away_team='TBL',
                away_score=5,
                final=True,
                gamecenter_id=2022020021,
                recap_url=None,
            ),
            Game(
                home_team='DET',
                home_score=3,
                away_team='MTL',
                away_score=0,
                final=True,
                gamecenter_id=2022020022,
                recap_url=None,
            ),
            Game(
                home_team='WPG',
                home_score=4,
                away_team='NYR',
                away_score=1,
                final=True,
                gamecenter_id=2022020023,
                recap_url=None,
            ),
            Game(
                home_team='SJS',
                home_score=1,
                away_team='CAR',
                away_score=2,
                final=True,
                gamecenter_id=2022020024,
                recap_url=None,
            ),
        ]

        actual_games = list(parser.parse_schedule_games(data.schedule))
        self.assertListEqual(actual_games, expected_games)

    def test_parse_toi(self):
        self.assertEqual(parser._parse_toi('0:0'), 0)
        self.assertEqual(parser._parse_toi('12:34'), 754)
        self.assertEqual(parser._parse_toi('100:1'), 6001)

    def test_parse_boxscore_players(self):
        skaters, goalies = parser.parse_boxscore_players(data.boxscore)

        self.assertEqual(len(skaters), 36)
        self.assertEqual(
            skaters[0],
            Skater(
                first_name='Nathan',
                last_name='MacKinnon',
                g=2,
                a=3,
                toi=1509,
                plusminus=1,
                shots=8,
                hits=0,
                pim=2,
                nationality='CAN',
            ),
        )
        self.assertEqual(skaters[-1].last_name, 'Megna')

        self.assertEqual(len(goalies), 2)
        self.assertEqual(
            goalies[0],
            Goalie(
                first_name='Alexandar',
                last_name='Georgiev',
                spct=0.8571428571428571,
                toi=3600,
                shots=28,
                nationality='RUS',
            ),
        )
        self.assertEqual(goalies[1].last_name, 'Luukkonen')

    def test_parse_upcoming(self):
        result = list(
            parser.parse_schedule_upcoming(
                data.upcoming_schedule, 'Europe/Helsinki', 18, 22
            )
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(
            result[0], ('03.12. 21:00', 'Minnesota Wild', 'Anaheim Ducks')
        )
