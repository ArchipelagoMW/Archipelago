import unittest
from .test_base import Sc2TestBase
from .. import Options, MissionTables

class TestOptions(unittest.TestCase):
    def test_campaign_size_option_max_matches_number_of_missions(self):
        self.assertEqual(Options.MaximumCampaignSize.range_end, len(MissionTables.SC2Mission))
