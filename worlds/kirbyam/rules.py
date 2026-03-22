"""Logic rules for Kirby & The Amazing Mirror.

This implementation is intentionally minimal while the world data model and
client/ROM integration are still in flux.

Current rules:
  - Access to the Dimension Mirror region requires collecting all 8 Mirror Shards
    (implemented as 8 progression items).
  - Within the Dimension Mirror:
      * Defeat Dark Meta Knight (Dimension Mirror) is an event available once
        the region is entered (no additional items required beyond the shards gate).
      * Defeat Dark Mind goal location requires: all 8 shards + DMK event.
      * 100% Save File goal location requires: all 8 shards (shard gate only).
  - Completion conditions:
        * Dark Mind: collect Defeat Dark Mind.
        * 100%: collect 100% Save File.
        * DEBUG: always completable.

NOTE: Dark Mind and 100% are modeled as explicit AP goal locations.
The client reports these goal locations from native AI-state signals and sends
CLIENT_GOAL after server acknowledgement of the selected goal location check.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import set_rule

from .data import data
from .generation_logging import logger
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
    Goal.option_100: "100% Save File",
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

    # Completion condition
    if world.options.goal.value == Goal.option_debug:
        logger.debug("[P%s] Goal mode DEBUG: completion always true", world.player)
        world.multiworld.completion_condition[world.player] = lambda _state: True
    else:
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
    entrance_name = "REGION_GAME_START -> REGION_DIMENSION_MIRROR/MAIN"
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
            if goal_location_name == "Defeat Dark Mind":
                # Sequenced after Dark Meta Knight within the Dimension Mirror.
                dmk_rule = lambda state: (
                    _has_all_shards(state, world.player)
                    and state.has(_DMK_DIMENSION_MIRROR_EVENT, world.player)
                )
                set_rule(goal_location, dmk_rule)
            else:
                set_rule(goal_location, shard_gate_rule)
        except KeyError:
            logger.warning(
                "[P%s] Goal location %s not found; shard gate not applied to this goal",
                world.player,
                goal_location_name,
            )
