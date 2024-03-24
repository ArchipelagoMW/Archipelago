from unittest import TestCase

from BaseClasses import CollectionState, Location
from ...stardew_rule import StardewRule, false_, MISSING_ITEM, Reach
from ...stardew_rule.rule_explain import explain


class RuleAssertMixin(TestCase):
    def assert_rule_true(self, rule: StardewRule, state: CollectionState):
        self.assertTrue(rule(state), explain(rule, state))

    def assert_rule_false(self, rule: StardewRule, state: CollectionState):
        self.assertFalse(rule(state), explain(rule, state, expected=False))

    def assert_rule_can_be_resolved(self, rule: StardewRule, complete_state: CollectionState):
        self.assertNotIn(MISSING_ITEM, repr(rule))
        self.assertTrue(rule is false_ or rule(complete_state), explain(rule, complete_state))

    def assert_reach_location_true(self, location: Location, state: CollectionState):
        self.assertTrue(location.can_reach(state), explain(Reach(location.name, "Location", 1), state))

    def assert_reach_location_false(self, location: Location, state: CollectionState):
        self.assertFalse(location.can_reach(state), explain(Reach(location.name, "Location", 1), state, expected=False))
