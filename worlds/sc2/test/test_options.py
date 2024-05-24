import unittest
from .test_base import Sc2TestBase
from .. import mission_tables, options

class TestOptions(unittest.TestCase):
    def test_campaign_size_option_max_matches_number_of_missions(self):
        self.assertEqual(options.MaximumCampaignSize.range_end, len(mission_tables.SC2Mission))
