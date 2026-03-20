"""Tests for Kirby AM world rule wiring."""

from __future__ import annotations

from dataclasses import dataclass

from ..options import Goal
from ..rules import set_rules


@dataclass
class _FakeOptions:
    goal_value: int

    @property
    def goal(self):
        class _GoalValue:
            def __init__(self, value: int):
                self.value = value

        return _GoalValue(self.goal_value)


class _FakeMultiWorld:
    def __init__(self) -> None:
        self.completion_condition: dict[int, object] = {}

    def get_entrance(self, _name: str, _player: int):
        raise KeyError("Entrance map is not required for completion rule tests")


class _FakeState:
    def __init__(self, owned: set[str] | None = None) -> None:
        self._owned = owned or set()

    def has(self, name: str, _player: int) -> bool:
        return name in self._owned

    def has_from_list_unique(self, names: list[str], _player: int, amount: int) -> bool:
        return len(set(names).intersection(self._owned)) >= amount


class _FakeWorld:
    def __init__(self, goal_value: int, player: int = 1) -> None:
        self.player = player
        self.options = _FakeOptions(goal_value)
        self.multiworld = _FakeMultiWorld()


def _get_completion_fn(world: _FakeWorld):
    completion_fn = world.multiworld.completion_condition[world.player]
    assert callable(completion_fn)
    return completion_fn


def test_dark_mind_goal_requires_dark_mind_event() -> None:
    world = _FakeWorld(Goal.option_dark_mind)
    set_rules(world)

    completion_fn = _get_completion_fn(world)
    assert not completion_fn(_FakeState())
    assert completion_fn(_FakeState({"EVENT_DEFEAT_DARK_MIND"}))


def test_100_percent_goal_requires_100_percent_event() -> None:
    world = _FakeWorld(Goal.option_100)
    set_rules(world)

    completion_fn = _get_completion_fn(world)
    assert not completion_fn(_FakeState({"EVENT_DEFEAT_DARK_MIND"}))
    assert completion_fn(_FakeState({"EVENT_100_PERCENT"}))


def test_debug_goal_is_always_complete() -> None:
    world = _FakeWorld(Goal.option_debug)
    set_rules(world)

    completion_fn = _get_completion_fn(world)
    assert completion_fn(_FakeState())
