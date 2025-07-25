from typing import Dict, List, NamedTuple, cast, TYPE_CHECKING
from BaseClasses import CollectionState, Entrance, Region
from worlds.oot_soh import SohWorld
from .Enums import Regions

if TYPE_CHECKING:
    from . import SohWorld

class SohRegionData(NamedTuple):
    connecting_regions: List[str] = []


region_data_table: Dict[str, SohRegionData] = {
    "Menu": SohRegionData(["Hyrule"]),
    "Hyrule": SohRegionData(),
}

class SohEntranceData(NamedTuple):
    can_pass_as_child: bool = True
    can_pass_as_adult: bool = True

entrance_data_table: Dict[str, SohEntranceData] = {

}
child_access_table: Dict[str, bool] = {}
adult_access_table: Dict[str, bool] = {}

def reset_age_access(start_as_adult: bool = False):
    for k in region_data_table.keys():
        child_access_table[k] = False
        adult_access_table[k] = False

    child_access_table[Regions.ROOT] = not start_as_adult
    adult_access_table[Regions.ROOT] = start_as_adult

reset_age_access()

#Returns whether a change was made
def update_age_access(world: "SohWorld", state: CollectionState):
    #Spread from Menu
    #If ToT accessible, spread from ToT
    #Any access at our starting age that ToT access opens up would be covered in the ToT floodfill, since if it mattered, we wouldn't reach that point
    just_found_tot = _spread_age_access(world, state, Regions.ROOT)
    if just_found_tot:
        _spread_age_access(world, state, Regions.TEMPLE_OF_TIME)

#Returns whether ToT was just found
def _spread_age_access(world: SohWorld, state: CollectionState, root: str) -> bool:
    region_list = [root]
    just_found_tot = False
    while len(region_list) > 0:
        region = world.get_region(region_list.pop())
        if child_access_table[region.name]:
            for exit in region.exits:
                #Breaks an infinite loop; this way, any cycle in the graph is broken as the boolean will have been made true
                if exit.connected_region is None or not entrance_data_table[exit.connected_region.name].can_pass_as_child or child_access_table[exit.connected_region.name]:
                    continue
                if state.can_reach_entrance(exit.name, world.player):
                    next_name = exit.connected_region.name
                    child_access_table[next_name] = True
                    if next_name not in region_list:
                        region_list.append(next_name)
                    if next_name == Regions.TEMPLE_OF_TIME: #If we just got access to ToT, we need to reset the floodfill to cover the adult side
                        #If we are in this clause, we first gained access as child, which must have been our starting age
                        adult_access_table[next_name] = True
                        just_found_tot = True
        if adult_access_table[region.name]:
            for exit in region.exits:
                #Breaks an infinite loop; this way, any cycle in the graph is broken as the boolean will have been made true
                if exit.connected_region is None or not entrance_data_table[exit.connected_region.name].can_pass_as_adult or adult_access_table[exit.connected_region.name]:
                    continue
                if state.can_reach_entrance(exit.name, world.player):
                    next_name = exit.connected_region.name
                    child_access_table[next_name] = True
                    if next_name not in region_list:
                        region_list.append(next_name)
                    if next_name == Regions.TEMPLE_OF_TIME: #If we just got access to ToT, we need to reset the floodfill to cover the child side
                        #If we're in this clause, we first gained access as adult, which must have been our starting age
                        child_access_table[next_name] = True
                        just_found_tot = True
    return just_found_tot

def can_access_region_as_child(state: CollectionState, world: SohWorld, region: Region | str) -> bool:
    if region is Region:
        region = cast(Region, region).name
    region = cast(str, region)
    return child_access_table[region] and state.can_reach_region(region, world.player)

def can_access_region_as_adult(state: CollectionState, world: SohWorld, region: Region | str) -> bool:
    if region is Region:
        region = cast(Region, region).name
    region = cast(str, region)
    return adult_access_table[region] and state.can_reach_region(region, world.player)

def can_access_entrance_as_child( state: CollectionState, world: SohWorld, entrance: Entrance | str) -> bool:
    if isinstance(entrance, Entrance):
        entrance = cast(Entrance, entrance)
        if entrance.parent_region is None:
            return False
        return entrance_data_table[entrance.name].can_pass_as_child and state.can_reach_entrance(entrance.name, world.player)\
              and can_access_region_as_child(state, world, entrance.parent_region)
    else:
        entrance = cast(str, entrance)
        return can_access_entrance_as_child(state, world, world.get_entrance(entrance))

def can_access_entrance_as_adult(state: CollectionState, world: SohWorld, entrance: Entrance | str) -> bool:
    if isinstance(entrance, Entrance):
        entrance = cast(Entrance, entrance)
        if entrance.parent_region is None:
            return False
        return entrance_data_table[entrance.name].can_pass_as_adult and state.can_reach_entrance(entrance.name, world.player) \
              and can_access_region_as_adult(state, world, entrance.parent_region)
    else:
        entrance = cast(str, entrance)
        return can_access_entrance_as_adult(state, world, world.get_entrance(entrance))