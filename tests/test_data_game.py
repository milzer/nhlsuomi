import unittest

from nhlsuomi.data import Game, Skater

game1 = Game('COL',  5, 'TBL',  0, True, 1, None, [
    Skater('a', 'a', 0, 0, 0, 0, 0, 0, 0, 'FIN'),
    Skater('b', 'b', 0, 0, 0, 0, 0, 0, 0, 'FIN'),
    Skater('c', 'c', 0, 0, 0, 0, 0, 0, 0, 'FIN'),
    Skater('d', 'd', 0, 0, 0, 0, 0, 0, 0, 'FIN'),
])

game2 = Game('COL',  5, 'TBL',  0, True, 2, None, [
    Skater('e', 'e', 1, 0, 0, 0, 0, 0, 0, 'FIN'),
    Skater('f', 'f', 0, 1, 0, 0, 0, 0, 0, 'FIN'),
    Skater('g', 'g', 0, 0, 0, 0, 0, 0, 0, 'FIN'),
])

game3 = Game('COL',  5, 'TBL',  0, True, 3, None, [
    Skater('h', 'h', 3, 0, 0, 0, 0, 0, 0, 'FIN'),
])

game4 = Game('COL',  5, 'TBL',  0, False, 4, None, [
    Skater('i', 'i', 1, 0, 0, 0, 0, 0, 0, 'FIN'),
    Skater('j', 'j', 1, 0, 0, 0, 0, 0, 0, 'FIN'),
    Skater('k', 'k', 1, 0, 0, 0, 0, 0, 0, 'FIN'),
    Skater('l', 'l', 1, 0, 0, 0, 0, 0, 0, 'FIN'),
])


class TestGameData(unittest.TestCase):
    def test_lt(self):
        self.assertLess(game2, game1)
        self.assertLess(game3, game1)
        self.assertLess(game2, game3)

    def test_ordering(self):
        games = [game1, game2, game3, game4]
        sorted_ids = [g.gamecenter_id for g in sorted(games)]
        self.assertListEqual(sorted_ids, [2, 3, 1, 4])
