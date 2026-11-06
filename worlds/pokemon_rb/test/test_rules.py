import unittest
from types import SimpleNamespace
from unittest import mock

from .. import rules


class DummyState:
    def __init__(self, items=None) -> None:
        self.items = dict(items or {})

    def has(self, name: str, player: int, count: int = 1) -> bool:
        return self.items.get(name, 0) >= count

    def has_any(self, names, player: int) -> bool:
        return any(self.has(name, player) for name in names)


class FakeLocation:
    def __init__(self, name: str) -> None:
        self.name = name


class FakeMultiWorld:
    def __init__(self, names) -> None:
        self.locations = [FakeLocation(name) for name in names]

    def get_locations(self, player: int):
        return self.locations


def make_world() -> SimpleNamespace:
    return SimpleNamespace(
        options=SimpleNamespace(
            prizesanity=False,
            require_pokedex=False,
            oaks_aide_rt_2=SimpleNamespace(value=0),
            oaks_aide_rt_11=SimpleNamespace(value=0),
            oaks_aide_rt_15=SimpleNamespace(value=0),
        ),
    )


def capture_access_rules(names):
    multiworld = FakeMultiWorld(names)
    access_rules = {}

    def remember_rule(location, rule) -> None:
        access_rules[location.name] = rule

    with mock.patch.object(rules, "add_rule", side_effect=remember_rule), \
            mock.patch.object(rules, "add_item_rule"):
        rules.set_rules(multiworld, make_world(), 1)

    return access_rules


class TestBranchRuleChanges(unittest.TestCase):
    def test_route_22_rival_and_trainer_parties_require_oaks_parcel(self) -> None:
        access_rules = capture_access_rules([
            "Route 22 - Rival 1",
            "Route 22 - Trainer Parties",
        ])

        for location_name in access_rules:
            with self.subTest(location_name=location_name):
                self.assertFalse(access_rules[location_name](DummyState()))
                self.assertTrue(access_rules[location_name](DummyState({"Oak's Parcel": 1})))

    def test_fighting_dojo_gifts_allow_defeating_sabrina_or_ut_glitch(self) -> None:
        access_rules = capture_access_rules([
            "Saffron Fighting Dojo - Gift 1",
            "Saffron Fighting Dojo - Gift 2",
        ])

        for location_name in access_rules:
            with self.subTest(location_name=location_name):
                self.assertFalse(access_rules[location_name](DummyState()))
                self.assertTrue(access_rules[location_name](DummyState({"Defeat Sabrina": 1})))
                self.assertTrue(access_rules[location_name](DummyState({"ut_glitch": 1})))
