import unittest

from nhlsuomi.data import Player


class TestPlayerData(unittest.TestCase):
    def test_eq(self):
        p1 = Player('a', 1, 1, 25, -1, 1, 1, 2)
        p2 = Player('b', 1, 1, 25, -1, 1, 1, 2)
        p3 = Player('a', 2,0, 10, -1, 1, 1, 2)
        self.assertTrue(p1 == p2)
        self.assertFalse(p1 == p3)
        self.assertFalse(p2 == p3)

    def test_lt(self):
        p1 = Player('1g', 1, 0, 0, 0, 0, 0, 0)
        p2 = Player('1a', 0, 1, 0, 0, 0, 0, 0)
        self.assertTrue(p1 > p2)

    def test_ordering(self):
        players = [
            Player('g', 1, 0, 0, 0, 0, 0, 0),
            Player('a', 0, 1, 0, 0, 0, 0, 0),
            Player('ga', 1, 1, 0, 0, 0, 0, 0),
            Player('2g', 2, 0, 0, 0, 0, 0, 0),
            Player('pim', 0, 0, 0, 0, 0, 0, 1),
            Player('hits', 0, 0, 0, 0, 0, 1, 0),
            Player('shots', 0, 0, 0, 0, 1, 0, 0),
            Player('plusminus', 0, 0, 0, 1, 0, 0, 0),
            Player('toi', 0, 0, 1, 0, 0, 0, 0)
        ]

        sorted_names = [p.name for p in sorted(players, reverse=True)]

        self.assertListEqual(
            sorted_names,
            ['2g', 'ga', 'g', 'a', 'plusminus', 'toi', 'shots', 'hits', 'pim']
        )

    def test_columns(self):
        p1 = Player('player', 1, 1, 1043, -1, 7, 6, 10)
        self.assertEqual(
            p1.columns,
            ('player', '1+1', '17:23', -1, 7, 6, 10)
        )
