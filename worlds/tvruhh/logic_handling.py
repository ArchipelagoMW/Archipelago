from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location, Entrance, Region

from . import locations, items

if TYPE_CHECKING:
    from .world import TVRUHHWorld

class TVRUHHLocation(Location):
    game = "TVRUHH"


# list of tags:
# "grind" - indicates if the location is a grind, applies to cumulative things
# "very_grind" - indicates if the location is extremely grindy, applies to cumulative things
# "tedious" - indicates if the location is tedious, applies to difficult things
# "very_tedious" - indicates if the location is extremely tedious, applies to very difficult things
# "defect" - indicates if the location requires Defect
# "twin" - indicates if the location requires Twin
# "devil" - indicates if the location requires Devil
# "alt_her" - indicates if the location requires Alter Blank
# "alt_defect" - indicates if the location requires Alter Defect
# "alt_twin" - indicates if the location requires Alter Twin
# "alt_devil" - indicates if the location requires Alter Devil
# "heavy_rain" - indicates if the location requires Heavy Rain (for Story)
# "torr_rain" - indicates if the location requires Torrential Rain (for Story)
# "quickplay" - indicates if the location requires Quickplay
# "ult_quick" - indicates if the location requires Ultra Quickplay
# "alt_story" - indicates if the location requires Alter Story
# "towers" - indicates if the location requires The Towers
# "endless" - indicates if the location requires Endless Stress
# "endl_terror" - indicates if the location requires Endless Terror
# "has_m_amount", {count} - indicates if the location requires more than a certain amount of monsters
# "has_specif_m", "{monster}"  - indicates if the location requires a specific monster unlocked
# "has_mf", "{monster family}", [count] - inidicates if the location requires all monsters or a given amount from a specific family
# ""
# =======================================================================================================
#  keep in mind some locations will not need any tags, because they are handled individually in rules.py
# =======================================================================================================

def logic_remover(world:TVRUHHWorld,check_list: list):
    return_list = check_list
    for x in check_list:
        if not world.options.grindy_dreams and locations.locations_to_tags[x].__contains__("grind"):
            return_list.remove(x)
        if not world.options.tedious_dreams and locations.locations_to_tags[x].__contains__("tedious"):
            return_list.remove(x)
        if not world.options.extremely_grindy_dreams and locations.locations_to_tags[x].__contains__("very_grind"):
            return_list.remove(x)
        if not world.options.extremely_tedious_dreams and locations.locations_to_tags[x].__contains__("very_tedious"):
            return_list.remove(x)
    
    return return_list


def logic_placer(world:TVRUHHWorld,location_list:dict,listtype:str):
    if listtype == "dreams":
        y = location_list.copy()
        for x in y:
            if locations.locations_to_tags[x].__contains__("quickplay"):
                world.get_region("Unlocked Quickplay").add_locations({x: location_list[x]},TVRUHHLocation)
                location_list.pop(x)
            if locations.locations_to_tags[x].__contains__("alter_story"):
                world.get_region("Unlocked Quickplay").add_locations({x: location_list[x]},TVRUHHLocation)
                location_list.pop(x)
            if locations.locations_to_tags[x].__contains__("has_specif_m") and locations.locations_to_tags[x].__contains__("quickplay"):
                world.get_region("(QP) Monster Unlocked " + locations.locations_to_tags[x][int(locations.locations_to_tags[x].index("has_specif_m"))+1]).add_locations({x: location_list[x]}, TVRUHHLocation)
                location_list.pop(x)
            elif locations.locations_to_tags[x].__contains__("has_specif_m"):
                world.get_region("(start) Monster Unlocked " + locations.locations_to_tags[x][int(locations.locations_to_tags[x].index("has_specif_m"))+1]).add_locations({x: location_list[x]}, TVRUHHLocation)
                location_list.pop(x)
            if locations.locations_to_tags[x].__contains__("has_m_amount"):
                world.multiworld.regions.append(Region("Monsters Unlocked " + str(locations.locations_to_tags[x][int(locations.locations_to_tags[x].index("has_m_amount"))+1]),world.player,world.multiworld))
                world.get_region("Start").connect(world.get_region("Monsters Unlocked " + str(locations.locations_to_tags[x][int(locations.locations_to_tags[x].index("has_m_amount"))+1])), "Start to " + str(locations.locations_to_tags[x][int(locations.locations_to_tags[x].index("has_m_amount"))+1]) + " Monsters", lambda state: state.has_from_list(items.monster_list, world.player, locations.locations_to_tags[x][int(locations.locations_to_tags[x].index("has_m_amount"))+1]))
                world.get_region("Monsters Unlocked " + str(locations.locations_to_tags[x][int(locations.locations_to_tags[x].index("has_m_amount"))+1])).add_locations({x: location_list[x]}, TVRUHHLocation)
                location_list.pop(x)
        world.get_region("Start").add_locations(location_list,TVRUHHLocation)
    elif listtype == "qp_medal":
        y = location_list.copy()
        for x in y:
            if locations.locations_to_tags[x].__contains__("has_specif_m"):
                world.get_region("(QP) Monster Unlocked " + locations.locations_to_tags[x][int(locations.locations_to_tags[x].index("has_specif_m"))+1]).add_locations({x: location_list[x]}, TVRUHHLocation)
                location_list.pop(x)
        world.get_region("Unlocked Quickplay").add_locations(location_list,TVRUHHLocation)