from typing import List
from unittest import TestCase

from BaseClasses import CollectionState, Location, Region, Entrance
from ...stardew_rule import StardewRule, false_, MISSING_ITEM, Reach
from ...stardew_rule.rule_explain import explain


class RuleAssertMixin(TestCase):
    def assert_rule_true(self, rule: StardewRule, state: CollectionState):
        expl = explain(rule, state)
        try:
            self.assertTrue(rule(state), expl)
        except KeyError as e:
            raise AssertionError(f"Error while checking rule {rule}: {e}"
                                 f"\nExplanation: {expl}")

    def assert_rules_true(self, rules: List[StardewRule], state: CollectionState):
        for rule in rules:
            self.assert_rule_true(rule, state)

    def assert_rule_false(self, rule: StardewRule, state: CollectionState):
        expl = explain(rule, state, expected=False)
        try:
            self.assertFalse(rule(state), expl)
        except KeyError as e:
            raise AssertionError(f"Error while checking rule {rule}: {e}"
                                 f"\nExplanation: {expl}")

    def assert_rules_false(self, rules: List[StardewRule], state: CollectionState):
        for rule in rules:
            self.assert_rule_false(rule, state)

    def assert_rule_can_be_resolved(self, rule: StardewRule, complete_state: CollectionState):
        expl = explain(rule, complete_state)
        try:
            self.assertNotIn(MISSING_ITEM, repr(rule))
            self.assertTrue(rule is false_ or rule(complete_state), expl)
        except KeyError as e:
            raise AssertionError(f"Error while checking rule {rule}: {e}"
                                 f"\nExplanation: {expl}")

    def assert_can_reach_location(self, location: Location | str, state: CollectionState) -> None:
        location_name = location.name if isinstance(location, Location) else location
        expl = explain(Reach(location_name, "Location", 1), state)
        try:
            can_reach = state.can_reach_location(location_name, 1)
            self.assertTrue(can_reach, expl)
        except KeyError as e:
            raise AssertionError(f"Error while checking location {location_name}: {e}"
                                 f"\nExplanation: {expl}")

    def assert_cannot_reach_location(self, location: Location | str, state: CollectionState) -> None:
        location_name = location.name if isinstance(location, Location) else location
        expl = explain(Reach(location_name, "Location", 1), state, expected=False)
        try:
            can_reach = state.can_reach_location(location_name, 1)
            self.assertFalse(can_reach, expl)
        except KeyError as e:
            raise AssertionError(f"Error while checking location {location_name}: {e}"
                                 f"\nExplanation: {expl}")

    def assert_can_reach_region(self, region: Region | str, state: CollectionState) -> None:
        region_name = region.name if isinstance(region, Region) else region
        expl = explain(Reach(region_name, "Region", 1), state)
        try:
            can_reach = state.can_reach_region(region_name, 1)
            self.assertTrue(can_reach, expl)
        except KeyError as e:
            raise AssertionError(f"Error while checking region {region_name}: {e}"
                                 f"\nExplanation: {expl}")

    def assert_cannot_reach_region(self, region: Region | str, state: CollectionState) -> None:
        region_name = region.name if isinstance(region, Region) else region
        expl = explain(Reach(region_name, "Region", 1), state, expected=False)
        try:
            can_reach = state.can_reach_region(region_name, 1)
            self.assertFalse(can_reach, expl)
        except KeyError as e:
            raise AssertionError(f"Error while checking region {region_name}: {e}"
                                 f"\nExplanation: {expl}")

    def assert_can_reach_entrance(self, entrance: Entrance | str, state: CollectionState) -> None:
        entrance_name = entrance.name if isinstance(entrance, Entrance) else entrance
        expl = explain(Reach(entrance_name, "Entrance", 1), state)
        try:
            can_reach = state.can_reach_entrance(entrance_name, 1)
            self.assertTrue(can_reach, expl)
        except KeyError as e:
            raise AssertionError(f"Error while checking entrance {entrance_name}: {e}"
                                 f"\nExplanation: {expl}")
