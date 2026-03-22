"""Tests for Kirby AM world rule wiring."""

from __future__ import annotations

from dataclasses import dataclass
from unittest.mock import patch

from ..data import data
from ..options import Goal
from ..rules import ABILITY_GATE_RULES, _ABILITY_GATE_STATUS_VALUES, get_region_ability_gate_annotations, set_rules


@dataclass
class _FakeOptions:
    goal_value: int

    @property
    def goal(self):
        class _GoalValue:
            def __init__(self, value: int):
                self.value = value

        return _GoalValue(self.goal_value)


class _FakeEntrance:
    def __init__(self, name: str, player: int) -> None:
        self.name = name
        self.player = player


class _FakeLocation:
    def __init__(self, name: str, player: int) -> None:
        self.name = name
        self.player = player
        self.access_rule = lambda _state: True  # set_rule writes here


class _FakeMultiWorld:
    def __init__(self) -> None:
        self.completion_condition: dict[int, object] = {}
        self.entrances: dict[tuple[str, int], _FakeEntrance] = {}
        self.locations: dict[tuple[str, int], _FakeLocation] = {}

    def get_entrance(self, name: str, player: int):
        key = (name, player)
        if key not in self.entrances:
            self.entrances[key] = _FakeEntrance(name, player)
        return self.entrances[key]

    def get_location(self, name: str, player: int):
        key = (name, player)
        if key not in self.locations:
            self.locations[key] = _FakeLocation(name, player)
        return self.locations[key]


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
    assert completion_fn(_FakeState({"Defeat Dark Mind"}))


def test_100_percent_goal_requires_100_percent_event() -> None:
    world = _FakeWorld(Goal.option_100)
    set_rules(world)

    completion_fn = _get_completion_fn(world)
    assert not completion_fn(_FakeState({"Defeat Dark Mind"}))
    assert completion_fn(_FakeState({"100% Save File"}))


def test_debug_goal_is_always_complete() -> None:
    world = _FakeWorld(Goal.option_debug)
    set_rules(world)

    completion_fn = _get_completion_fn(world)
    assert completion_fn(_FakeState())


def test_set_rules_applies_shard_gate_to_dimension_mirror_and_goal_events() -> None:
    world = _FakeWorld(Goal.option_dark_mind)

    with patch("worlds.kirbyam.rules.set_rule") as mock_set_rule:
        set_rules(world)

    applied_names = [call.args[0].name for call in mock_set_rule.call_args_list]
    assert "REGION_GAME_START -> REGION_DIMENSION_MIRROR/MAIN" in applied_names
    assert "Defeat Dark Mind" in applied_names
    assert "100% Save File" in applied_names


ALL_SHARDS = {
    "Mustard Mountain - Mirror Shard",
    "Moonlight Mansion - Mirror Shard",
    "Candy Constellation - Mirror Shard",
    "Olive Ocean - Mirror Shard",
    "Peppermint Palace - Mirror Shard",
    "Cabbage Cavern - Mirror Shard",
    "Carrot Castle - Mirror Shard",
    "Radish Ruins - Mirror Shard",
}
_DMK_EVENT = "Defeat Dark Meta Knight (Dimension Mirror)"


def test_defeat_dark_mind_requires_dmk_event() -> None:
    """Defeat Dark Mind goal location must be blocked without the DMK event."""
    world = _FakeWorld(Goal.option_dark_mind)
    set_rules(world)

    dm_location = world.multiworld.get_location("Defeat Dark Mind", world.player)
    assert callable(dm_location.access_rule)

    # All shards but no DMK event: blocked.
    assert not dm_location.access_rule(_FakeState(ALL_SHARDS))

    # All shards + DMK event: accessible.
    assert dm_location.access_rule(_FakeState(ALL_SHARDS | {_DMK_EVENT}))


def test_defeat_dark_mind_blocked_without_shards() -> None:
    """Defeat Dark Mind goal location requires all 8 shards even with DMK event."""
    world = _FakeWorld(Goal.option_dark_mind)
    set_rules(world)

    dm_location = world.multiworld.get_location("Defeat Dark Mind", world.player)
    assert callable(dm_location.access_rule)

    # DMK event with partial shards: blocked.
    partial_shards = set(list(ALL_SHARDS)[:7])
    assert not dm_location.access_rule(_FakeState(partial_shards | {_DMK_EVENT}))

    # No shards and no DMK: blocked.
    assert not dm_location.access_rule(_FakeState({_DMK_EVENT}))


def test_100_percent_goal_does_not_require_dmk_event() -> None:
    """100% Save File goal location requires only shards, not the DMK event."""
    world = _FakeWorld(Goal.option_100)
    set_rules(world)

    pct_location = world.multiworld.get_location("100% Save File", world.player)
    assert callable(pct_location.access_rule)

    # All shards, no DMK event: accessible (100% has independent logic).
    assert pct_location.access_rule(_FakeState(ALL_SHARDS))

    # Partial shards: blocked.
    partial = set(list(ALL_SHARDS)[:7])
    assert not pct_location.access_rule(_FakeState(partial))


def test_dmk_event_present_in_dimension_mirror_region() -> None:
    """areas.json must declare the Defeat Dark Meta Knight (Dimension Mirror) event."""
    from ..data import load_json_data

    regions = load_json_data("regions/areas.json")
    dim_region = regions.get("REGION_DIMENSION_MIRROR/MAIN", {})
    assert dim_region, "REGION_DIMENSION_MIRROR/MAIN must exist in areas.json"
    events = dim_region.get("events", [])
    assert _DMK_EVENT in events, (
        f"{_DMK_EVENT!r} event must be declared in REGION_DIMENSION_MIRROR/MAIN events in areas.json"
    )


def test_ability_gate_helpers_default_true_without_ability_items() -> None:
    state = _FakeState()

    for gate_name, gate_rule in ABILITY_GATE_RULES.items():
        assert gate_rule(state, 1), f"{gate_name} should default to True until ability items exist"


def test_region_ability_gate_annotations_load_for_future_big_chest_rollout() -> None:
    annotations = get_region_ability_gate_annotations()

    expected_regions = {
        "REGION_MUSTARD_MOUNTAIN/MAIN",
        "REGION_MOONLIGHT_MANSION/MAIN",
        "REGION_CANDY_CONSTELLATION/MAIN",
        "REGION_OLIVE_OCEAN/MAIN",
        "REGION_CABBAGE_CAVERN/MAIN",
        "REGION_CARROT_CASTLE/MAIN",
        "REGION_RADISH_RUINS/MAIN",
    }
    assert expected_regions.issubset(annotations)

    for region_name in expected_regions:
        region_annotations = annotations[region_name]
        assert region_annotations == data.regions[region_name].ability_gates
        for gate_name, gate_annotation in region_annotations.items():
            assert gate_name in ABILITY_GATE_RULES
            assert gate_annotation["status"] in _ABILITY_GATE_STATUS_VALUES
            assert gate_annotation["applies_to"] == ["future_major_chest_locations"]
            assert gate_annotation["evidence"]

    assert annotations["REGION_OLIVE_OCEAN/MAIN"]["CanBreakBlocks"]["status"] == "confirmed"
    assert annotations["REGION_OLIVE_OCEAN/MAIN"]["CanPoundPegs"]["status"] == "confirmed"
    assert annotations["REGION_CABBAGE_CAVERN/MAIN"]["CanBreakBlocks"]["status"] == "confirmed"
    assert annotations["REGION_CABBAGE_CAVERN/MAIN"]["CanUseMini"]["status"] == "semantic_candidate"

