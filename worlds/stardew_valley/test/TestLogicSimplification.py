from .. import True_
from ..logic import Received, Has, False_, And, Or


def test_simplify_true_in_and():
    rules = {
        "Wood": True_(),
        "Rock": True_(),
    }
    summer = Received("Summer", 0, 1)
    assert (Has("Wood", rules) & summer & Has("Rock", rules)).simplify() == summer


def test_simplify_false_in_or():
    rules = {
        "Wood": False_(),
        "Rock": False_(),
    }
    summer = Received("Summer", 0, 1)
    assert (Has("Wood", rules) | summer | Has("Rock", rules)).simplify() == summer


def test_simplify_and_in_and():
    rule = And(And(Received('Summer', 0, 1), Received('Fall', 0, 1)),
               And(Received('Winter', 0, 1), Received('Spring', 0, 1)))
    assert rule.simplify() == And(Received('Summer', 0, 1), Received('Fall', 0, 1), Received('Winter', 0, 1),
                                  Received('Spring', 0, 1))


def test_simplify_duplicated_and():
    rule = And(And(Received('Summer', 0, 1), Received('Fall', 0, 1)),
               And(Received('Summer', 0, 1), Received('Fall', 0, 1)))
    assert rule.simplify() == And(Received('Summer', 0, 1), Received('Fall', 0, 1))


def test_simplify_or_in_or():
    rule = Or(Or(Received('Summer', 0, 1), Received('Fall', 0, 1)),
              Or(Received('Winter', 0, 1), Received('Spring', 0, 1)))
    assert rule.simplify() == Or(Received('Summer', 0, 1), Received('Fall', 0, 1), Received('Winter', 0, 1),
                                 Received('Spring', 0, 1))


def test_simplify_duplicated_or():
    rule = And(Or(Received('Summer', 0, 1), Received('Fall', 0, 1)),
               Or(Received('Summer', 0, 1), Received('Fall', 0, 1)))
    assert rule.simplify() == Or(Received('Summer', 0, 1), Received('Fall', 0, 1))


def test_simplify_true_in_or():
    rule = Or(True_(), Received('Summer', 0, 1))
    assert rule.simplify() == True_()


def test_simplify_false_in_and():
    rule = And(False_(), Received('Summer', 0, 1))
    assert rule.simplify() == False_()
