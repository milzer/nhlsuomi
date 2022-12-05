import unittest
from datetime import datetime

from nhlsuomi import utils


class TestUtils(unittest.TestCase):
    def test_dt_localizer(self):
        localizer = utils.dt_localizer('Europe/Helsinki')
        utc_datetime = datetime(2022, 12, 1, 23)
        hki_datetime = localizer(utc_datetime)
        self.assertEqual(hki_datetime.day, 2)
        self.assertEqual(hki_datetime.hour, 1)
