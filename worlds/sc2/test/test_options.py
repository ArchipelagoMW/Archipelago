import unittest
from typing import Set, Dict, List

from .test_base import Sc2TestBase
from .. import mission_tables, options, items


class TestOptions(unittest.TestCase):
    def test_campaign_size_option_max_matches_number_of_missions(self) -> None:
        self.assertEqual(options.MaximumCampaignSize.range_end, len(mission_tables.SC2Mission))

    def test_unit_max_upgrades_matching_items(self) -> None:
        base_items: Set[str] = {
            items.get_full_item_list()[item].parent_item for item in items.get_full_item_list()
            if items.get_full_item_list()[item].parent_item is not None
        }

        upgrade_items: Dict[str, List[str]] = dict()
        for item in base_items:
            upgrade_items[item] = [
                upgrade_item for upgrade_item in items.get_full_item_list()
                if items.get_full_item_list()[upgrade_item].parent_item == item
            ]
        upgrade_counter: List[int] = list()
        for item in base_items:
            quantities: List[int] = [items.get_full_item_list()[upgrade_item].quantity for upgrade_item in upgrade_items[item]]
            upgrade_counter.append(sum(quantities))

        self.assertEqual(options.MAX_UPGRADES_OPTION, max(upgrade_counter))
