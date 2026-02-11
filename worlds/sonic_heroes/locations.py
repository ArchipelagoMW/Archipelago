"""
Location Handling Here
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from worlds.sonic_heroes import SonicHeroesWorld

from BaseClasses import Location, LocationProgressType
from .constants import *


class SonicHeroesLocation(Location):
    """
    Location Class for Sonic Heroes.
    """
    game = SONICHEROES


def create_locations(world, region):
    """
    Creates locations for Sonic Heroes.
    """
    if region.name in world.region_to_location.keys():
        for loc in world.region_to_location[region.name]:
            #rule = None
            rule = world.full_logic_mapping_dict[loc.rulestr]


            """
            if loc.team in world.logic_mapping_dict.keys():
                if loc.level in world.logic_mapping_dict[loc.team].keys():
                    if loc.rulestr in world.logic_mapping_dict[loc.team][loc.level].keys():
                        rule = world.logic_mapping_dict[loc.team][loc.level][loc.rulestr]
                    else:
                        #print(f"Loc {loc.name} is missing the logic mapping for rulestr "
                              #f"{loc.rulestr} with team {loc.team} and level {loc.level}")
                        pass
                else:
                    #print(f"Loc {loc.name} is missing the logic mapping for level"
                          #f" {loc.level} with team {loc.team} and rulestr {loc.rulestr}")
                    pass
            else:
                #print(f"Loc {loc.name} is missing the logic mapping for team {loc.team} with "
                      #f"rulestr {loc.rulestr} and level {loc.level}")
                pass
            """
            create_location(world, region, loc.name, loc.code, rule)


def create_location(world: SonicHeroesWorld, region, name, code, rule=None):
    """
    Creates a location for Sonic Heroes.
    """
    #print(f"Creating location {name}")
    loc = Location(world.player, name, code, region)
    loc.access_rule = rule

    #for boss_name in sonic_heroes_extra_names.values():
        #if boss_name in name:
            #print(f"Creating Boss Location {name}")

    if loc.name == METALOVERLORD:
        #print(f"Setting {loc.name} to Excluded")
        loc.progress_type = LocationProgressType.EXCLUDED

    #for level in emerald_levels:
        #if f"{level} {constants.EMERALD}" == loc.name:
            #if world.options.goal_unlock_condition.value != 0 and world.options.ability_unlocks.value != 1:
                #loc.progress_type = LocationProgressType.PRIORITY
                #pass
            #else:
                #print("Unable to Set Emerald Location as Priority Due to Options")
                #pass
        #pass

    #print(f"Creating Location {name} for region {region.name}")

    region.locations.append(loc)
