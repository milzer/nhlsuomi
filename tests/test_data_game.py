import unittest

from nhlsuomi.data import Game, Player

game1 = Game('COL',  5, 'TBL',  0, True, 1, [
    Player('a', 0, 0, 0, 0, 0, 0, 0),
    Player('b', 0, 0, 0, 0, 0, 0, 0),
    Player('c', 0, 0, 0, 0, 0, 0, 0),
    Player('d', 0, 0, 0, 0, 0, 0, 0)
])

game2 = Game('COL',  5, 'TBL',  0, True, 2, [
    Player('e', 1, 0, 0, 0, 0, 0, 0),
    Player('f', 0, 1, 0, 0, 0, 0, 0),
    Player('g', 0, 0, 0, 0, 0, 0, 0)
])

game3 = Game('COL',  5, 'TBL',  0, True, 3, [
    Player('h', 3, 0, 0, 0, 0, 0, 0)
])

game4 = Game('COL',  5, 'TBL',  0, False, 4, [
    Player('i', 1, 0, 0, 0, 0, 0, 0),
    Player('j', 1, 0, 0, 0, 0, 0, 0),
    Player('k', 1, 0, 0, 0, 0, 0, 0),
    Player('l', 1, 0, 0, 0, 0, 0, 0),
])


class TestGameData(unittest.TestCase):
    def test_lt(self):
        self.assertLess(game1, game2)
        self.assertLess(game1, game3)
        self.assertLess(game3, game2)

    def test_ordering(self):
        games = [game1, game2, game3, game4]
        sorted_ids = [g.gamecenter_id for g in sorted(games, reverse=True)]
        self.assertListEqual(sorted_ids, [2, 3, 1, 4])
