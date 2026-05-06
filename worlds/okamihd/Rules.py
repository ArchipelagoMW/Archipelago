from rule_builder.rules import Has, And, Rule, True_, OptionFilter, Or
from worlds.AutoWorld import CollectionState
from worlds.generic.Rules import add_rule, set_rule
from .Enums.BrushTechniques import BrushTechniques
from .Enums.DivineInstruments import DivineInstruments
from .Enums.LocationType import LocationType
from .Options import ProgressiveWeapons
from .Types import LocData, ExitData, EventData
from BaseClasses import Location, Entrance, Region
from typing import TYPE_CHECKING, List, Callable, Union, Dict

from ..hk.Options import count

if TYPE_CHECKING:
    from . import OkamiWorld


def has_power_slash_level(state: CollectionState, world: "OkamiWorld", level: int) -> bool:
    return state.has(BrushTechniques.POWER_SLASH, world.player, level)


def has_cherry_bomb_level(state: CollectionState, world: "OkamiWorld", level: int) -> bool:
    return state.has(BrushTechniques.CHERRY_BOMB, world.player, level)


def has_brush_technique(state: CollectionState, world: "OkamiWorld", technique: BrushTechniques) -> bool:
    return state.has(technique, world.player)


def has_portable_fire_source(state: CollectionState, world: "OkamiWorld") -> bool:
    return state.has(DivineInstruments.SOLAR_FLARE.value.item_name, world.player)


def has_portable_thunder_source(state: CollectionState, world: "OkamiWorld") -> bool:
    return state.has(DivineInstruments.THUNDER_EDGE.value.item_name, world.player)


def has_portable_ice_source(state: CollectionState, world: "OkamiWorld") -> bool:
    return state.has(DivineInstruments.TUNDRA_BEADS.value.item_name, world.player)


def gale_shrine_access(state: CollectionState, world: "OkamiWorld") -> bool:
    return state.has_group("canine_warriors", world.player, world.options.RequiredDoggorbs.value)


def moon_cave_access(state: CollectionState, world: "OkamiWorld") -> bool:
    return state.has('Serpent Crystal', world.player)

def has_soup_ingerdients(state: CollectionState, world: "OkamiWorld", amount:int) -> bool:
    return state.has_group("soup_ingredients",world.player,amount)

def night_time_check_rule(state:CollectionState,world:"OkamiWorld")->bool:
    return state.has(BrushTechniques.CRESCENT,world.player) or not world.options.NightTimeChecksRequireCrescent

# Special Rule to handle fire with the big ball torches in Moon Cave
# Player needs to have either fire, or lit the torches by solving the sand room.
def moon_cave_fire_rule(state:CollectionState,world:"OkamiWorld")->bool:
       return has_portable_fire_source(state,world) or state.has("Moon Cave - 2F Push the ball",world.player)

# Variant for the 4F fireball room
def moon_cave_fire_rule_4f(state:CollectionState,world:"OkamiWorld")->bool:
       return has_portable_fire_source(state,world) or state.has("Moon Cave - 4F Move Fireball",world.player)


def has_divine_instrument_tier(tier: int, state: CollectionState, world: "OkamiWorld") -> Rule | True_ :
    progressive_weapon_rule = OptionFilter(ProgressiveWeapons,1) & Or(Has("Progressive Mirror", count=tier),Has("Progressive Sword", count=tier),Has("Progressive Rosary", count=tier))

    match tier:
        case 2:
            return Or(progressive_weapon_rule,)
        case _:
            return True_



def apply_event_or_location_rules(loc: Location, name: str, data: LocData | EventData, world: "OkamiWorld"):
        ## RULE BUILDER REWORK:
        # - FOR EACH LOCATION, BUILD AN ARRAY OF RULES THAT WILL BE ADDED TO THE world.set_rule(loc,AND(*Rules))

        rules : List[Rule |True_] = []


        required_techinques = []
        required_power_slash_level = data.power_slash_level
        required_cherry_bomb_level = data.cherry_bomb_level

        if len(data.mandatory_enemies) > 0:
            weapon_tier_required = 0
            for e in data.mandatory_enemies:
                weapon_tier_required = max(weapon_tier_required, e.value.required_weapon_tier)
                if len(e.value.required_techniques) > 0:
                    required_techinques += e.value.required_techniques
                if e.value.requires_slash:
                    required_power_slash_level = max(required_power_slash_level, 1)
                if e.value.requires_bomb:
                    required_cherry_bomb_level = max(required_cherry_bomb_level, 1)

            if weapon_tier_required > 0:
               rules.append( has_divine_instrument_tier(weapon_tier_required,state,world))

        required_techinques += data.required_brush_techniques

        match data.type:
            case LocationType.TREASURE_BUD:
                required_techinques += [BrushTechniques.GREENSPROUT_BLOOM]
            case LocationType.BURIED_UNDER_LEAF_PILE:
                required_techinques += [BrushTechniques.GALESTORM]
                if world.options.NightTimeChecksRequireCrescent:
                    required_techinques += [BrushTechniques.CRESCENT]
            case LocationType.BURIED_CHEST:
                if world.options.NightTimeChecksRequireCrescent:
                    required_techinques += [BrushTechniques.CRESCENT]
            case LocationType.STONE_BURIED_CHEST:
                # FIXME when dojo techniques are handled
                if world.options.NightTimeChecksRequireCrescent:
                    required_techinques += [BrushTechniques.CRESCENT]
            case LocationType.BURNING_CHEST:
                add_rule(loc, lambda state: state.has(BrushTechniques.GALESTORM, world.player)
                                            or state.has(BrushTechniques.WATERSPOUT, world.player))
            case LocationType.BURNING_CHEST_NO_WATER:
                required_techinques += [BrushTechniques.GALESTORM]
            case LocationType.UNDERWATER_CHEST:
                required_power_slash_level = max(required_power_slash_level, 1)
            case LocationType.UNDERWATER_CHEST_SHALLOW:
                add_rule(loc, lambda state: state.has(BrushTechniques.POWER_SLASH, world.player) or
                                            state.has(BrushTechniques.CHERRY_BOMB, world.player))
            case LocationType.DIGGING_MINIGAME_EARLY:
                required_power_slash_level = max(required_power_slash_level, 1)
                required_cherry_bomb_level = max(required_cherry_bomb_level, 1)
                required_techinques += [BrushTechniques.GREENSPROUT_BLOOM]
            case LocationType.DIGGING_MINIGAME_LATER:
                required_power_slash_level = max(required_power_slash_level, 1)
                required_cherry_bomb_level = max(required_cherry_bomb_level, 1)
                required_techinques += [BrushTechniques.GREENSPROUT_BLOOM, BrushTechniques.WATERSPOUT,
                                        BrushTechniques.GALESTORM]
            case LocationType.FROZEN_CHEST:
                required_techinques+=[BrushTechniques.INFERNO]

            case _:
                required_techinques+=[]


        if data.needs_long_swim:
            add_rule(loc, lambda state: (state.has("Water Tablet", world.player) or state.has(
                BrushTechniques.GREENSPROUT_WATERLILY, world.player)))

        for t in required_techinques:
            add_rule(loc, lambda state, technique=t: has_brush_technique(state, world, technique))

        if required_power_slash_level > 0:
            add_rule(loc, (lambda state, level=required_power_slash_level: has_power_slash_level(state, world, level)))

        if required_cherry_bomb_level > 0:
            add_rule(loc, (lambda state, level=required_cherry_bomb_level: has_cherry_bomb_level(state, world, level)))

        for i in data.required_items_events:
            add_rule(loc, lambda state: state.has(i, world.player))

        if data.special_rule is not None:
            # Call special rule if it's defined
            add_rule(loc, lambda state: data.special_rule(state, world))
        world.set_rule(loc,And(Has('Item'),Has('Item2')))


def apply_exit_rules(etr: Entrance, name: str, data: ExitData, world: "OkamiWorld"):
    if data.needs_long_swim:
        add_rule(etr, lambda state: (
            # Disable bc we won't randomize merchants yet
            # state.has("Water Tablet", world.player) or
            # TODO: add event here to buy the water table from its unrandomized location at the emperor's as an alternative way
            # to get this OR place locked water tablet at a standard location
            state.has(
                BrushTechniques.GREENSPROUT_WATERLILY, world.player)))

    for e in data.has_events:
        add_rule(etr, lambda state: state.has(e, world.player))


def set_rules(world: "OkamiWorld"):
    world.multiworld.completion_condition[world.player] = lambda state: state.has(
        "Moon Cave - Defeat Orochi", world.player)
    return

