import json
import pathlib
import unittest
from collections import OrderedDict
from datetime import datetime

from nhlsuomi.reddit import icydata


class Test_icydata(unittest.TestCase):
    def setUp(self):
        if not hasattr(self, 'submissions'):
            path = pathlib.Path(__file__).parent / 'icydata.json'
            self.submissions = json.loads(path.read_text())

    def test_hilights(self):
        self.assertIsNotNone(self.submissions)

        keywords = ['Laine', 'Korpisalo']
        hilights, _ = icydata.parse_hilights_recaps(self.submissions, keywords, 18,
                                                    _now=lambda: datetime(2019, 11, 23))
        expected = [
            ('Laine scores goal', 'https://wscdsszoominwestus.azureedge.net/publish/d663e54d-db5e-4c7d-b3d8-9a0b548aebd4.mp4'),
            ('Korpisalo makes save', 'https://wscdsszoominwestus.azureedge.net/publish/6efb1f8b-0e2d-498a-aaae-839980d3139c.mp4'),
            ('Ristolainen scores PPG', 'https://wscdsszoominwestus.azureedge.net/publish/4a64f0f7-c9cf-4e2c-acef-57439a4bcd71.mp4')
        ]
        self.assertEqual(hilights, expected)

    def test_no_hilights(self):
        self.assertIsNotNone(self.submissions)

        keywords = ['Laine', 'Korpisalo']
        hilights, _ = icydata.parse_hilights_recaps(self.submissions, keywords, 18,
                                                    _now=lambda: datetime(2019, 11, 24))
        expected = []
        self.assertEqual(hilights, expected)

    def test_recaps(self):
        self.assertIsNotNone(self.submissions)

        _, recaps = icydata.parse_hilights_recaps(self.submissions[:2], [], 18)
        expected = OrderedDict()
        expected['PITNJD'] = 'https://hlslive-wsczoominwestus.med.nhl.com/publish/056ae7ef-ac8a-4597-9e2a-caeedfbec847.mp4'
        expected['OTTNYR'] = 'https://hlslive-wsczoominwestus.med.nhl.com/publish/b00a68fd-caac-40e7-a232-50b72fefb70a.mp4'
        self.assertEqual(recaps, expected)
