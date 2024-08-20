import typing
import unittest
from unittest import TestCase, SkipTest

from BaseClasses import MultiWorld
from . import RuleAssertMixin, setup_solo_multiworld, allsanity_mods_6_x_x, minimal_locations_maximal_items
from .. import StardewValleyWorld
from ..data.bundle_data import all_bundle_items_except_money
from ..logic.logic import StardewLogic
from ..options import BundleRandomization


def collect_all(mw):
    for item in mw.get_items():
        mw.state.collect(item, prevent_sweep=True)


class LogicTestBase(RuleAssertMixin, TestCase):
    options: typing.Dict[str, typing.Any] = {}
    multiworld: MultiWorld
    logic: StardewLogic
    world: StardewValleyWorld

    @classmethod
    def setUpClass(cls) -> None:
        if cls is LogicTestBase:
            raise SkipTest("Not running test on base class.")

    def setUp(self) -> None:
        self.multiworld = setup_solo_multiworld(self.options, _cache={})
        collect_all(self.multiworld)
        self.world = typing.cast(StardewValleyWorld, self.multiworld.worlds[1])
        self.logic = self.world.logic

    def test_given_bundle_item_then_is_available_in_logic(self):
        for bundle_item in all_bundle_items_except_money:
            if not bundle_item.can_appear(self.world.content, self.world.options):
                continue

            with self.subTest(msg=bundle_item.item_name):
                self.assertIn(bundle_item.get_item(), self.logic.registry.item_rules)

    def test_given_item_rule_then_can_be_resolved(self):
        for item in self.logic.registry.item_rules.keys():
            with self.subTest(msg=item):
                rule = self.logic.registry.item_rules[item]
                self.assert_rule_can_be_resolved(rule, self.multiworld.state)

    def test_given_building_rule_then_can_be_resolved(self):
        for building in self.logic.registry.building_rules.keys():
            with self.subTest(msg=building):
                rule = self.logic.registry.building_rules[building]
                self.assert_rule_can_be_resolved(rule, self.multiworld.state)

    def test_given_quest_rule_then_can_be_resolved(self):
        for quest in self.logic.registry.quest_rules.keys():
            with self.subTest(msg=quest):
                rule = self.logic.registry.quest_rules[quest]
                self.assert_rule_can_be_resolved(rule, self.multiworld.state)

    def test_given_special_order_rule_then_can_be_resolved(self):
        for special_order in self.logic.registry.special_order_rules.keys():
            with self.subTest(msg=special_order):
                rule = self.logic.registry.special_order_rules[special_order]
                self.assert_rule_can_be_resolved(rule, self.multiworld.state)

    def test_given_crop_rule_then_can_be_resolved(self):
        for crop in self.logic.registry.crop_rules.keys():
            with self.subTest(msg=crop):
                rule = self.logic.registry.crop_rules[crop]
                self.assert_rule_can_be_resolved(rule, self.multiworld.state)

    def test_given_fish_rule_then_can_be_resolved(self):
        for fish in self.logic.registry.fish_rules.keys():
            with self.subTest(msg=fish):
                rule = self.logic.registry.fish_rules[fish]
                self.assert_rule_can_be_resolved(rule, self.multiworld.state)

    def test_given_museum_rule_then_can_be_resolved(self):
        for donation in self.logic.registry.museum_rules.keys():
            with self.subTest(msg=donation):
                rule = self.logic.registry.museum_rules[donation]
                self.assert_rule_can_be_resolved(rule, self.multiworld.state)

    def test_given_cooking_rule_then_can_be_resolved(self):
        for cooking_rule in self.logic.registry.cooking_rules.keys():
            with self.subTest(msg=cooking_rule):
                rule = self.logic.registry.cooking_rules[cooking_rule]
                self.assert_rule_can_be_resolved(rule, self.multiworld.state)

    def test_given_location_rule_then_can_be_resolved(self):
        for location in self.multiworld.get_locations(1):
            with self.subTest(msg=location.name):
                rule = location.access_rule
                self.assert_rule_can_be_resolved(rule, self.multiworld.state)


class TestAllSanityLogic(LogicTestBase):
    options = allsanity_mods_6_x_x()


@unittest.skip("This test does not pass because some content is still not in content packs.")
class TestMinLocationsMaxItemsLogic(LogicTestBase):
    options = minimal_locations_maximal_items()
    options[BundleRandomization.internal_name] = BundleRandomization.default
