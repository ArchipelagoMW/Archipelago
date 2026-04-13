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

    # Cross-area mirror connections derived from transitions.json.
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
    # Exactly 22 rooms carry locations (9 major chests + 5 vitality/sound + 8 boss defeats)
    assert len(rooms_with_locations) == 22, (
        f"Expected 22 rooms with locations, got {len(rooms_with_locations)}: {list(rooms_with_locations.keys())}"
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
    assert room_regions["REGION_RAINBOW_ROUTE/ROOM_1_CENTRAL_CIRCLE"]["locations"] == regions_before["REGION_RAINBOW_ROUTE/ROOM_1_CENTRAL_CIRCLE"]
    
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


def test_region_ability_gate_annotations_load_for_future_big_chest_rollout() -> None:
    # ability_gates has moved from areas.json /MAIN regions to rooms.json room entries.
    # Each room carries an ability_gates dict (empty by default; populated when gate
    # evidence is confirmed for that specific room).  Areas no longer carry this metadata.
    from ..data import load_json_data

    rooms = load_json_data("regions/rooms.json")
    areas = load_json_data("regions/areas.json")

    for room_name, room_def in rooms.items():
        assert "ability_gates" in room_def, f"Room {room_name} missing ability_gates key"
        assert isinstance(room_def["ability_gates"], dict), (
            f"Room {room_name} ability_gates must be a dict"
        )

    for area_name, area_def in areas.items():
        assert "ability_gates" not in area_def, (
            f"Area {area_name} should not have ability_gates (belongs in rooms.json)"
        )

