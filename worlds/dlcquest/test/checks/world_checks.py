from typing import List

from BaseClasses import MultiWorld
from .. import DLCQuestTestBase
from ... import Options


def get_all_item_names(multiworld: MultiWorld) -> List[str]:
    return [item.name for item in multiworld.itempool]


def get_all_location_names(multiworld: MultiWorld) -> List[str]:
    return [location.name for location in multiworld.get_locations() if not location.advancement]


def assert_victory_exists(tester: DLCQuestTestBase, multiworld: MultiWorld):
    campaign = multiworld.worlds[1].options.campaign
    all_items = [item.name for item in multiworld.get_items()]
    if campaign == Options.Campaign.option_basic or campaign == Options.Campaign.option_both:
        tester.assertIn("Victory Basic", all_items)
    if campaign == Options.Campaign.option_live_freemium_or_die or campaign == Options.Campaign.option_both:
        tester.assertIn("Victory Freemium", all_items)


def collect_all_then_assert_can_win(tester: DLCQuestTestBase, multiworld: MultiWorld):
    for item in multiworld.get_items():
        multiworld.state.collect(item)
    campaign = multiworld.worlds[1].options.campaign
    if campaign == Options.Campaign.option_basic or campaign == Options.Campaign.option_both:
        tester.assertTrue(multiworld.find_item("Victory Basic", 1).can_reach(multiworld.state))
    if campaign == Options.Campaign.option_live_freemium_or_die or campaign == Options.Campaign.option_both:
        tester.assertTrue(multiworld.find_item("Victory Freemium", 1).can_reach(multiworld.state))


def assert_can_win(tester: DLCQuestTestBase, multiworld: MultiWorld):
    assert_victory_exists(tester, multiworld)
    collect_all_then_assert_can_win(tester, multiworld)


def assert_same_number_items_locations(tester: DLCQuestTestBase, multiworld: MultiWorld):
    non_event_locations = [location for location in multiworld.get_locations() if not location.advancement]
    tester.assertEqual(len(multiworld.itempool), len(non_event_locations))
