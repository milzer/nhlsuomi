import unittest

from nhlsuomi.data import Player


class TestPlayerData(unittest.TestCase):
    def test_lt(self):
        p1 = Player('1g', '1g',1, 0, 0, 0, 0, 0, 0)
        p2 = Player('1a', '1a', 0, 1, 0, 0, 0, 0, 0)
        self.assertLess(p2, p1)

    def test_ordering(self):
        players = [
            Player('g', 'g', 1, 0, 0, 0, 0, 0, 0),
            Player('a', 'a', 0, 1, 0, 0, 0, 0, 0),
            Player('ga', 'ga', 1, 1, 0, 0, 0, 0, 0),
            Player('2g', '2g', 2, 0, 0, 0, 0, 0, 0),
            Player('pim', 'pim', 0, 0, 0, 0, 0, 0, 1),
            Player('hits', 'hits', 0, 0, 0, 0, 0, 1, 0),
            Player('shots', 'shots', 0, 0, 0, 0, 1, 0, 0),
            Player('plusminus', 'plusminus', 0, 0, 0, 1, 0, 0, 0),
            Player('toi', 'toi', 0, 0, 1, 0, 0, 0, 0)
        ]

        sorted_names = [p.last_name for p in sorted(players, reverse=True)]

        self.assertListEqual(
            sorted_names,
            ['2g', 'ga', 'g', 'a', 'plusminus', 'toi', 'shots', 'hits', 'pim']
        )

    def test_columns(self):
        p1 = Player('player', 'player', 1, 1, 1043, -1, 7, 6, 10)
        self.assertEqual(
            p1.columns,
            ('player', 'player', '1+1', '17:23', -1, 7, 6, 10)
        )
