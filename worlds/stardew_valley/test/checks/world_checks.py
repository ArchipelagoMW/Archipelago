from typing import List

from BaseClasses import MultiWorld, ItemClassification
from ... import StardewItem
from .. import SVTestBase


def get_all_item_names(multiworld: MultiWorld) -> List[str]:
    return [item.name for item in multiworld.itempool]


def get_all_location_names(multiworld: MultiWorld) -> List[str]:
    return [location.name for location in multiworld.get_locations() if not location.event]


def assert_victory_exists(tester: SVTestBase, multiworld: MultiWorld):
    tester.assertIn(StardewItem("Victory", ItemClassification.progression, None, 1), multiworld.get_items())


def collect_all_then_assert_can_win(tester: SVTestBase, multiworld: MultiWorld):
    for item in multiworld.get_items():
        multiworld.state.collect(item)
    tester.assertTrue(multiworld.find_item("Victory", 1).can_reach(multiworld.state))


def assert_can_win(tester: SVTestBase, multiworld: MultiWorld):
    assert_victory_exists(tester, multiworld)
    collect_all_then_assert_can_win(tester, multiworld)


def assert_same_number_items_locations(tester: SVTestBase, multiworld: MultiWorld):
    non_event_locations = [location for location in multiworld.get_locations() if not location.event]
    tester.assertEqual(len(multiworld.itempool), len(non_event_locations))