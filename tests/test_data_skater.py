import unittest

from nhlsuomi.data import Skater


class TestPlayerData(unittest.TestCase):
    def test_lt(self):
        p1 = Skater('1g', '1g',1, 0, 0, 0, 0, 0, 0, 'FIN')
        p2 = Skater('1a', '1a', 0, 1, 0, 0, 0, 0, 0, 'FIN')
        self.assertLess(p2, p1)

    def test_ordering(self):
        players = [
            Skater('g', 'g', 1, 0, 0, 0, 0, 0, 0, 'FIN'),
            Skater('a', 'a', 0, 1, 0, 0, 0, 0, 0, 'FIN'),
            Skater('ga', 'ga', 1, 1, 0, 0, 0, 0, 0, 'FIN'),
            Skater('2g', '2g', 2, 0, 0, 0, 0, 0, 0, 'FIN'),
            Skater('pim', 'pim', 0, 0, 0, 0, 0, 0, 1, 'FIN'),
            Skater('hits', 'hits', 0, 0, 0, 0, 0, 1, 0, 'FIN'),
            Skater('shots', 'shots', 0, 0, 0, 0, 1, 0, 0, 'FIN'),
            Skater('plusminus', 'plusminus', 0, 0, 0, 1, 0, 0, 0, 'FIN'),
            Skater('toi', 'toi', 0, 0, 1, 0, 0, 0, 0, 'FIN'),
        ]

        sorted_names = [p.last_name for p in sorted(players, reverse=True)]

        self.assertListEqual(
            sorted_names,
            ['2g', 'ga', 'g', 'a', 'plusminus', 'toi', 'shots', 'hits', 'pim']
        )

    def test_columns(self):
        p1 = Skater('player', 'player', 1, 1, 1043, -1, 7, 6, 10, 'FIN')
        self.assertEqual(
            p1.columns,
            ('player', 'player', '1+1', '17:23', -1, 7, 6, 10)
        )
