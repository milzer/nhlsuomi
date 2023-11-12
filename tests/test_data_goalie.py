import unittest

from nhlsuomi.data import Goalie


class TestGoalieData(unittest.TestCase):
    def test_lt(self):
        g1 = Goalie('a', 'a', 0.99, 60 * 60, 15, 'FIN')
        g2 = Goalie('b', 'b', 0.89, 60 * 60, 15, 'FIN')
        self.assertLess(g1, g2)

        g1 = Goalie('a', 'a', 0.99, 35 * 60, 15, 'FIN')
        g2 = Goalie('b', 'b', 0.89, 60 * 60, 15, 'FIN')
        self.assertLess(g2, g1)

    def test_ordering(self):
        Goalies = [
            Goalie('a', 'a', 0.89, 60 * 60, 16, 'FIN'),
            Goalie('b', 'b', 0.95, 50 * 60, 17, 'FIN'),
            Goalie('c', 'c', 0.95, 59 * 60, 18, 'FIN'),
            Goalie('d', 'd', 1.00, 39 * 60, 10, 'FIN'),
        ]

        sorted_names = [p.last_name for p in sorted(Goalies)]

        self.assertListEqual(sorted_names, ['c', 'b', 'a', 'd'])

    def test_columns(self):
        g = Goalie('first', 'last', 0.8478, 3457, 15, 'FIN')
        self.assertEqual(g.columns, ('first', 'last', '84.8%', '57:37', 15))
