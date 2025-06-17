from worlds.AutoWorld import CollectionState
from worlds.generic.Rules import add_rule, set_rule
from .Types import LocData, ExitData, BrushTechniques, DivineInstruments, EventData
from BaseClasses import Location, Entrance, Region
from typing import TYPE_CHECKING, List, Callable, Union, Dict

if TYPE_CHECKING:
    from . import OkamiWorld


def has_power_slash_level(state: CollectionState, world: "OkamiWorld", level: int) -> bool:
    return state.has(BrushTechniques.POWER_SLASH.value.item_name, world.player, level)


def has_cherry_bomb_level(state: CollectionState, world: "OkamiWorld", level: int) -> bool:
    return state.has(BrushTechniques.CHERRY_BOMB.value.item_name, world.player, level)


def has_brush_technique(state: CollectionState, world: "OkamiWorld", technique: BrushTechniques) -> bool:
    return state.has(technique.value.item_name, world.player)


#def has_portable_fire_source(state: CollectionState, world: "OkamiWorld") -> bool:
#    return state.has(DivineInstruments.SOLAR_FLARE.value.item_name, world.player)


#def has_portable_thunder_source(state: CollectionState, world: "OkamiWorld") -> bool:
#    return state.has(DivineInstruments.THUNDER_EDGE.value.item_name, world.player)


#def has_portable_ice_source(state: CollectionState, world: "OkamiWorld") -> bool:
#    return state.has(DivineInstruments.TUNDRA_BEADS.value.item_name, world.player)


def has_divine_instrument_tier(tier: int, state: CollectionState, world: "OkamiWorld") -> bool:
    match tier:
        case 1:
            return state.has_group('divine_instrument', world.player, 1)
        case 2:
            return (state.has_group('divine_instrument_tier_2', world.player, 1) or
                    state.has_group('divine_instrument_tier_3', world.player, 1) or
                    state.has_group('divine_instrument_tier_4', world.player, 1) or
                    state.has_group('divine_instrument_tier_5', world.player, 1))
        case 3:
            return (state.has_group('divine_instrument_tier_3', world.player, 1) or
                    state.has_group('divine_instrument_tier_4', world.player, 1) or
                    state.has_group('divine_instrument_tier_5', world.player, 1))
        case 4:
            return (state.has_group('divine_instrument_tier_4', world.player, 1) or
                    state.has_group('divine_instrument_tier_5', world.player, 1))
        case 5:
            return state.has_group('divine_instrument_tier_5', world.player, 1)


def apply_event_or_location_rules(loc: Location, name: str, data: LocData | EventData, world: "OkamiWorld"):
    required_techinques = []

    if len(data.mandatory_enemies) > 0:
        weapon_tier_required = 0
        for e in data.mandatory_enemies:
            weapon_tier_required = max(weapon_tier_required, e.value.required_weapon_tier)
            if len(e.value.required_techniques) > 0:
                required_techinques += e.value.required_techniques
        if weapon_tier_required > 0:
            add_rule(loc,
                     lambda state, level=weapon_tier_required: has_divine_instrument_tier(weapon_tier_required, state,
                                                                                          world))
    required_techinques += data.required_brush_techniques

    # Might do multiples checks on certain techniques, not sure yet if that's a issue or not.
    for t in required_techinques:
        add_rule(loc, lambda state, technique=t: has_brush_technique(state, world, technique))

    if data.power_slash_level > 0:
        add_rule(loc, (lambda state, level=data.power_slash_level: has_power_slash_level(state, world, level)))

    if data.cherry_bomb_level > 0:
        add_rule(loc, (lambda state, level=data.cherry_bomb_level: has_cherry_bomb_level(state, world, level)))

    if data.buried == 1 and world.options.BuriedChestsByNight == 1:
        add_rule(loc, lambda state: state.has(BrushTechniques.CRESCENT.value.item_name, world.player))

    for e in data.has_events:
        add_rule(loc, lambda state: state.has(e, world.player))

    for i in data.required_items:
        add_rule(loc, lambda state: state.has(i, world.player))

    if data.needs_swim:
        add_rule(loc, lambda state: (state.has("Water Tablet", world.player) or state.has(
            BrushTechniques.GREENSPROUT_WATERLILY.value.item_name, world.player)))


def apply_exit_rules(etr: Entrance, name: str, data: ExitData, world: "OkamiWorld"):
    if data.needs_swim:
        add_rule(etr, lambda state: (
                # Disable bc we won't randomize merchants yet
                #state.has("Water Tablet", world.player) or
                #TODO: add event here to buy the water table from its unrandomized location at the emperor's as an alternative way
                # to get this OR place locked water tablet at a standard location
                state.has(
            BrushTechniques.GREENSPROUT_WATERLILY.value.item_name, world.player)))

    for e in data.has_events:
        add_rule(etr, lambda state: state.has(e, world.player))

    for e in data.doesnt_have_events:
        add_rule(etr, lambda state: not state.has(e, world.player))


def set_rules(world: "OkamiWorld"):
    world.multiworld.completion_condition[world.player] = lambda state: state.has(
         "Agata Forest - Open Ruins Door", world.player)
    return
    # set_specific_rules(world)

    # set_event_rules(world)
