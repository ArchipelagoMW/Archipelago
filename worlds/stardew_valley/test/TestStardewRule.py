import unittest
from unittest import skip
from unittest.mock import MagicMock, Mock

from ..stardew_rule import Received, Has, False_, And, Or, True_, HasProgressionPercent, false_, true_


class TestSimplification(unittest.TestCase):
    def test_simplify_true_in_and(self):
        rules = {
            "Wood": True_(),
            "Rock": True_(),
        }
        summer = Received("Summer", 0, 1)
        self.assertEqual(summer, (Has("Wood", rules) & summer & Has("Rock", rules)).simplify())

    def test_simplify_false_in_or(self):
        rules = {
            "Wood": False_(),
            "Rock": False_(),
        }
        summer = Received("Summer", 0, 1)
        self.assertEqual(summer, (Has("Wood", rules) | summer | Has("Rock", rules)).simplify())

    def test_simplify_and_in_and(self):
        rule = And(Received('Summer', 0, 1), Received('Fall', 0, 1)) & And(Received('Winter', 0, 1), Received('Spring', 0, 1))
        self.assertEqual(And(Received('Summer', 0, 1), Received('Fall', 0, 1), Received('Winter', 0, 1), Received('Spring', 0, 1)), rule.simplify())

    @skip("This feature has been disabled and that seems to save time")
    def test_simplify_duplicated_and(self):
        rule = And(And(Received('Summer', 0, 1), Received('Fall', 0, 1)), And(Received('Summer', 0, 1), Received('Fall', 0, 1)))
        self.assertEqual(And(Received('Summer', 0, 1), Received('Fall', 0, 1)), rule.simplify())

    def test_simplify_or_in_or(self):
        rule = Or(Received('Summer', 0, 1), Received('Fall', 0, 1)) | Or(Received('Winter', 0, 1), Received('Spring', 0, 1))
        self.assertEqual(Or(Received('Summer', 0, 1), Received('Fall', 0, 1), Received('Winter', 0, 1), Received('Spring', 0, 1)), rule.simplify())

    @skip("This feature has been disabled and that seems to save time")
    def test_simplify_duplicated_or(self):
        rule = And(Or(Received('Summer', 0, 1), Received('Fall', 0, 1)), Or(Received('Summer', 0, 1), Received('Fall', 0, 1)))
        self.assertEqual(Or(Received('Summer', 0, 1), Received('Fall', 0, 1)), rule.simplify())

    def test_simplify_true_in_or(self):
        rule = Or(True_(), Received('Summer', 0, 1))
        self.assertEqual(True_(), rule.simplify())

    def test_simplify_false_in_and(self):
        rule = And(False_(), Received('Summer', 0, 1))
        self.assertEqual(False_(), rule.simplify())


class TestHasProgressionPercentSimplification(unittest.TestCase):
    def test_has_progression_percent_and_uses_max(self):
        rule = HasProgressionPercent(1, 20) & HasProgressionPercent(1, 10)
        self.assertEqual(rule, HasProgressionPercent(1, 20))

    def test_has_progression_percent_or_uses_min(self):
        rule = HasProgressionPercent(1, 20) | HasProgressionPercent(1, 10)
        self.assertEqual(rule, HasProgressionPercent(1, 10))

    def test_and_between_progression_percent_and_other_progression_percent_uses_max(self):
        cases = [
            And(HasProgressionPercent(1, 10)) & HasProgressionPercent(1, 20),
            HasProgressionPercent(1, 10) & And(HasProgressionPercent(1, 20)),
            And(HasProgressionPercent(1, 20)) & And(HasProgressionPercent(1, 10)),
        ]
        for i, case in enumerate(cases):
            with self.subTest(f"{i} {repr(case)}"):
                self.assertEqual(case, And(HasProgressionPercent(1, 20)))

    def test_or_between_progression_percent_and_other_progression_percent_uses_max(self):
        cases = [
            Or(HasProgressionPercent(1, 10)) | HasProgressionPercent(1, 20),
            HasProgressionPercent(1, 10) | Or(HasProgressionPercent(1, 20)),
            Or(HasProgressionPercent(1, 20)) | Or(HasProgressionPercent(1, 10))
        ]
        for i, case in enumerate(cases):
            with self.subTest(f"{i} {repr(case)}"):
                self.assertEqual(case, Or(HasProgressionPercent(1, 10)))


class TestEvaluateWhileSimplifying(unittest.TestCase):
    def test_propagate_evaluate_while_simplifying(self):
        expected_result = True
        collection_state = MagicMock()
        other_rule = MagicMock()
        other_rule.evaluate_while_simplifying = Mock(return_value=(other_rule, expected_result))
        rule = And(Or(other_rule))

        _, actual_result = rule.evaluate_while_simplifying(collection_state)

        other_rule.evaluate_while_simplifying.assert_called_with(collection_state)
        self.assertEqual(expected_result, actual_result)

    def test_return_complement_when_its_found(self):
        expected_simplified = false_
        expected_result = False
        collection_state = MagicMock()
        rule = And(expected_simplified)

        actual_simplified, actual_result = rule.evaluate_while_simplifying(collection_state)

        self.assertEqual(expected_result, actual_result)
        self.assertEqual(expected_simplified, actual_simplified)

    def test_short_circuit_when_complement_found(self):
        collection_state = MagicMock()
        other_rule = MagicMock()
        rule = Or(true_, )

        rule.evaluate_while_simplifying(collection_state)

        other_rule.evaluate_while_simplifying.assert_not_called()

    def test_short_circuit_when_combinable_rules_is_false(self):
        collection_state = MagicMock()
        other_rule = MagicMock()
        rule = And(HasProgressionPercent(1, 10), other_rule)

        rule.evaluate_while_simplifying(collection_state)

        other_rule.evaluate_while_simplifying.assert_not_called()

    def test_identity_is_removed_from_other_rules(self):
        collection_state = MagicMock()
        rule = Or(false_, HasProgressionPercent(1, 10))

        rule.evaluate_while_simplifying(collection_state)

        self.assertEqual(0, len(rule.other_rules))

    def test_complement_replaces_combinable_rules(self):
        collection_state = MagicMock()
        rule = Or(HasProgressionPercent(1, 10), true_)

        rule.evaluate_while_simplifying(collection_state)

        self.assertEqual(0, len(rule.combinable_rules))

    def test_simplifying_to_complement_propagates_complement(self):
        expected_simplified = true_
        expected_result = True
        collection_state = MagicMock()
        rule = Or(Or(expected_simplified), HasProgressionPercent(1, 10))

        actual_simplified, actual_result = rule.evaluate_while_simplifying(collection_state)

        self.assertEqual(expected_result, actual_result)
        self.assertEqual(expected_simplified, actual_simplified)
        self.assertEqual(0, len(rule.combinable_rules))

    def test_already_simplified_rules_are_not_simplified_again(self):
        collection_state = MagicMock()
        other_rule = MagicMock()
        other_rule.evaluate_while_simplifying = Mock(return_value=(other_rule, False))
        rule = Or(other_rule, HasProgressionPercent(1, 10))

        rule.evaluate_while_simplifying(collection_state)
        other_rule.assert_not_called()
        other_rule.evaluate_while_simplifying.reset_mock()

        rule.evaluate_while_simplifying(collection_state)
        other_rule.assert_called_with(collection_state)
        other_rule.evaluate_while_simplifying.assert_not_called()

    def test_continue_simplification_after_short_circuited(self):
        collection_state = MagicMock()
        a_rule = MagicMock()
        a_rule.evaluate_while_simplifying = Mock(return_value=(a_rule, False))
        another_rule = MagicMock()
        another_rule.evaluate_while_simplifying = Mock(return_value=(another_rule, False))
        rule = And(a_rule, another_rule)

        rule.evaluate_while_simplifying(collection_state)
        # This test is completely messed up because sets are used internally and order of the rules cannot be ensured.
        not_yet_simplified, already_simplified = (another_rule, a_rule) if a_rule.evaluate_while_simplifying.called else (a_rule, another_rule)
        not_yet_simplified.evaluate_while_simplifying.assert_not_called()
        already_simplified.return_value = True

        rule.evaluate_while_simplifying(collection_state)
        not_yet_simplified.evaluate_while_simplifying.assert_called_with(collection_state)


@skip("Those two tests validate a bug that has yet to be fixed.")
class TestEvaluateWhileSimplifyingDoubleCalls(unittest.TestCase):
    """
    So, there is a situation where a rule kind of calls itself while it's being evaluated, because its evaluation triggers a region cache refresh.

    The region cache check every entrance, so if a rule is also used in an entrances, it can be reevaluated.
    """

    def test_nested_call_in_the_internal_rule_being_evaluated_does_check_the_internal_rule(self):
        collection_state = MagicMock()
        internal_rule = MagicMock()
        rule = Or(internal_rule)

        called_once = False
        internal_call_result = None

        def first_call_to_internal_rule(state):
            nonlocal internal_call_result
            nonlocal called_once
            if called_once:
                return internal_rule, True
            called_once = True

            _, internal_call_result = rule.evaluate_while_simplifying(state)
            internal_rule.evaluate_while_simplifying = Mock(return_value=(internal_rule, True))
            return internal_rule, True

        internal_rule.evaluate_while_simplifying = first_call_to_internal_rule

        rule.evaluate_while_simplifying(collection_state)

        self.assertTrue(called_once)
        self.assertTrue(internal_call_result)

    def test_nested_call_to_already_simplified_rule_does_not_steal_rule_to_simplified_from_parent_call(self):
        collection_state = MagicMock()
        an_internal_rule = MagicMock()
        an_internal_rule.evaluate_while_simplifying = Mock(return_value=(an_internal_rule, True))
        another_internal_rule = MagicMock()
        another_internal_rule.evaluate_while_simplifying = Mock(return_value=(another_internal_rule, True))
        rule = Or(an_internal_rule, another_internal_rule)

        rule.evaluate_while_simplifying(collection_state)
        # This test is completely messed up because sets are used internally and order of the rules cannot be ensured.
        if an_internal_rule.evaluate_while_simplifying.called:
            not_yet_simplified, already_simplified = another_internal_rule, an_internal_rule
        else:
            not_yet_simplified, already_simplified = an_internal_rule, another_internal_rule

        called_once = False
        internal_call_result = None

        def call_to_already_simplified(state):
            nonlocal internal_call_result
            nonlocal called_once
            if called_once:
                return False
            called_once = True

            _, internal_call_result = rule.evaluate_while_simplifying(state)
            return False

        already_simplified.side_effect = call_to_already_simplified

        _, actual_result = rule.evaluate_while_simplifying(collection_state)

        self.assertTrue(called_once)
        self.assertTrue(internal_call_result)
        self.assertTrue(actual_result)
