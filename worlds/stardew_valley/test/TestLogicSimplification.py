from .. import _True
from ..logic import _Received, _Has, _False, _And, _Or


def test_simplify_true_in_and():
    rules = {
        "Wood": _True(),
        "Rock": _True(),
    }
    summer = _Received("Summer", 0, 1)
    assert (_Has("Wood", rules) & summer & _Has("Rock", rules)).simplify() == summer


def test_simplify_false_in_or():
    rules = {
        "Wood": _False(),
        "Rock": _False(),
    }
    summer = _Received("Summer", 0, 1)
    assert (_Has("Wood", rules) | summer | _Has("Rock", rules)).simplify() == summer


def test_simplify_and_in_and():
    rule = _And(_And(_Received('Summer', 0, 1), _Received('Fall', 0, 1)),
                _And(_Received('Winter', 0, 1), _Received('Spring', 0, 1)))
    assert rule.simplify() == _And(_Received('Summer', 0, 1), _Received('Fall', 0, 1), _Received('Winter', 0, 1),
                                   _Received('Spring', 0, 1))


def test_simplify_duplicated_and():
    rule = _And(_And(_Received('Summer', 0, 1), _Received('Fall', 0, 1)),
                _And(_Received('Summer', 0, 1), _Received('Fall', 0, 1)))
    assert rule.simplify() == _And(_Received('Summer', 0, 1), _Received('Fall', 0, 1))


def test_simplify_or_in_or():
    rule = _Or(_Or(_Received('Summer', 0, 1), _Received('Fall', 0, 1)),
               _Or(_Received('Winter', 0, 1), _Received('Spring', 0, 1)))
    assert rule.simplify() == _Or(_Received('Summer', 0, 1), _Received('Fall', 0, 1), _Received('Winter', 0, 1),
                                  _Received('Spring', 0, 1))


def test_simplify_duplicated_or():
    rule = _And(_Or(_Received('Summer', 0, 1), _Received('Fall', 0, 1)),
                _Or(_Received('Summer', 0, 1), _Received('Fall', 0, 1)))
    assert rule.simplify() == _Or(_Received('Summer', 0, 1), _Received('Fall', 0, 1))


def test_simplify_true_in_or():
    rule = _Or(_True(), _Received('Summer', 0, 1))
    assert rule.simplify() == _True()


def test_simplify_false_in_and():
    rule = _And(_False(), _Received('Summer', 0, 1))
    assert rule.simplify() == _False()
