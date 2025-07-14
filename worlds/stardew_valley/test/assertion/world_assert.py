from typing import List
from unittest import TestCase

from BaseClasses import MultiWorld, ItemClassification
from .rule_assert import RuleAssertMixin
from ... import StardewItem
from ...items import items_by_group, Group
from ...locations import LocationTags, locations_by_tag


def get_all_item_names(multiworld: MultiWorld) -> List[str]:
    return [item.name for item in multiworld.itempool]


def get_all_location_names(multiworld: MultiWorld) -> List[str]:
    return [location.name for location in multiworld.get_locations() if location.address is not None]


class WorldAssertMixin(RuleAssertMixin, TestCase):

    def assert_victory_exists(self, multiworld: MultiWorld):
        self.assertIn(StardewItem("Victory", ItemClassification.progression, None, 1), multiworld.get_items())

    def assert_can_reach_victory(self, multiworld: MultiWorld):
        victory = multiworld.find_item("Victory", 1)
        self.assert_rule_true(victory.access_rule, multiworld.state)

    def assert_cannot_reach_victory(self, multiworld: MultiWorld):
        victory = multiworld.find_item("Victory", 1)
        self.assert_rule_false(victory.access_rule, multiworld.state)

    def assert_item_was_necessary_for_victory(self, item: StardewItem, multiworld: MultiWorld):
        self.assert_can_reach_victory(multiworld)
        multiworld.state.remove(item)
        self.assert_cannot_reach_victory(multiworld)
        multiworld.state.collect(item, prevent_sweep=False)
        self.assert_can_reach_victory(multiworld)

    def assert_item_was_not_necessary_for_victory(self, item: StardewItem, multiworld: MultiWorld):
        self.assert_can_reach_victory(multiworld)
        multiworld.state.remove(item)
        self.assert_can_reach_victory(multiworld)
        multiworld.state.collect(item, prevent_sweep=False)
        self.assert_can_reach_victory(multiworld)

    def assert_can_win(self, multiworld: MultiWorld):
        self.assert_victory_exists(multiworld)
        self.assert_can_reach_victory(multiworld)

    def assert_same_number_items_locations(self, multiworld: MultiWorld):
        non_event_locations = [location for location in multiworld.get_locations() if location.address is not None]
        self.assertEqual(len(multiworld.itempool), len(non_event_locations))

    def assert_can_reach_everything(self, multiworld: MultiWorld):
        for location in multiworld.get_locations():
            self.assert_can_reach_location(location, multiworld.state)

    def assert_basic_checks(self, multiworld: MultiWorld):
        self.assert_same_number_items_locations(multiworld)
        non_event_items = [item for item in multiworld.get_items() if item.code]
        for item in non_event_items:
            multiworld.state.collect(item)
        self.assert_can_win(multiworld)
        self.assert_can_reach_everything(multiworld)

    def assert_basic_checks_with_subtests(self, multiworld: MultiWorld):
        with self.subTest("same_number_items_locations"):
            self.assert_same_number_items_locations(multiworld)
        non_event_items = [item for item in multiworld.get_items() if item.code]
        for item in non_event_items:
            multiworld.state.collect(item)
        with self.subTest("can_win"):
            self.assert_can_win(multiworld)
        with self.subTest("can_reach_everything"):
            self.assert_can_reach_everything(multiworld)

    def assert_no_ginger_island_content(self, multiworld: MultiWorld):
        ginger_island_items = [item_data.name for item_data in items_by_group[Group.GINGER_ISLAND]]
        ginger_island_locations = [location_data.name for location_data in locations_by_tag[LocationTags.GINGER_ISLAND]]
        for item in multiworld.get_items():
            self.assertNotIn(item.name, ginger_island_items)
        for location in multiworld.get_locations():
            self.assertNotIn(location.name, ginger_island_locations)
