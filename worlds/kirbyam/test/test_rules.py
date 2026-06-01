"""Tests for Kirby AM world rule wiring."""

from __future__ import annotations

from dataclasses import dataclass
from unittest.mock import patch

from ..options import Goal
from ..rules import (
    ABILITY_GATE_RULES,
    get_stake_breaking_abilities,
    get_stake_gated_transition_entrance_names,
    set_rules,
)


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


def test_unknown_goal_value_defaults_to_dark_mind_completion() -> None:
    world = _FakeWorld(99)
    set_rules(world)

    completion_fn = _get_completion_fn(world)
    assert not completion_fn(_FakeState())
    assert completion_fn(_FakeState({"Defeat Dark Mind"}))


def test_set_rules_applies_shard_gate_to_dimension_mirror_and_goal_events() -> None:
    world = _FakeWorld(Goal.option_dark_mind)

    with patch("worlds.kirbyam.rules.set_rule") as mock_set_rule:
        set_rules(world)

    applied_names = [call.args[0].name for call in mock_set_rule.call_args_list]
    assert "REGION_RAINBOW_ROUTE/MAIN -> REGION_DIMENSION_MIRROR/MAIN" in applied_names
    assert "Defeat Dark Mind" in applied_names


def test_area_topology_routes_start_through_rainbow_route_anchor() -> None:
    from ..data import load_json_data

    regions = load_json_data("regions/areas.json")

    assert regions["REGION_GAME_START"]["exits"] == ["REGION_RAINBOW_ROUTE/MAIN"]

    # Rainbow Route is the hub; connects to all areas that have a hub mirror in
    # the room-level transition data. Olive Ocean and Radish Ruins have no hub
    # mirror to Rainbow Route (they are reached via adjacent areas instead).
    assert set(regions["REGION_RAINBOW_ROUTE/MAIN"]["exits"]) == {
        "REGION_RAINBOW_ROUTE/ROOM_1_CENTRAL_CIRCLE",
        "REGION_MUSTARD_MOUNTAIN/MAIN",
        "REGION_MOONLIGHT_MANSION/MAIN",
        "REGION_CANDY_CONSTELLATION/MAIN",
        "REGION_PEPPERMINT_PALACE/MAIN",
        "REGION_CABBAGE_CAVERN/MAIN",
        "REGION_CARROT_CASTLE/MAIN",
        "REGION_DIMENSION_MIRROR/MAIN",
    }

    # Areas connected to Rainbow Route via hub mirror exit back to it.
    for region_name in {
        "REGION_MUSTARD_MOUNTAIN/MAIN",
        "REGION_MOONLIGHT_MANSION/MAIN",
        "REGION_CANDY_CONSTELLATION/MAIN",
        "REGION_PEPPERMINT_PALACE/MAIN",
        "REGION_CABBAGE_CAVERN/MAIN",
        "REGION_CARROT_CASTLE/MAIN",
    }:
        assert "REGION_RAINBOW_ROUTE/MAIN" in regions[region_name]["exits"]

    # Areas reachable only via cross-area mirrors have no direct Rainbow Route exit.
    assert "REGION_RAINBOW_ROUTE/MAIN" not in regions["REGION_OLIVE_OCEAN/MAIN"]["exits"]
    assert "REGION_RAINBOW_ROUTE/MAIN" not in regions["REGION_RADISH_RUINS/MAIN"]["exits"]

    # Cross-area mirror connections derived from rooms.json transitions data.
    assert set(regions["REGION_CABBAGE_CAVERN/MAIN"]["exits"]) >= {
        "REGION_OLIVE_OCEAN/MAIN", "REGION_RADISH_RUINS/MAIN",
    }
    assert "REGION_OLIVE_OCEAN/MAIN" in regions["REGION_MOONLIGHT_MANSION/MAIN"]["exits"]
    assert set(regions["REGION_OLIVE_OCEAN/MAIN"]["exits"]) >= {
        "REGION_CABBAGE_CAVERN/MAIN", "REGION_MOONLIGHT_MANSION/MAIN",
    }
    assert set(regions["REGION_CARROT_CASTLE/MAIN"]["exits"]) >= {
        "REGION_PEPPERMINT_PALACE/MAIN", "REGION_RADISH_RUINS/MAIN",
    }
    assert set(regions["REGION_PEPPERMINT_PALACE/MAIN"]["exits"]) >= {"REGION_CARROT_CASTLE/MAIN"}
    assert set(regions["REGION_RADISH_RUINS/MAIN"]["exits"]) >= {
        "REGION_CABBAGE_CAVERN/MAIN", "REGION_CARROT_CASTLE/MAIN",
    }


def test_room_subareas_pure_topology_with_all_rooms() -> None:
    from ..data import load_json_data

    room_regions = load_json_data("regions/rooms.json")

    assert len(room_regions) == 286

    included_room_sanity = [
        region.get("room_sanity", {}).get("included", False)
        for region in room_regions.values()
    ]
    assert sum(1 for included in included_room_sanity if included) == 263

    included_room_sanity_ids = [
        region["room_sanity"]["location_id"]
        for region in room_regions.values()
        if region.get("room_sanity", {}).get("included", False)
    ]
    included_room_sanity_bits = [
        region["room_sanity"]["bit_index"]
        for region in room_regions.values()
        if region.get("room_sanity", {}).get("included", False)
    ]
    assert len(included_room_sanity_ids) == len(set(included_room_sanity_ids))
    assert len(included_room_sanity_bits) == len(set(included_room_sanity_bits))

    expected_warp_room_sanity = {
        "REGION_RAINBOW_ROUTE/ROOM_1_WARP",
        "REGION_MOONLIGHT_MANSION/ROOM_2_WARP",
        "REGION_MUSTARD_MOUNTAIN/ROOM_4_WARP",
        "REGION_CARROT_CASTLE/ROOM_5_WARP",
        "REGION_PEPPERMINT_PALACE/ROOM_7_WARP",
        "REGION_CANDY_CONSTELLATION/ROOM_9_WARP",
    }
    for region_key in expected_warp_room_sanity:
        room_meta = room_regions[region_key]["room_sanity"]
        assert room_meta["included"] is True
        assert isinstance(room_meta["location_id"], int)
        assert isinstance(room_meta["bit_index"], int)

    # Rooms may carry location data where the actual in-game pickup occurs.
    # Exactly the rooms with boss defeats and big chests should have locations;
    # all other rooms remain topology-only with empty lists.
    from ..data import load_json_data as _load
    known_locations = set(_load("locations.json").keys())
    rooms_with_locations = {
        key: region["locations"]
        for key, region in room_regions.items()
        if region.get("locations")
    }
    # Every location claimed by a room must be a known location key
    for room_key, loc_list in rooms_with_locations.items():
        for loc_key in loc_list:
            assert loc_key in known_locations, (
                f"Room {room_key} claims unknown location key {loc_key!r}"
            )
    # Canonical room entries carry 38 AP locations; additional location ownership
    # can live in logical_subregions for disconnected chamber modeling.
    room_keys = list(rooms_with_locations.keys())
    assert len(rooms_with_locations) == 38, (
        f"Expected 38 canonical rooms with locations, got {len(rooms_with_locations)}: {room_keys}"
    )

    # Topology includes all rooms, but Room Sanity remains optional metadata.
    assert all(
        "room_sanity" in region for region in room_regions.values()
    ), "All room regions must carry room_sanity metadata"

    assert all(
        "exits" in region for region in room_regions.values()
    ), "All room regions must have exits defined"


def test_room_subareas_preserve_two_way_and_one_way_transitions() -> None:
    from ..data import load_json_data

    room_regions = load_json_data("regions/rooms.json")

    assert "REGION_RAINBOW_ROUTE/ROOM_1_35" in room_regions["REGION_RAINBOW_ROUTE/ROOM_1_CENTRAL_CIRCLE"]["exits"]
    assert "REGION_RAINBOW_ROUTE/ROOM_1_CENTRAL_CIRCLE" in room_regions["REGION_RAINBOW_ROUTE/ROOM_1_35"]["exits"]

    assert "REGION_RAINBOW_ROUTE/ROOM_1_39" in room_regions["REGION_RAINBOW_ROUTE/ROOM_1_38"]["exits"]
    assert "REGION_RAINBOW_ROUTE/ROOM_1_38" not in room_regions["REGION_RAINBOW_ROUTE/ROOM_1_39"]["exits"]


def test_room_reachability_from_start() -> None:
    from ..rules import _reachable_rooms_from

    reachable = _reachable_rooms_from("REGION_RAINBOW_ROUTE/ROOM_1_CENTRAL_CIRCLE")

    assert len(reachable) == 263
    assert "REGION_RAINBOW_ROUTE/ROOM_1_CENTRAL_CIRCLE" in reachable
    assert "REGION_RAINBOW_ROUTE/ROOM_1_35" in reachable
    assert "REGION_CANDY_CONSTELLATION/ROOM_9_20" in reachable


def test_room_sanity_binding_optional() -> None:
    from ..data import load_json_data
    from ..rules import _bind_room_sanity_locations

    room_regions = load_json_data("regions/rooms.json")

    regions_before = {
        name: region.get("locations", []).copy()
        for name, region in room_regions.items()
    }

    _bind_room_sanity_locations(room_regions, enable_room_sanity=False)
    assert (
        room_regions["REGION_RAINBOW_ROUTE/ROOM_1_CENTRAL_CIRCLE"]["locations"]
        == regions_before["REGION_RAINBOW_ROUTE/ROOM_1_CENTRAL_CIRCLE"]
    )

    _bind_room_sanity_locations(room_regions, enable_room_sanity=True)
    assert "ROOM_SANITY_1_CENTRAL_CIRCLE" in room_regions["REGION_RAINBOW_ROUTE/ROOM_1_CENTRAL_CIRCLE"]["locations"]
    assert "ROOM_SANITY_1_WARP" in room_regions["REGION_RAINBOW_ROUTE/ROOM_1_WARP"]["locations"]
    assert "ROOM_SANITY_2_WARP" in room_regions["REGION_MOONLIGHT_MANSION/ROOM_2_WARP"]["locations"]
    assert "ROOM_SANITY_4_WARP" in room_regions["REGION_MUSTARD_MOUNTAIN/ROOM_4_WARP"]["locations"]
    assert "ROOM_SANITY_5_WARP" in room_regions["REGION_CARROT_CASTLE/ROOM_5_WARP"]["locations"]
    assert "ROOM_SANITY_7_WARP" in room_regions["REGION_PEPPERMINT_PALACE/ROOM_7_WARP"]["locations"]
    assert "ROOM_SANITY_9_WARP" in room_regions["REGION_CANDY_CONSTELLATION/ROOM_9_WARP"]["locations"]
    assert "ROOM_SANITY_10_01" not in room_regions["REGION_DIMENSION_MIRROR/ROOM_10_01"]["locations"]
    assert "ROOM_SANITY_0_01" not in room_regions["REGION_TUTORIAL/ROOM_0_01"]["locations"]


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


def test_room_transition_overrides_are_room_local_only() -> None:
    # Transition-level gate metadata belongs in rooms.json under each room's
    # transitions list. areas.json should not carry that room graph detail.
    from ..data import load_json_data

    rooms = load_json_data("regions/rooms.json")
    areas = load_json_data("regions/areas.json")

    for room_name, room_def in rooms.items():
        assert "transitions" in room_def, f"Room {room_name} missing transitions key"
        assert isinstance(room_def["transitions"], list), (
            f"Room {room_name} transitions must be a list"
        )

    for area_name, area_def in areas.items():
        assert "transitions" not in area_def, (
            f"Area {area_name} should not have room transitions (belongs in rooms.json)"
        )


def test_logical_exit_overrides_reference_declared_exits() -> None:
    from ..data import load_json_data

    rooms = load_json_data("regions/rooms.json")

    for room_name, room_def in rooms.items():
        exits = room_def.get("exits", [])
        assert isinstance(exits, list), f"Room {room_name} exits must be a list"
        exit_set = {exit_name for exit_name in exits if isinstance(exit_name, str)}

        logical_exit_overrides = room_def.get("logical_exit_overrides", {})
        if logical_exit_overrides is None:
            logical_exit_overrides = {}
        assert isinstance(logical_exit_overrides, dict), (
            f"Room {room_name} logical_exit_overrides must be a dict when present"
        )

        missing = sorted(str(destination) for destination in logical_exit_overrides if destination not in exit_set)
        assert not missing, (
            f"Room {room_name} logical_exit_overrides includes destinations missing from exits: {missing}"
        )


def test_split_rooms_define_logical_subregion_metadata() -> None:
    from ..data import load_json_data

    rooms = load_json_data("regions/rooms.json")

    room_2_07 = rooms["REGION_MOONLIGHT_MANSION/ROOM_2_07"]
    assert room_2_07["logical_subregions"]["ENTRY_FROM_2_04"]["exits"] == [
        "REGION_MOONLIGHT_MANSION/ROOM_2_04"
    ]
    assert rooms["REGION_MOONLIGHT_MANSION/ROOM_2_04"]["logical_exit_overrides"] == {
        "REGION_MOONLIGHT_MANSION/ROOM_2_07": "ENTRY_FROM_2_04"
    }

    room_2_17 = rooms["REGION_MOONLIGHT_MANSION/ROOM_2_17"]
    assert set(room_2_17["logical_subregions"]["UPPER_HALL"]["exits"]) == {
        "REGION_MOONLIGHT_MANSION/ROOM_2_16",
        "REGION_MOONLIGHT_MANSION/ROOM_2_18",
    }
    assert set(room_2_17["logical_subregions"]["LOWER_HALL"]["exits"]) == {
        "REGION_MOONLIGHT_MANSION/ROOM_2_12",
        "REGION_MOONLIGHT_MANSION/ROOM_2_19",
    }

    room_2_goal_2 = rooms["REGION_MOONLIGHT_MANSION/ROOM_2_GOAL_2"]
    assert room_2_goal_2["logical_subregions"]["ENTRY_FROM_2_ENTRY"]["exits"] == [
        "REGION_MOONLIGHT_MANSION/ROOM_2_ENTRY"
    ]
    assert rooms["REGION_MOONLIGHT_MANSION/ROOM_2_ENTRY"]["logical_exit_overrides"] == {
        "REGION_MOONLIGHT_MANSION/ROOM_2_GOAL_2": "ENTRY_FROM_2_ENTRY"
    }

    room_9_chest_2 = rooms["REGION_CANDY_CONSTELLATION/ROOM_9_CHEST_2"]
    assert room_9_chest_2["logical_subregions"]["ENTRY_FROM_9_01"]["exits"] == [
        "REGION_CANDY_CONSTELLATION/ROOM_9_01"
    ]
    assert room_9_chest_2["logical_subregions"]["ENTRY_FROM_9_09"]["exits"] == [
        "REGION_CANDY_CONSTELLATION/ROOM_9_09"
    ]
    assert room_9_chest_2["logical_subregions"]["ENTRY_FROM_9_09"]["locations"] == [
        "SOUND_PLAYER_CHEST"
    ]
    assert rooms["REGION_CANDY_CONSTELLATION/ROOM_9_01"]["logical_exit_overrides"] == {
        "REGION_CANDY_CONSTELLATION/ROOM_9_CHEST_2": "ENTRY_FROM_9_01"
    }
    assert rooms["REGION_CANDY_CONSTELLATION/ROOM_9_09"]["logical_exit_overrides"] == {
        "REGION_CANDY_CONSTELLATION/ROOM_9_CHEST_2": "ENTRY_FROM_9_09"
    }

    room_8_07 = rooms["REGION_RADISH_RUINS/ROOM_8_07"]
    assert room_8_07["logical_subregions"]["ENTRY_FROM_8_GOAL_1"]["exits"] == [
        "REGION_RADISH_RUINS/ROOM_8_GOAL_1"
    ]
    assert set(room_8_07["logical_subregions"]["ENTRY_FROM_8_18_OR_8_21_OR_8_23"]["exits"]) == {
        "REGION_RADISH_RUINS/ROOM_8_18",
        "REGION_RADISH_RUINS/ROOM_8_21",
        "REGION_RADISH_RUINS/ROOM_8_23",
    }
    assert rooms["REGION_RADISH_RUINS/ROOM_8_GOAL_1"]["logical_exit_overrides"] == {
        "REGION_RADISH_RUINS/ROOM_8_07": "ENTRY_FROM_8_GOAL_1"
    }

    room_8_09 = rooms["REGION_RADISH_RUINS/ROOM_8_09"]
    assert room_8_09["logical_subregions"]["ENTRY_FROM_8_03"]["exits"] == [
        "REGION_RADISH_RUINS/ROOM_8_04"
    ]
    assert room_8_09["logical_subregions"]["ENTRY_FROM_8_04"]["exits"] == [
        "REGION_RADISH_RUINS/ROOM_8_03"
    ]
    assert rooms["REGION_RADISH_RUINS/ROOM_8_03"]["logical_exit_overrides"] == {
        "REGION_RADISH_RUINS/ROOM_8_09": "ENTRY_FROM_8_03"
    }
    assert rooms["REGION_RADISH_RUINS/ROOM_8_04"]["logical_exit_overrides"] == {
        "REGION_RADISH_RUINS/ROOM_8_09": "ENTRY_FROM_8_04"
    }

    room_5_13 = rooms["REGION_CARROT_CASTLE/ROOM_5_13"]
    assert room_5_13["logical_subregions"]["ENTRY_FROM_5_12"]["exits"] == [
        "REGION_CARROT_CASTLE/ROOM_5_12"
    ]
    assert set(room_5_13["logical_subregions"]["ENTRY_FROM_5_18_OR_5_WARP"]["exits"]) == {
        "REGION_CARROT_CASTLE/ROOM_5_18",
        "REGION_CARROT_CASTLE/ROOM_5_WARP",
    }
    assert rooms["REGION_CARROT_CASTLE/ROOM_5_12"]["logical_exit_overrides"] == {
        "REGION_CARROT_CASTLE/ROOM_5_13": "ENTRY_FROM_5_12"
    }
    assert rooms["REGION_CARROT_CASTLE/ROOM_5_18"]["logical_exit_overrides"] == {
        "REGION_CARROT_CASTLE/ROOM_5_13": "ENTRY_FROM_5_18_OR_5_WARP"
    }
    assert rooms["REGION_CARROT_CASTLE/ROOM_5_WARP"]["logical_exit_overrides"] == {
        "REGION_CARROT_CASTLE/ROOM_5_13": "ENTRY_FROM_5_18_OR_5_WARP"
    }

    room_6_05 = rooms["REGION_OLIVE_OCEAN/ROOM_6_05"]
    assert set(room_6_05["logical_subregions"]["ENTRY_FROM_6_04_OR_6_06"]["exits"]) == {
        "REGION_OLIVE_OCEAN/ROOM_6_04",
        "REGION_OLIVE_OCEAN/ROOM_6_06",
    }
    assert room_6_05["logical_subregions"]["ENTRY_FROM_6_04_OR_6_06"]["locations"] == [
        "MINOR_CHEST_OLIVE_OCEAN_6_05"
    ]
    assert room_6_05["logical_subregions"]["ENTRY_FROM_6_23"]["exits"] == [
        "REGION_OLIVE_OCEAN/ROOM_6_23"
    ]
    assert rooms["REGION_OLIVE_OCEAN/ROOM_6_04"]["logical_exit_overrides"] == {
        "REGION_OLIVE_OCEAN/ROOM_6_05": "ENTRY_FROM_6_04_OR_6_06"
    }
    assert rooms["REGION_OLIVE_OCEAN/ROOM_6_06"]["logical_exit_overrides"] == {
        "REGION_OLIVE_OCEAN/ROOM_6_05": "ENTRY_FROM_6_04_OR_6_06"
    }
    assert rooms["REGION_OLIVE_OCEAN/ROOM_6_23"]["logical_exit_overrides"] == {
        "REGION_OLIVE_OCEAN/ROOM_6_05": "ENTRY_FROM_6_23"
    }


def test_logical_exit_overrides_route_to_synthetic_subregions() -> None:
    from ..data import data as kirby_data

    room_2_07_from_2_04 = "REGION_MOONLIGHT_MANSION/ROOM_2_07__LOGIC__ENTRY_FROM_2_04"
    room_2_17_upper = "REGION_MOONLIGHT_MANSION/ROOM_2_17__LOGIC__UPPER_HALL"
    room_2_17_lower = "REGION_MOONLIGHT_MANSION/ROOM_2_17__LOGIC__LOWER_HALL"
    room_2_goal_2_from_entry = "REGION_MOONLIGHT_MANSION/ROOM_2_GOAL_2__LOGIC__ENTRY_FROM_2_ENTRY"
    room_9_chest_2_from_9_01 = "REGION_CANDY_CONSTELLATION/ROOM_9_CHEST_2__LOGIC__ENTRY_FROM_9_01"
    room_9_chest_2_from_9_09 = "REGION_CANDY_CONSTELLATION/ROOM_9_CHEST_2__LOGIC__ENTRY_FROM_9_09"
    room_8_07_from_goal_1 = "REGION_RADISH_RUINS/ROOM_8_07__LOGIC__ENTRY_FROM_8_GOAL_1"
    room_8_07_from_8_18_8_21_8_23 = "REGION_RADISH_RUINS/ROOM_8_07__LOGIC__ENTRY_FROM_8_18_OR_8_21_OR_8_23"
    room_8_09_from_8_03 = "REGION_RADISH_RUINS/ROOM_8_09__LOGIC__ENTRY_FROM_8_03"
    room_8_09_from_8_04 = "REGION_RADISH_RUINS/ROOM_8_09__LOGIC__ENTRY_FROM_8_04"
    room_5_13_from_5_12 = "REGION_CARROT_CASTLE/ROOM_5_13__LOGIC__ENTRY_FROM_5_12"
    room_5_13_from_5_18_or_5_warp = "REGION_CARROT_CASTLE/ROOM_5_13__LOGIC__ENTRY_FROM_5_18_OR_5_WARP"
    room_6_05_from_6_04_or_6_06 = "REGION_OLIVE_OCEAN/ROOM_6_05__LOGIC__ENTRY_FROM_6_04_OR_6_06"
    room_6_05_from_6_23 = "REGION_OLIVE_OCEAN/ROOM_6_05__LOGIC__ENTRY_FROM_6_23"

    assert room_2_07_from_2_04 in kirby_data.regions["REGION_MOONLIGHT_MANSION/ROOM_2_04"].exits
    assert kirby_data.regions[room_2_07_from_2_04].exits == ["REGION_MOONLIGHT_MANSION/ROOM_2_04"]

    assert room_2_17_lower in kirby_data.regions["REGION_MOONLIGHT_MANSION/ROOM_2_12"].exits
    assert room_2_17_upper in kirby_data.regions["REGION_MOONLIGHT_MANSION/ROOM_2_16"].exits
    assert room_2_17_lower in kirby_data.regions["REGION_MOONLIGHT_MANSION/ROOM_2_19"].exits
    assert room_2_goal_2_from_entry in kirby_data.regions["REGION_MOONLIGHT_MANSION/ROOM_2_ENTRY"].exits
    assert room_9_chest_2_from_9_01 in kirby_data.regions["REGION_CANDY_CONSTELLATION/ROOM_9_01"].exits
    assert room_9_chest_2_from_9_09 in kirby_data.regions["REGION_CANDY_CONSTELLATION/ROOM_9_09"].exits
    assert room_8_07_from_goal_1 in kirby_data.regions["REGION_RADISH_RUINS/ROOM_8_GOAL_1"].exits
    assert room_8_07_from_8_18_8_21_8_23 in kirby_data.regions["REGION_RADISH_RUINS/ROOM_8_18"].exits
    assert room_8_07_from_8_18_8_21_8_23 in kirby_data.regions["REGION_RADISH_RUINS/ROOM_8_21"].exits
    assert room_8_07_from_8_18_8_21_8_23 in kirby_data.regions["REGION_RADISH_RUINS/ROOM_8_23"].exits
    assert room_8_09_from_8_03 in kirby_data.regions["REGION_RADISH_RUINS/ROOM_8_03"].exits
    assert room_8_09_from_8_04 in kirby_data.regions["REGION_RADISH_RUINS/ROOM_8_04"].exits
    assert room_5_13_from_5_12 in kirby_data.regions["REGION_CARROT_CASTLE/ROOM_5_12"].exits
    assert room_5_13_from_5_18_or_5_warp in kirby_data.regions["REGION_CARROT_CASTLE/ROOM_5_18"].exits
    assert room_5_13_from_5_18_or_5_warp in kirby_data.regions["REGION_CARROT_CASTLE/ROOM_5_WARP"].exits
    assert room_6_05_from_6_04_or_6_06 in kirby_data.regions["REGION_OLIVE_OCEAN/ROOM_6_04"].exits
    assert room_6_05_from_6_04_or_6_06 in kirby_data.regions["REGION_OLIVE_OCEAN/ROOM_6_06"].exits
    assert room_6_05_from_6_23 in kirby_data.regions["REGION_OLIVE_OCEAN/ROOM_6_23"].exits

    assert set(kirby_data.regions[room_2_17_upper].exits) == {
        "REGION_MOONLIGHT_MANSION/ROOM_2_16",
        "REGION_MOONLIGHT_MANSION/ROOM_2_18",
    }
    assert set(kirby_data.regions[room_2_17_lower].exits) == {
        "REGION_MOONLIGHT_MANSION/ROOM_2_12",
        "REGION_MOONLIGHT_MANSION/ROOM_2_19",
    }
    assert kirby_data.regions[room_2_goal_2_from_entry].exits == ["REGION_MOONLIGHT_MANSION/ROOM_2_ENTRY"]
    assert kirby_data.regions[room_9_chest_2_from_9_01].exits == ["REGION_CANDY_CONSTELLATION/ROOM_9_01"]
    assert kirby_data.regions[room_9_chest_2_from_9_09].exits == ["REGION_CANDY_CONSTELLATION/ROOM_9_09"]
    assert kirby_data.regions[room_9_chest_2_from_9_09].locations == ["SOUND_PLAYER_CHEST"]
    assert kirby_data.regions[room_8_07_from_goal_1].exits == ["REGION_RADISH_RUINS/ROOM_8_GOAL_1"]
    assert set(kirby_data.regions[room_8_07_from_8_18_8_21_8_23].exits) == {
        "REGION_RADISH_RUINS/ROOM_8_18",
        "REGION_RADISH_RUINS/ROOM_8_21",
        "REGION_RADISH_RUINS/ROOM_8_23",
    }
    assert kirby_data.regions[room_8_09_from_8_03].exits == ["REGION_RADISH_RUINS/ROOM_8_04"]
    assert kirby_data.regions[room_8_09_from_8_04].exits == ["REGION_RADISH_RUINS/ROOM_8_03"]
    assert kirby_data.regions[room_5_13_from_5_12].exits == ["REGION_CARROT_CASTLE/ROOM_5_12"]
    assert set(kirby_data.regions[room_5_13_from_5_18_or_5_warp].exits) == {
        "REGION_CARROT_CASTLE/ROOM_5_18",
        "REGION_CARROT_CASTLE/ROOM_5_WARP",
    }
    assert set(kirby_data.regions[room_6_05_from_6_04_or_6_06].exits) == {
        "REGION_OLIVE_OCEAN/ROOM_6_04",
        "REGION_OLIVE_OCEAN/ROOM_6_06",
    }
    assert kirby_data.regions[room_6_05_from_6_04_or_6_06].locations == ["MINOR_CHEST_OLIVE_OCEAN_6_05"]
    assert kirby_data.regions[room_6_05_from_6_23].exits == ["REGION_OLIVE_OCEAN/ROOM_6_23"]


def test_stake_breaking_abilities_are_shared_and_expected() -> None:
    abilities = get_stake_breaking_abilities()

    # Keep ordering deterministic for stable behavior, but do not pin the full
    # set so stake-breaking abilities can expand over time without brittle tests.
    assert abilities == tuple(sorted(abilities))
    assert set(abilities) >= {"Hammer", "Master", "Smash", "Stone"}
    assert len(abilities) == len(set(abilities))


def test_stake_gated_transitions_include_candy_one_way_gate() -> None:
    stake_entrances = set(get_stake_gated_transition_entrance_names())

    assert "REGION_CANDY_CONSTELLATION/ROOM_9_06 -> REGION_CANDY_CONSTELLATION/ROOM_9_CHEST_1" in stake_entrances
    assert "REGION_CANDY_CONSTELLATION/ROOM_9_CHEST_1 -> REGION_CANDY_CONSTELLATION/ROOM_9_06" not in stake_entrances


def test_stake_gated_transitions_cover_cross_region_stake_rooms() -> None:
    stake_entrances = set(get_stake_gated_transition_entrance_names())

    assert "REGION_OLIVE_OCEAN/ROOM_6_15 -> REGION_OLIVE_OCEAN/ROOM_6_CHEST_2" in stake_entrances
    assert "REGION_MOONLIGHT_MANSION/ROOM_2_04 -> REGION_MOONLIGHT_MANSION/ROOM_2_GOAL_1" in stake_entrances
    assert "REGION_CANDY_CONSTELLATION/ROOM_9_HUB -> REGION_CANDY_CONSTELLATION/ROOM_9_CHEST_3" in stake_entrances


def test_stake_gated_transitions_come_from_room_transition_overrides() -> None:
    from ..data import load_json_data

    rooms_payload = load_json_data("regions/rooms.json")
    rooms = rooms_payload if isinstance(rooms_payload, dict) else {}
    annotated: set[str] = set()
    for source_room, room_data in rooms.items():
        if not isinstance(source_room, str) or not isinstance(room_data, dict):
            continue
        transitions = room_data.get("transitions", [])
        if not isinstance(transitions, list):
            continue
        for transition in transitions:
            if not isinstance(transition, dict):
                continue
            if transition.get("ability_gate") != "CanPoundPegs":
                continue
            destination_room = transition.get("destination_room")
            if isinstance(destination_room, str):
                annotated.add(f"{source_room} -> {destination_room}")

    assert annotated
    assert set(get_stake_gated_transition_entrance_names()) == annotated


def test_stake_gated_transitions_ignore_non_stake_non_exit_mismatch_warning() -> None:
    rooms_payload = {
        "REGION_TEST/ROOM_A": {
            "exits": ["REGION_TEST/ROOM_B"],
            "transitions": [
                {
                    "destination_room": "REGION_TEST/ROOM_MISSING",
                    "ability_gate": "CanCutRopes",
                },
                {
                    "destination_room": "REGION_TEST/ROOM_MISSING",
                    "ability_gate": "CanPoundPegs",
                },
            ],
        }
    }

    with patch("worlds.kirbyam.rules.load_json_data", return_value=rooms_payload), \
         patch("worlds.kirbyam.rules.logger.warning") as warning_log:
        assert get_stake_gated_transition_entrance_names() == ()
        warning_log.assert_called_once_with(
            "Stake transition override references non-exit edge: %s -> %s",
            "REGION_TEST/ROOM_A",
            "REGION_TEST/ROOM_MISSING",
        )


def test_stake_gated_transitions_handles_non_list_exits() -> None:
    rooms_payload = {
        "REGION_TEST/ROOM_A": {
            "exits": None,
            "transitions": [
                {
                    "destination_room": "REGION_TEST/ROOM_B",
                    "ability_gate": "CanPoundPegs",
                }
            ],
        }
    }

    with patch("worlds.kirbyam.rules.load_json_data", return_value=rooms_payload), \
         patch("worlds.kirbyam.rules.logger.warning") as warning_log:
        assert get_stake_gated_transition_entrance_names() == ()
        warning_log.assert_any_call(
            "Room exits payload has unexpected type for %s; treating as empty list",
            "REGION_TEST/ROOM_A",
        )


def test_lever_rooms_define_four_lever_events() -> None:
    from ..data import load_json_data

    rooms = load_json_data("regions/rooms.json")

    assert "Activate Lever - Moonlight Mansion 2-11" in rooms["REGION_MOONLIGHT_MANSION/ROOM_2_11"]["events"]
    assert "Activate Lever - Carrot Castle 5-12" in rooms["REGION_CARROT_CASTLE/ROOM_5_12"]["events"]
    assert "Activate Lever - Olive Ocean 6-13" in rooms["REGION_OLIVE_OCEAN/ROOM_6_13"]["events"]
    assert "Activate Lever - Radish Ruins 8-12" in rooms["REGION_RADISH_RUINS/ROOM_8_12"]["events"]


def test_hub_switch_locations_have_matching_big_switch_events() -> None:
    from ..data import load_json_data

    areas = load_json_data("regions/areas.json")

    expected_events_by_hub_switch = {
        "HUB_SWITCH_MUSTARD": "Activate Big Switch - Mustard Mountain",
        "HUB_SWITCH_MOONLIGHT": "Activate Big Switch - Moonlight Mansion",
        "HUB_SWITCH_CANDY": "Activate Big Switch - Candy Constellation",
        "HUB_SWITCH_OLIVE": "Activate Big Switch - Olive Ocean",
        "HUB_SWITCH_PEPPERMINT_EAST": "Activate Big Switch - Peppermint Palace East",
        "HUB_SWITCH_PEPPERMINT_WEST": "Activate Big Switch - Peppermint Palace West",
        "HUB_SWITCH_CABBAGE_CAVERN_CENTER": "Activate Big Switch - Cabbage Cavern Center",
        "HUB_SWITCH_CABBAGE_CAVERN_EAST": "Activate Big Switch - Cabbage Cavern East",
        "HUB_SWITCH_CABBAGE_CAVERN_WEST": "Activate Big Switch - Cabbage Cavern West",
        "HUB_SWITCH_CARROT": "Activate Big Switch - Carrot Castle",
        "HUB_SWITCH_RADISH": "Activate Big Switch - Radish Ruins",
        "HUB_SWITCH_RAINBOW_ROUTE_EAST": "Activate Big Switch - Rainbow Route East",
        "HUB_SWITCH_RAINBOW_ROUTE_NORTH": "Activate Big Switch - Rainbow Route North",
        "HUB_SWITCH_RAINBOW_ROUTE_SOUTH": "Activate Big Switch - Rainbow Route South",
        "HUB_SWITCH_RAINBOW_ROUTE_WEST": "Activate Big Switch - Rainbow Route West",
    }

    found_events: set[str] = set()
    for area_data in areas.values():
        if not isinstance(area_data, dict):
            continue
        locations = area_data.get("locations", [])
        events = area_data.get("events", [])
        if not isinstance(locations, list) or not isinstance(events, list):
            continue
        location_set = {location for location in locations if isinstance(location, str)}
        event_set = {event for event in events if isinstance(event, str)}
        for hub_switch_key, expected_event in expected_events_by_hub_switch.items():
            if hub_switch_key in location_set:
                assert expected_event in event_set
                found_events.add(expected_event)

    assert found_events == set(expected_events_by_hub_switch.values())
