import unittest
from unittest import skip

from ..stardew_rule import Received, Has, False_, And, Or, True_, HasProgressionPercent


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
