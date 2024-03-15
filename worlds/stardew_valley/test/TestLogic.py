from unittest import TestCase

from . import setup_solo_multiworld, allsanity_options_with_mods
from .assertion import RuleAssertMixin
from ..data.bundle_data import all_bundle_items_except_money

multi_world = setup_solo_multiworld(allsanity_options_with_mods(), _cache={})
world = multi_world.worlds[1]
logic = world.logic


def collect_all(mw):
    for item in mw.get_items():
        mw.state.collect(item, event=True)


collect_all(multi_world)


class TestLogic(RuleAssertMixin, TestCase):
    def test_given_bundle_item_then_is_available_in_logic(self):
        for bundle_item in all_bundle_items_except_money:
            with self.subTest(msg=bundle_item.item_name):
                self.assertIn(bundle_item.item_name, logic.registry.item_rules)

    def test_given_item_rule_then_can_be_resolved(self):
        for item in logic.registry.item_rules.keys():
            with self.subTest(msg=item):
                rule = logic.registry.item_rules[item]
                self.assert_rule_can_be_resolved(rule, multi_world.state)

    def test_given_building_rule_then_can_be_resolved(self):
        for building in logic.registry.building_rules.keys():
            with self.subTest(msg=building):
                rule = logic.registry.building_rules[building]
                self.assert_rule_can_be_resolved(rule, multi_world.state)

    def test_given_quest_rule_then_can_be_resolved(self):
        for quest in logic.registry.quest_rules.keys():
            with self.subTest(msg=quest):
                rule = logic.registry.quest_rules[quest]
                self.assert_rule_can_be_resolved(rule, multi_world.state)

    def test_given_special_order_rule_then_can_be_resolved(self):
        for special_order in logic.registry.special_order_rules.keys():
            with self.subTest(msg=special_order):
                rule = logic.registry.special_order_rules[special_order]
                self.assert_rule_can_be_resolved(rule, multi_world.state)

    def test_given_tree_fruit_rule_then_can_be_resolved(self):
        for tree_fruit in logic.registry.tree_fruit_rules.keys():
            with self.subTest(msg=tree_fruit):
                rule = logic.registry.tree_fruit_rules[tree_fruit]
                self.assert_rule_can_be_resolved(rule, multi_world.state)

    def test_given_seed_rule_then_can_be_resolved(self):
        for seed in logic.registry.seed_rules.keys():
            with self.subTest(msg=seed):
                rule = logic.registry.seed_rules[seed]
                self.assert_rule_can_be_resolved(rule, multi_world.state)

    def test_given_crop_rule_then_can_be_resolved(self):
        for crop in logic.registry.crop_rules.keys():
            with self.subTest(msg=crop):
                rule = logic.registry.crop_rules[crop]
                self.assert_rule_can_be_resolved(rule, multi_world.state)

    def test_given_fish_rule_then_can_be_resolved(self):
        for fish in logic.registry.fish_rules.keys():
            with self.subTest(msg=fish):
                rule = logic.registry.fish_rules[fish]
                self.assert_rule_can_be_resolved(rule, multi_world.state)

    def test_given_museum_rule_then_can_be_resolved(self):
        for donation in logic.registry.museum_rules.keys():
            with self.subTest(msg=donation):
                rule = logic.registry.museum_rules[donation]
                self.assert_rule_can_be_resolved(rule, multi_world.state)

    def test_given_cooking_rule_then_can_be_resolved(self):
        for cooking_rule in logic.registry.cooking_rules.keys():
            with self.subTest(msg=cooking_rule):
                rule = logic.registry.cooking_rules[cooking_rule]
                self.assert_rule_can_be_resolved(rule, multi_world.state)

    def test_given_location_rule_then_can_be_resolved(self):
        for location in multi_world.get_locations(1):
            with self.subTest(msg=location.name):
                rule = location.access_rule
                self.assert_rule_can_be_resolved(rule, multi_world.state)
