"""Logic rules for Kirby & The Amazing Mirror.

This implementation is intentionally minimal while the world data model and
client/ROM integration are still in flux.

Current rules:
    - Access to Rainbow Route's connected area graph starts from REGION_GAME_START,
            which now only feeds the Rainbow Route hub.
    - Access to the Dimension Mirror region from Rainbow Route requires collecting
            all 8 Mirror Shards (implemented as 8 progression items).
        - Within the Dimension Mirror:
            * Defeat Dark Meta Knight (Dimension Mirror) is an event available once
                the region is entered (no additional items required beyond the shards gate).
            * Defeat Dark Mind goal location requires: all 8 shards + DMK event.
        - Completion conditions:
            * Dark Mind: collect Defeat Dark Mind.

NOTE: Dark Mind is modeled as an explicit AP goal location.
The client reports this goal location from native AI-state signals and sends
CLIENT_GOAL after server acknowledgement of the selected goal location check.
"""

from __future__ import annotations

from collections import deque
from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import forbid_items_for_player, set_rule

from .data import LocationCategory, data
from .generation_logging import logger
from .groups import resolve_item_group
from .options import Goal

if TYPE_CHECKING:
    from . import KirbyAmWorld


_SHARD_ITEM_LABELS = [
    "Mustard Mountain - Mirror Shard",
    "Moonlight Mansion - Mirror Shard",
    "Candy Constellation - Mirror Shard",
    "Olive Ocean - Mirror Shard",
    "Peppermint Palace - Mirror Shard",
    "Cabbage Cavern - Mirror Shard",
    "Carrot Castle - Mirror Shard",
    "Radish Ruins - Mirror Shard",
]

_GOAL_LOCATION_LABELS = {
    Goal.option_dark_mind: "Defeat Dark Mind",
}

_DMK_DIMENSION_MIRROR_EVENT = "Defeat Dark Meta Knight (Dimension Mirror)"
_ABILITY_GATE_STATUS_VALUES = frozenset({"confirmed", "semantic_candidate", "unconfirmed"})

# These gates intentionally default to True until ability items/statues become
# part of the item pool. The names match the planned logic categories from #37.
_ABILITY_GATE_PLACEHOLDER_SOURCES = {
    "CanCutRopes": frozenset({"Cutter", "Sword", "Cupid", "Smash", "Master"}),
    "CanBreakBlocks": frozenset({"Hammer", "Stone", "Throw", "Burning", "Missile", "UFO", "Smash", "Master"}),
    "CanUseMini": frozenset({"Mini"}),
    "CanLightFuses": frozenset({"Fire", "Burning", "Bomb", "Laser", "UFO", "Master"}),
    "CanPoundPegs": frozenset({"Hammer", "Stone", "Smash", "Master"}),
}


def _has_all_shards(state: CollectionState, player: int) -> bool:
    return state.has_from_list_unique(_SHARD_ITEM_LABELS, player, len(_SHARD_ITEM_LABELS))


def _allow_pending_ability_gate(_state: CollectionState, _player: int, _gate_name: str) -> bool:
    return True


def can_cut_ropes(state: CollectionState, player: int) -> bool:
    return _allow_pending_ability_gate(state, player, "CanCutRopes")


def can_break_blocks(state: CollectionState, player: int) -> bool:
    return _allow_pending_ability_gate(state, player, "CanBreakBlocks")


def can_use_mini(state: CollectionState, player: int) -> bool:
    return _allow_pending_ability_gate(state, player, "CanUseMini")


def can_light_fuses(state: CollectionState, player: int) -> bool:
    return _allow_pending_ability_gate(state, player, "CanLightFuses")


def can_pound_pegs(state: CollectionState, player: int) -> bool:
    return _allow_pending_ability_gate(state, player, "CanPoundPegs")


CanCutRopes = can_cut_ropes
CanBreakBlocks = can_break_blocks
CanUseMini = can_use_mini
CanLightFuses = can_light_fuses
CanPoundPegs = can_pound_pegs


ABILITY_GATE_RULES = {
    "CanCutRopes": can_cut_ropes,
    "CanBreakBlocks": can_break_blocks,
    "CanUseMini": can_use_mini,
    "CanLightFuses": can_light_fuses,
    "CanPoundPegs": can_pound_pegs,
}


def get_region_ability_gate_annotations() -> dict[str, dict[str, dict[str, object]]]:
    annotations: dict[str, dict[str, dict[str, object]]] = {}
    for region_name, region_data in data.regions.items():
        if region_data.ability_gates:
            annotations[region_name] = region_data.ability_gates
    return annotations


def set_rules(world: KirbyAmWorld) -> None:
    shard_gate_rule = lambda state: _has_all_shards(state, world.player)

    item_name_groups = getattr(world, "item_name_groups", {})
    shard_items = resolve_item_group(item_name_groups, "Shards", default=_SHARD_ITEM_LABELS)
    get_locations = getattr(world.multiworld, "get_locations", None)
    if callable(get_locations):
        for location in get_locations(world.player):
            key = getattr(location, "key", None)
            if key is None:
                continue
            loc_meta = data.locations.get(key)
            if loc_meta is None or loc_meta.category != LocationCategory.BOSS_DEFEAT:
                continue
            forbid_items_for_player(location, shard_items, world.player)

    # Completion condition
    goal_label = _GOAL_LOCATION_LABELS.get(world.options.goal.value, "Defeat Dark Mind")
    if world.options.goal.value not in _GOAL_LOCATION_LABELS:
        logger.warning(
            "[P%s] Unknown goal value %s; defaulting to %s",
            world.player,
            world.options.goal.value,
            goal_label,
        )
    else:
        logger.debug("[P%s] Goal mode %s: require %s", world.player, world.options.goal.value, goal_label)
    world.multiworld.completion_condition[world.player] = (
        lambda state, required_goal=goal_label: state.has(required_goal, world.player)
    )

    # Region gating: the name is generated by regions.create_regions()
    entrance_name = "REGION_RAINBOW_ROUTE/MAIN -> REGION_DIMENSION_MIRROR/MAIN"
    try:
        entrance = world.multiworld.get_entrance(entrance_name, world.player)
        set_rule(entrance, shard_gate_rule)
    except KeyError:
        # If the entrance doesn't exist yet (during early iteration), don't block generation.
        logger.debug(
            "[P%s] Entrance %r not found; skipping Dimension Mirror shard gate",
            world.player,
            entrance_name,
        )

    for goal_location_name in _GOAL_LOCATION_LABELS.values():
        try:
            goal_location = world.multiworld.get_location(goal_location_name, world.player)
            # Sequenced after Dark Meta Knight within the Dimension Mirror.
            dmk_rule = lambda state: (
                _has_all_shards(state, world.player)
                and state.has(_DMK_DIMENSION_MIRROR_EVENT, world.player)
            )
            set_rule(goal_location, dmk_rule)
        except KeyError:
            logger.warning(
                "[P%s] Goal location %s not found; Dark Meta Knight requirement not applied to this goal",
                world.player,
                goal_location_name,
            )


# ============================================================================
# Room Graph Reachability Queries
# ============================================================================
# rooms.json defines room connectivity and may include non-room-sanity locations
# (for example, boss/chest ownership). Room-sanity binding remains optional.
# These functions allow querying which rooms are reachable from which other rooms.
# The location binding (room-sanity checks) is separate and optional.


def _get_room_graph() -> dict[str, dict]:
    """Load room topology data used for reachability queries."""
    from .data import load_json_data
    return load_json_data("regions/rooms.json")


def _reachable_rooms_from(
    start_region: str,
    graph: dict[str, dict] | None = None,
) -> set[str]:
    """
    BFS to find all rooms reachable from a given start region.
    
    Args:
        start_region: The starting room region name (e.g., "REGION_RAINBOW_ROUTE/ROOM_1_01").
        graph: The room graph dict. If None, loads from data.
    
    Returns:
        Set of all reachable room region names.
    """
    if graph is None:
        graph = _get_room_graph()
    
    visited = set()
    queued = {start_region}
    queue = deque([start_region])
    
    while queue:
        current = queue.popleft()
        if current in visited:
            continue
        if current not in graph:
            continue
        
        visited.add(current)
        for next_room in graph[current].get("exits", []):
            if next_room not in visited and next_room not in queued:
                queue.append(next_room)
                queued.add(next_room)
    
    return visited


def _bind_room_sanity_locations(
    world_regions: dict,
    enable_room_sanity: bool = True,
) -> None:
    """
    Optionally bind room-sanity locations to room regions.
    
    Room topology may include non-room-sanity locations; this function selectively
    attaches ROOM_SANITY_* locations to their corresponding room regions.
    
    Args:
        world_regions: The regions dict loaded from data files.
        enable_room_sanity: If True, load and bind room-sanity locations to rooms.
    """
    if not enable_room_sanity:
        return
    
    from .data import load_json_data
    import re
    
    room_regions_topology = load_json_data("regions/rooms.json")

    # Bind each room_sanity-enabled room region to its ROOM_SANITY_* location key.
    for region_name, region_def in room_regions_topology.items():
        if not isinstance(region_def, dict):
            continue
        room_meta = region_def.get("room_sanity")
        if not isinstance(room_meta, dict) or not bool(room_meta.get("included", False)):
            continue

        match = re.match(r"REGION_[A-Z_]+/ROOM_(\d+)_(\d+)$", region_name)
        if not match:
            continue

        area_code = int(match.group(1))
        room_code = int(match.group(2))
        location_name = f"ROOM_SANITY_{area_code}_{room_code:02d}"

        if region_name in world_regions:
            if "locations" not in world_regions[region_name]:
                world_regions[region_name]["locations"] = []
            if location_name not in world_regions[region_name]["locations"]:
                world_regions[region_name]["locations"].append(location_name)
