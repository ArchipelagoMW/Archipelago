import unittest

from test.general import setup_solo_multiworld
from .. import StardewValleyWorld
from ..bundle_data import all_bundle_items_except_money
from ..logic import MISSING_ITEM, _False


class TestAllLogicalItem(unittest.TestCase):
    multi_world = setup_solo_multiworld(StardewValleyWorld)
    world = multi_world.worlds[1]
    logic = world.logic

    def setUp(self) -> None:
        for item in self.multi_world.get_items():
            self.multi_world.state.collect(item, event=True)

    def test_given_bundle_item_then_is_available_in_logic(self):
        for bundle_item in all_bundle_items_except_money:
            with self.subTest(bundle_item=bundle_item):
                assert bundle_item.item.name in self.logic.item_rules

    def test_given_item_rule_then_can_be_resolved(self):
        for item in self.logic.item_rules.keys():
            with self.subTest(item=item):
                rule = self.logic.item_rules[item]

                assert MISSING_ITEM not in repr(rule)
                assert rule == _False() or rule(self.multi_world.state), f"Could not resolve rule for {item} {rule}"

    def test_given_building_rule_then_can_be_resolved(self):
        for item in self.logic.building_rules.keys():
            with self.subTest(item=item):
                rule = self.logic.building_rules[item]

                assert MISSING_ITEM not in repr(rule)
                assert rule == _False() or rule(self.multi_world.state), f"Could not resolve rule for {item} {rule}"

    def test_given_quest_rule_then_can_be_resolved(self):
        for item in self.logic.quest_rules.keys():
            with self.subTest(item=item):
                rule = self.logic.quest_rules[item]

                assert MISSING_ITEM not in repr(rule)
                assert rule == _False() or rule(self.multi_world.state), f"Could not resolve rule for {item} {rule}"

    def test_given_location_rule_then_can_be_resolved(self):
        for location in self.multi_world.get_locations(1):
            with self.subTest(location=location):
                rule = location.access_rule

                assert MISSING_ITEM not in repr(rule)
                assert rule == _False() or rule(self.multi_world.state), f"Could not resolve rule for {location} {rule}"
