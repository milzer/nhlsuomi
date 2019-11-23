import unittest

from nhlsuomi.NHL.utils import pluck


class Test_pluck(unittest.TestCase):
    def test_simple(self):
        d = {
            'a': 1,
            'b': 2
        }
        self.assertEqual(pluck(d, ('a')), 1)
        self.assertEqual(pluck(d, ('b')), 2)
        self.assertEqual(pluck(d, ('c')), None)

    def test_deep(self):
        d = {
            'a': {
                'b': {
                    'c': {
                        'd': {
                            'e': 1
                        }
                    }
                }
            }
        }

        self.assertEqual(pluck(d, ('a.b.c.d.e')), 1)
        self.assertEqual(pluck(d, ('a.b.c.d.e.f')), None)
        self.assertEqual(pluck(d, ('a.b.c.d')), {'e': 1})
        self.assertEqual(pluck(d, ('a.b.d.d.e')), None)
