from typing import List
from unittest import TestCase

from BaseClasses import CollectionState, Location, Region, Entrance
from ...stardew_rule import StardewRule, false_, MISSING_ITEM, Reach
from ...stardew_rule.rule_explain import explain


class RuleAssertMixin(TestCase):
    def assert_rule_true(self, rule: StardewRule, state: CollectionState):
        try:
            rule_result = rule(state)
            if not rule_result:
                expl = explain(rule, state)
                self.assertTrue(rule(state), expl)
        except KeyError as e:
            expl = explain(rule, state)
            raise AssertionError(f"Error while checking rule {rule}: {e}"
                                 f"\nExplanation: {expl}")

    def assert_rules_true(self, rules: List[StardewRule], state: CollectionState):
        for rule in rules:
            self.assert_rule_true(rule, state)

    def assert_rule_false(self, rule: StardewRule, state: CollectionState):
        try:
            rule_result = rule(state)
            if rule_result:
                expl = explain(rule, state, expected=False)
                self.assertFalse(rule(state), expl)
        except KeyError as e:
            expl = explain(rule, state, expected=False)
            raise AssertionError(f"Error while checking rule {rule}: {e}"
                                 f"\nExplanation: {expl}")

    def assert_rules_false(self, rules: List[StardewRule], state: CollectionState):
        for rule in rules:
            self.assert_rule_false(rule, state)

    def assert_rule_can_be_resolved(self, rule: StardewRule, complete_state: CollectionState):
        try:
            self.assertNotIn(MISSING_ITEM, repr(rule))
            rule_valid = rule is false_ or rule(complete_state)
            if not rule_valid:
                expl = explain(rule, complete_state)
                self.assertTrue(rule_valid, expl)
        except KeyError as e:
            expl = explain(rule, complete_state)
            raise AssertionError(f"Error while checking rule {rule}: {e}"
                                 f"\nExplanation: {expl}")

    def assert_can_reach_location(self, location: Location | str, state: CollectionState) -> None:
        location_name = location.name if isinstance(location, Location) else location
        try:
            can_reach = state.can_reach_location(location_name, 1)
            if not can_reach:
                expl = explain(Reach(location_name, "Location", 1), state)
                self.assertTrue(can_reach, expl)
        except KeyError as e:
            expl = explain(Reach(location_name, "Location", 1), state)
            raise AssertionError(f"Error while checking location {location_name}: {e}"
                                 f"\nExplanation: {expl}")

    def assert_cannot_reach_location(self, location: Location | str, state: CollectionState) -> None:
        location_name = location.name if isinstance(location, Location) else location
        try:
            can_reach = state.can_reach_location(location_name, 1)
            if can_reach:
                expl = explain(Reach(location_name, "Location", 1), state, expected=False)
                self.assertFalse(can_reach, expl)
        except KeyError as e:
            expl = explain(Reach(location_name, "Location", 1), state, expected=False)
            raise AssertionError(f"Error while checking location {location_name}: {e}"
                                 f"\nExplanation: {expl}")

    def assert_can_reach_region(self, region: Region | str, state: CollectionState) -> None:
        region_name = region.name if isinstance(region, Region) else region
        try:
            can_reach = state.can_reach_region(region_name, 1)
            if not can_reach:
                expl = explain(Reach(region_name, "Region", 1), state)
                self.assertTrue(can_reach, expl)
        except KeyError as e:
            expl = explain(Reach(region_name, "Region", 1), state)
            raise AssertionError(f"Error while checking region {region_name}: {e}"
                                 f"\nExplanation: {expl}")

    def assert_cannot_reach_region(self, region: Region | str, state: CollectionState) -> None:
        region_name = region.name if isinstance(region, Region) else region
        try:
            can_reach = state.can_reach_region(region_name, 1)
            if can_reach:
                expl = explain(Reach(region_name, "Region", 1), state, expected=False)
                self.assertFalse(can_reach, expl)
        except KeyError as e:
            expl = explain(Reach(region_name, "Region", 1), state, expected=False)
            raise AssertionError(f"Error while checking region {region_name}: {e}"
                                 f"\nExplanation: {expl}")

    def assert_can_reach_entrance(self, entrance: Entrance | str, state: CollectionState) -> None:
        entrance_name = entrance.name if isinstance(entrance, Entrance) else entrance
        try:
            can_reach = state.can_reach_entrance(entrance_name, 1)
            if not can_reach:
                expl = explain(Reach(entrance_name, "Entrance", 1), state)
                self.assertTrue(can_reach, expl)
        except KeyError as e:
            expl = explain(Reach(entrance_name, "Entrance", 1), state)
            raise AssertionError(f"Error while checking entrance {entrance_name}: {e}"
                                 f"\nExplanation: {expl}")
