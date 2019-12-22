import json
import pathlib
import unittest

from nhlsuomi.NHL import parser


class Test_nhl_parser(unittest.TestCase):
    def setUp(self):
        if not hasattr(self, 'games'):
            path = pathlib.Path(__file__).parent / 'games.json'
            self.games = json.loads(path.read_text())

    def test_parser(self):
        self.assertIsNotNone(self.games)

        games = parser.parse_games(self.games, '2019-11-22')
        expected = [
            {'away': {'score': 1, 'team': 'NJD'}, 'home': {'score': 4, 'team': 'PIT'}, 'id': 2019020346, 'status': 1},
            {'away': {'score': 1, 'team': 'NYR'}, 'home': {'score': 4, 'team': 'OTT'}, 'id': 2019020347, 'status': 1}
        ]

        self.assertCountEqual(games, expected)

        players, hilight_players = parser.parse_players(games, ['FIN'])
        expected_players = [
            {'status': 1, 'id': 2019020346, 'home': {'team': 'PIT', 'score': 4}, 'away': {'team': 'NJD', 'score': 1}, 'players': [{'first_name': 'Sami', 'last_name': 'Vatanen', 'nationality': 'FIN', 'toi': '19:51', 'shots': 7, 'hits': 0, 'plus_minus': -2, 'position': 'D', 'goals': 0, 'assists': 0, 'value': 2, 'sv': 0}], 'value': 1002},
            {'status': 1, 'id': 2019020347, 'home': {'team': 'OTT', 'score': 4}, 'away': {'team': 'NYR', 'score': 1}, 'players': [{'first_name': 'Kaapo', 'last_name': 'Kakko', 'nationality': 'FIN', 'toi': '15:20', 'shots': 2, 'hits': 0, 'plus_minus': 0, 'position': 'RW', 'goals': 0, 'assists': 0, 'value': 2, 'sv': 0}], 'value': 1002}
        ]
        expected_hilight_players = ['Kakko', 'Vatanen']
        self.assertEqual(players, expected_players)
        self.assertCountEqual(hilight_players, expected_hilight_players)
