from worlds.AutoWorld import CollectionState
from worlds.generic.Rules import add_rule, set_rule
from .Types import LocData, ExitData, BrushTechniques, BrushTechniqueData
from BaseClasses import Location, Entrance, Region
from typing import TYPE_CHECKING, List, Callable, Union, Dict

if TYPE_CHECKING:
    from . import OkamiWorld


def has_power_slash_level(state: CollectionState, world: "OkamiWorld", level: int) -> bool:
    return state.has(BrushTechniques.POWER_SLASH.value.item_name, world.player, level)


def has_cherry_bomb_level(state: CollectionState, world: "OkamiWorld", level: int) -> bool:
    return state.has("0", world.player, level)


def has_brush_technique(state: CollectionState, world: "OkamiWorld", technique: BrushTechniques) -> bool:
    return state.has(technique.value.item_name, world.player)


def apply_event_or_location_rules(loc: Location, name: str, data: LocData, world: "OkamiWorld"):
    #  if not is_location_valid(world, name):
    #     return
    for t in data.required_brush_techniques:
        add_rule(loc, lambda state, technique=t: has_brush_technique(state, world, technique))

    if data.power_slash_level > 0:
        add_rule(loc, (lambda state, level=data.power_slash_level: has_power_slash_level(state, world, level)))

    if data.cherry_bomb_level > 0:
        add_rule(loc, (lambda state, level=data.power_slash_level: has_cherry_bomb_level(state, world, level)))
    if data.buried_chest == 1 and world.options.BuriedChestsByNight==1 :
        add_rule(loc,lambda state : state.has(BrushTechniques.CRESCENT.value.item_name,world.player))


def apply_exit_rules(etr: Entrance, name: str, data: ExitData, world: "OkamiWorld"):
    if data.needs_swim:
        add_rule(etr, lambda state: (state.has("Water Tablet", world.player) or state.has(BrushTechniques.GREENSPROUT_WATERLILY.value.item_name,world.player)))

    for e in data.has_events:
        add_rule(etr, lambda state: state.has(e, world.player))

    for e in data.doesnt_have_events:
        add_rule(etr, lambda state: not state.has(e, world.player))


def set_rules(world: "OkamiWorld"):
    world.multiworld.completion_condition[world.player] = lambda state: state.has("End for now", world.player)
    return
    # set_specific_rules(world)

    # set_event_rules(world)
