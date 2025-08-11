from typing import TYPE_CHECKING
from BaseClasses import CollectionState

from .Locations import LMLocation
from worlds.generic.Rules import add_rule

if TYPE_CHECKING:
    from . import LMWorld

FIRE_SPIRIT_SPOT = ("1F Hallway",
                    "Study",
                    "Butler's Room",
                    "Cold Storage",
                    "Mirror Room",
                    "Dining Room",
                    "2F Rear Hallway",
                    "Sitting Room",
                    "Graveyard",
                    "Roof")

WATER_SPIRIT_SPOT = ("Kitchen",
                     "Boneyard",
                     "Courtyard",
                     "1F Bathroom",
                     "2F Washroom",
                     "Sitting Room")

ICE_SPIRIT_SPOT = ("Kitchen",
                   "Pipe Room",
                   "Tea Room",
                   "Ceramics Studio")


def set_element_rules(world: "LMWorld", location: LMLocation, use_enemizer: bool):
    region = location.region
    if len(location.access) != 0:
        for item in location.access:
            if item == "Fire Element Medal":
                add_rule(location, lambda state: can_fst_fire(state, world.player), "and")
            elif item == "Water Element Medal":
                add_rule(location, lambda state: can_fst_water(state, world.player), "and")
            elif item == "Ice Element Medal":
                add_rule(location, lambda state: can_fst_ice(state, world.player), "and")
            else:
                add_rule(location, lambda state, i=item: state.has(i, world.player), "and")

    if use_enemizer:
        if region in world.ghost_affected_regions.keys() and location != "Uncle Grimmly, Hermit of the Darkness":
            # if fire, require water
            if world.ghost_affected_regions[region] == "Fire":
                add_rule(location, lambda state: can_fst_water(state, world.player), "and")
            # if water, require ice
            elif world.ghost_affected_regions[region] == "Water":
                add_rule(location, lambda state: can_fst_ice(state, world.player), "and")
            # if ice, require fire
            elif world.ghost_affected_regions[region] == "Ice":
                add_rule(location, lambda state: can_fst_fire(state, world.player), "and")
            else:
                pass

def can_fst_fire(state: CollectionState, player: int):
    return (state.has("Fire Element Medal", player) and state.has("Progressive Vacuum", player)
                                                    and (state.can_reach_region("1F Hallway", player) or
                                                        state.can_reach_region("Study", player) or
                                                        state.can_reach_region("Butler's Room", player) or
                                                        state.can_reach_region("Cold Storage", player) or
                                                        state.can_reach_region("Mirror Room", player) or
                                                        state.can_reach_region("Dining Room", player) or
                                                        state.can_reach_region("2F Rear Hallway", player) or
                                                        state.can_reach_region("Sitting Room", player) or
                                                        state.can_reach_region("Graveyard", player) or
                                                        state.can_reach_region("Roof", player)))


def can_fst_water(state, player):
    return (state.has("Water Element Medal", player) and state.has("Progressive Vacuum", player) and
                                                        (state.can_reach_region("Kitchen", player) or
                                                         state.can_reach_region("Boneyard", player) or
                                                         state.can_reach_region("Courtyard", player) or
                                                         state.can_reach_region("1F Bathroom", player) or
                                                         state.can_reach_region("2F Washroom", player) or
                                                         state.can_reach_region("Sitting Room", player)))


def can_fst_ice(state, player):
    return (state.has("Ice Element Medal", player) and state.has("Progressive Vacuum", player)
                                                    and (state.can_reach_region("Kitchen", player) or
                                                       state.can_reach_region("Pipe Room", player) or
                                                       state.can_reach_region("Tea Room", player) or
                                                       state.can_reach_region("Ceramics Studio", player)))

