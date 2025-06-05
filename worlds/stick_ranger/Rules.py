from typing import TYPE_CHECKING, Callable, Dict, List

from BaseClasses import CollectionState, MultiWorld
from worlds.generic.Rules import set_rule

from .Constants import GOAL_EXIT_LOCATIONS, RANGER_CLASSES
from .Items import unlocks_by_region
from .Options import SROptions

if TYPE_CHECKING:
    from . import StickRanger


def class_count(state, player) -> int:
    """Return the number of ranger classes the player has unlocked."""
    return sum(
        state.has(f"Unlock {cls} Class", player)
        for cls in RANGER_CLASSES
    )

def reached_castle(player, threshold, req_classes) -> Callable[[CollectionState], bool]:
    """Return whether or not the player has unlocked access to the Castle stage yet."""
    return lambda state, _pl=player, _T=threshold, _keys=unlocks_by_region["Grassland"]: (
        state.has("Unlock Castle", _pl, 1)
        and sum(1 for k in _keys if state.has(k, _pl, 1)) >= _T
        and class_count(state, _pl) >= req_classes
    )

def reached_submarine_shrine(player, castle_pred, threshold, req_classes) -> Callable[[CollectionState], bool]:
    """Return whether or not the player has unlocked access to the Submarine Shrine stage yet."""
    return lambda state, _pl=player, _T=threshold, _keys=unlocks_by_region["Sea"], _c=castle_pred: (
        _c(state)
        and state.has("Unlock Submarine Shrine", _pl, 1)
        and sum(1 for k in _keys if state.has(k, _pl, 1)) >= _T
        and class_count(state, _pl) >= req_classes
    )

def reached_pyramid(player, submarine_shrine_pred, threshold, req_classes) -> Callable[[CollectionState], bool]:
    """Return whether or not the player has unlocked access to the Pyramid stage yet."""
    return lambda state, _pl=player, _T=threshold, _keys=unlocks_by_region["Desert"], _s=submarine_shrine_pred: (
        _s(state)
        and state.has("Unlock Pyramid", _pl, 1)
        and sum(1 for k in _keys if state.has(k, _pl, 1)) >= _T
        and class_count(state, _pl) >= req_classes
    )

def reached_ice_castle(player, pyramid_pred, threshold, req_classes) -> Callable[[CollectionState], bool]:
    """Return whether or not the player has unlocked access to the Ice Castle stage yet."""
    return lambda state, _pl=player, _T=threshold, _keys=unlocks_by_region["Ice"], _p=pyramid_pred: (
        _p(state)
        and state.has("Unlock Ice Castle", _pl, 1)
        and sum(1 for k in _keys if state.has(k, _pl, 1)) >= _T
        and class_count(state, _pl) >= req_classes
    )

def reached_hell_castle(player, ice_castle_pred, threshold, req_classes) -> Callable[[CollectionState], bool]:
    """Return whether or not the player has unlocked access to the Hell Castle stage yet."""
    return lambda state, _pl=player, _T=threshold, _keys=unlocks_by_region["Hell"], _i=ice_castle_pred: (
        _i(state)
        and state.has("Unlock Hell Castle", _pl, 1)
        and sum(1 for k in _keys if state.has(k, _pl, 1)) >= _T
        and class_count(state, _pl) >= req_classes
    )

def set_region_rules(player, multiworld, boss_stage_reqs) -> None:
    """
    Sets region rules for every stage, except every stage before the Castle stage.
    This ensures players can beat the levels they unlock and make for a nice progression feeling.
    """
    castle_predicate: Callable[[CollectionState], bool] = reached_castle(
        player, multiworld.random.randint(6, 10), boss_stage_reqs["Castle"]
        )
    set_rule(multiworld.get_entrance("Castle", player), castle_predicate)

    submarine_shrine_predicate: Callable[[CollectionState], bool] = reached_submarine_shrine(
        player, castle_predicate, multiworld.random.randint(4, 7), boss_stage_reqs["Submarine Shrine"]
        )
    set_rule(multiworld.get_entrance("Submarine Shrine", player), submarine_shrine_predicate)

    pyramid_predicate: Callable[[CollectionState], bool] = reached_pyramid(
        player, submarine_shrine_predicate, multiworld.random.randint(4, 7), boss_stage_reqs["Pyramid"]
        )
    set_rule(multiworld.get_entrance("Pyramid", player), pyramid_predicate)

    ice_castle_predicate: Callable[[CollectionState], bool] = reached_ice_castle(
        player, pyramid_predicate, multiworld.random.randint(5, 8), boss_stage_reqs["Ice Castle"]
        )
    set_rule(multiworld.get_entrance("Ice Castle", player), ice_castle_predicate)

    hell_castle_predicate: Callable[[CollectionState], bool] = reached_hell_castle(
        player, ice_castle_predicate, multiworld.random.randint(6, 10), boss_stage_reqs["Hell Castle"]
        )
    set_rule(multiworld.get_entrance("Hell Castle", player), hell_castle_predicate)
    set_rule(multiworld.get_entrance("Volcano", player), hell_castle_predicate)
    set_rule(multiworld.get_entrance("Mountaintop", player), hell_castle_predicate)

    for unlock_name in unlocks_by_region["Sea"]:
        entrance_name = multiworld.get_entrance(unlock_name.replace("Unlock ", ""), player)
        set_rule(entrance_name, lambda state, _pl=player, _nm=unlock_name, _c=castle_predicate:
            state.has(_nm, _pl, 1) and _c(state)
        )

    for unlock_name in unlocks_by_region["Desert"]:
        entrance_name = multiworld.get_entrance(unlock_name.replace("Unlock ", ""), player)
        set_rule(entrance_name, lambda state, _pl=player, _nm=unlock_name, _s=submarine_shrine_predicate:
            state.has(_nm, _pl, 1) and _s(state)
        )

    for unlock_name in unlocks_by_region["Ice"]:
        entrance_name = multiworld.get_entrance(unlock_name.replace("Unlock ", ""), player)
        set_rule(entrance_name, lambda state, _pl=player, _nm=unlock_name, _p=pyramid_predicate:
            state.has(_nm, _pl, 1) and _p(state)
        )

    for unlock_name in unlocks_by_region["Hell"]:
        entrance_name = multiworld.get_entrance(unlock_name.replace("Unlock ", ""), player)
        set_rule(entrance_name, lambda state, _pl=player, _nm=unlock_name, _i=ice_castle_predicate:
            state.has(_nm, _pl, 1) and _i(state)
        )

def set_rules(self: "StickRanger") -> None:
    options: SROptions = self.options
    multiworld: MultiWorld = self.multiworld
    player: int = self.player

    goal_exit_names: List[str] = GOAL_EXIT_LOCATIONS[options.goal.value]
    multiworld.completion_condition[player] = (
        lambda state: all(
            state.can_reach(loc, "Location", player) for loc in goal_exit_names
        )
    )

    boss_stage_requirements: Dict[str, int] = {
        "Castle": options.classes_req_for_castle.value,
        "Submarine Shrine": options.classes_req_for_submarine_shrine.value,
        "Pyramid": options.classes_req_for_pyramid.value,
        "Ice Castle": options.classes_req_for_ice_castle.value,
        "Hell Castle": options.classes_req_for_hell_castle.value,
    }

    if not options.ranger_class_randomizer.value:
        for stage in boss_stage_requirements:
            boss_stage_requirements[stage] = 0

    order: List[str] = ["Castle", "Submarine Shrine", "Pyramid", "Ice Castle", "Hell Castle"]
    for previous, next in zip(order, order[1:]):
        boss_stage_requirements[next] = max(boss_stage_requirements[previous], boss_stage_requirements[next])

    set_region_rules(self.player, self.multiworld, boss_stage_requirements)