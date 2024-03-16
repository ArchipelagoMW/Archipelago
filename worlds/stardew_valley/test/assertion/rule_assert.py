from unittest import TestCase

from BaseClasses import CollectionState
from ...stardew_rule import StardewRule, false_, MISSING_ITEM
from ...stardew_rule.rule_explain import explain


class RuleAssertMixin(TestCase):
    def assert_rule_true(self, rule: StardewRule, state: CollectionState):
        self.assertTrue(rule(state), explain(rule, state))

    def assert_rule_false(self, rule: StardewRule, state: CollectionState):
        self.assertFalse(rule(state), explain(rule, state, expected=False))

    def assert_rule_can_be_resolved(self, rule: StardewRule, complete_state: CollectionState):
        self.assertNotIn(MISSING_ITEM, repr(rule))
        self.assertTrue(rule is false_ or rule(complete_state), explain(rule, complete_state))
