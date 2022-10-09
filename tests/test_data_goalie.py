import unittest

from nhlsuomi.data import Goalie


class TestGoalieData(unittest.TestCase):
    def test_lt(self):
        g1 = Goalie('a', 'a', 0.99, 60 * 60, 15)
        g2 = Goalie('b', 'b', 0.89, 60 * 60, 15)
        self.assertLess(g2, g1)

        g1 = Goalie('a', 'a', 0.99, 35 * 60, 15)
        g2 = Goalie('b', 'b', 0.89, 60 * 60, 15)
        self.assertLess(g1, g2)

    def test_ordering(self):
        Goalies = [
            Goalie('a', 'a', 0.89, 60 * 60, 16),
            Goalie('b', 'b', 0.95, 50 * 60, 17),
            Goalie('c', 'c', 0.95, 59 * 60, 18),
            Goalie('d', 'd', 1.00, 39 * 60, 10)
        ]

        sorted_names = [p.last_name for p in sorted(Goalies, reverse=True)]

        self.assertListEqual(
            sorted_names,
            ['c', 'b', 'a', 'd']
        )

    def test_columns(self):
        g = Goalie('first', 'last', 0.8478, 3457, 15)
        self.assertEqual(
            g.columns,
            ('first', 'last', '84.8%', '57:37', 15)
        )
