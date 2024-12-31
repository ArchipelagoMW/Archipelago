from typing import List
from unittest import TestCase

from BaseClasses import CollectionState, Location
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

    def assert_reach_location_true(self, location: Location, state: CollectionState):
        expl = explain(Reach(location.name, "Location", 1), state)
        try:
            can_reach = location.can_reach(state)
            self.assertTrue(can_reach, expl)
        except KeyError as e:
            raise AssertionError(f"Error while checking location {location.name}: {e}"
                                 f"\nExplanation: {expl}")

    def assert_reach_location_false(self, location: Location, state: CollectionState):
        expl = explain(Reach(location.name, "Location", 1), state, expected=False)
        try:
            self.assertFalse(location.can_reach(state), expl)
        except KeyError as e:
            raise AssertionError(f"Error while checking location {location.name}: {e}"
                                 f"\nExplanation: {expl}")
