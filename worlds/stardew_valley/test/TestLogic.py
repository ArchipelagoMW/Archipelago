import unittest

from test.general import setup_solo_multiworld
from .. import StardewValleyWorld, StardewLocation
from ..data.bundle_data import BundleItem, all_bundle_items_except_money
from ..stardew_rule import MISSING_ITEM, False_

multi_world = setup_solo_multiworld(StardewValleyWorld)
world = multi_world.worlds[1]
logic = world.logic


def collect_all(mw):
    for item in mw.get_items():
        mw.state.collect(item, event=True)


collect_all(multi_world)


class TestLogic(unittest.TestCase):
    def test_given_bundle_item_then_is_available_in_logic(self):
        for bundle_item in all_bundle_items_except_money:
            with self.subTest(msg=bundle_item.item.name):
                self.assertIn(bundle_item.item.name, logic.item_rules)

    def test_given_item_rule_then_can_be_resolved(self):
        for item in logic.item_rules.keys():
            with self.subTest(msg=item):
                rule = logic.item_rules[item]
                self.assertNotIn(MISSING_ITEM, repr(rule))
                self.assertTrue(rule == False_() or rule(multi_world.state), f"Could not resolve item rule for {item} {rule}")

    def test_given_building_rule_then_can_be_resolved(self):
        for building in logic.building_rules.keys():
            with self.subTest(msg=building):
                rule = logic.building_rules[building]
                self.assertNotIn(MISSING_ITEM, repr(rule))
                self.assertTrue(rule == False_() or rule(multi_world.state), f"Could not resolve building rule for {building} {rule}")

    def test_given_quest_rule_then_can_be_resolved(self):
        for quest in logic.quest_rules.keys():
            with self.subTest(msg=quest):
                rule = logic.quest_rules[quest]
                self.assertNotIn(MISSING_ITEM, repr(rule))
                self.assertTrue(rule == False_() or rule(multi_world.state), f"Could not resolve quest rule for {quest} {rule}")

    def test_given_special_order_rule_then_can_be_resolved(self):
        for special_order in logic.special_order_rules.keys():
            with self.subTest(msg=special_order):
                rule = logic.special_order_rules[special_order]
                self.assertNotIn(MISSING_ITEM, repr(rule))
                self.assertTrue(rule == False_() or rule(multi_world.state), f"Could not resolve special order rule for {special_order} {rule}")

    def test_given_tree_fruit_rule_then_can_be_resolved(self):
        for tree_fruit in logic.tree_fruit_rules.keys():
            with self.subTest(msg=tree_fruit):
                rule = logic.tree_fruit_rules[tree_fruit]
                self.assertNotIn(MISSING_ITEM, repr(rule))
                self.assertTrue(rule == False_() or rule(multi_world.state), f"Could not resolve tree fruit rule for {tree_fruit} {rule}")

    def test_given_seed_rule_then_can_be_resolved(self):
        for seed in logic.seed_rules.keys():
            with self.subTest(msg=seed):
                rule = logic.seed_rules[seed]
                self.assertNotIn(MISSING_ITEM, repr(rule))
                self.assertTrue(rule == False_() or rule(multi_world.state), f"Could not resolve seed rule for {seed} {rule}")

    def test_given_crop_rule_then_can_be_resolved(self):
        for crop in logic.crop_rules.keys():
            with self.subTest(msg=crop):
                rule = logic.crop_rules[crop]
                self.assertNotIn(MISSING_ITEM, repr(rule))
                self.assertTrue(rule == False_() or rule(multi_world.state), f"Could not resolve crop rule for {crop} {rule}")

    def test_given_fish_rule_then_can_be_resolved(self):
        for fish in logic.fish_rules.keys():
            with self.subTest(msg=fish):
                rule = logic.fish_rules[fish]
                self.assertNotIn(MISSING_ITEM, repr(rule))
                self.assertTrue(rule == False_() or rule(multi_world.state), f"Could not resolve fish rule for {fish} {rule}")

    def test_given_museum_rule_then_can_be_resolved(self):
        for donation in logic.museum_rules.keys():
            with self.subTest(msg=donation):
                rule = logic.museum_rules[donation]
                self.assertNotIn(MISSING_ITEM, repr(rule))
                self.assertTrue(rule == False_() or rule(multi_world.state), f"Could not resolve museum rule for {donation} {rule}")

    def test_given_cooking_rule_then_can_be_resolved(self):
        for cooking_rule in logic.cooking_rules.keys():
            with self.subTest(msg=cooking_rule):
                rule = logic.cooking_rules[cooking_rule]
                self.assertNotIn(MISSING_ITEM, repr(rule))
                self.assertTrue(rule == False_() or rule(multi_world.state), f"Could not resolve cooking rule for {cooking_rule} {rule}")

    def test_given_location_rule_then_can_be_resolved(self):
        for location in multi_world.get_locations(1):
            with self.subTest(msg=location.name):
                rule = location.access_rule
                self.assertNotIn(MISSING_ITEM, repr(rule))
                self.assertTrue(rule == False_() or rule(multi_world.state), f"Could not resolve location rule for {location} {rule}")
