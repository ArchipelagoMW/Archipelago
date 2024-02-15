import unittest
from .. import True_
from ..logic import Received, Has, False_, And, Or


class TestSimplification(unittest.TestCase):
    def test_simplify_true_in_and(self):
        rules = {
            "Wood": True_(),
            "Rock": True_(),
        }
        summer = Received("Summer", 0, 1)
        self.assertEqual((Has("Wood", rules) & summer & Has("Rock", rules)).simplify(),
                         summer)

    def test_simplify_false_in_or(self):
        rules = {
            "Wood": False_(),
            "Rock": False_(),
        }
        summer = Received("Summer", 0, 1)
        self.assertEqual((Has("Wood", rules) | summer | Has("Rock", rules)).simplify(),
                         summer)

    def test_simplify_and_in_and(self):
        rule = And(And(Received('Summer', 0, 1), Received('Fall', 0, 1)),
                   And(Received('Winter', 0, 1), Received('Spring', 0, 1)))
        self.assertEqual(rule.simplify(),
                         And(Received('Summer', 0, 1), Received('Fall', 0, 1),
                             Received('Winter', 0, 1), Received('Spring', 0, 1)))

    def test_simplify_duplicated_and(self):
        rule = And(And(Received('Summer', 0, 1), Received('Fall', 0, 1)),
                   And(Received('Summer', 0, 1), Received('Fall', 0, 1)))
        self.assertEqual(rule.simplify(),
                         And(Received('Summer', 0, 1), Received('Fall', 0, 1)))

    def test_simplify_or_in_or(self):
        rule = Or(Or(Received('Summer', 0, 1), Received('Fall', 0, 1)),
                  Or(Received('Winter', 0, 1), Received('Spring', 0, 1)))
        self.assertEqual(rule.simplify(),
                         Or(Received('Summer', 0, 1), Received('Fall', 0, 1), Received('Winter', 0, 1),
                            Received('Spring', 0, 1)))

    def test_simplify_duplicated_or(self):
        rule = And(Or(Received('Summer', 0, 1), Received('Fall', 0, 1)),
                   Or(Received('Summer', 0, 1), Received('Fall', 0, 1)))
        self.assertEqual(rule.simplify(),
                         Or(Received('Summer', 0, 1), Received('Fall', 0, 1)))

    def test_simplify_true_in_or(self):
        rule = Or(True_(), Received('Summer', 0, 1))
        self.assertEqual(rule.simplify(), True_())

    def test_simplify_false_in_and(self):
        rule = And(False_(), Received('Summer', 0, 1))
        self.assertEqual(rule.simplify(), False_())
