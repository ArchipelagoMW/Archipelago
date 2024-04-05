import unittest

from .. import MissionTables, Options


class TestOptions(unittest.TestCase):
    def test_campaign_size_option_max_matches_number_of_missions(self):
        self.assertEqual(Options.MaximumCampaignSize.range_end, len(MissionTables.SC2Mission))
