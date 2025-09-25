from typing import Dict, List, NamedTuple, cast, TYPE_CHECKING
from BaseClasses import CollectionState, Entrance, Region
from .Enums import Regions

if TYPE_CHECKING:
    from . import SohWorld

class SohRegionData(NamedTuple):
    connecting_regions: List[str] = []

def double_link_regions(world: "SohWorld", region1: str, region2: str):
    world.get_region(region1).connect(world.get_region(region2))
    world.get_region(region2).connect(world.get_region(region1))

region_data_table: Dict[str, SohRegionData] = {
    Regions.ROOT.value: SohRegionData([Regions.KF_LINKS_HOUSE.value]),

    # Kokiri Forest
    Regions.KOKIRI_FOREST.value: SohRegionData([]),
    Regions.KF_OUTSIDE_DEKU_TREE.value: SohRegionData([]),
    Regions.KF_LINKS_HOUSE.value: SohRegionData([Regions.ROOT.value, Regions.DEKU_TREE_ENTRYWAY.value, Regions.DODONGOS_CAVERN_ENTRYWAY.value]),
    Regions.KF_MIDOS_HOUSE.value: SohRegionData([]),
    Regions.KF_SARIAS_HOUSE.value: SohRegionData([]),
    Regions.KF_HOUSE_OF_TWINS.value: SohRegionData([]),
    Regions.KF_KNOW_IT_ALL_HOUSE.value: SohRegionData([]),
    Regions.KF_KOKIRI_SHOP.value: SohRegionData([]),
    Regions.KF_STORMS_GROTTO.value: SohRegionData([]),

    # Lost Woods
    Regions.LW_FOREST_EXIT.value: SohRegionData([]),
    Regions.THE_LOST_WOODS.value: SohRegionData([]),
    Regions.LW_BEYOND_MIDO.value: SohRegionData([]),
    Regions.LW_NEAR_SHORTCUTS_GROTTO.value: SohRegionData([]),
    Regions.DEKU_THEATER.value: SohRegionData([]),
    Regions.LW_SCRUBS_GROTTO.value: SohRegionData([]),
    Regions.LW_BRIDGE_FROM_FOREST.value: SohRegionData([]),
    Regions.LW_BRIDGE.value: SohRegionData([]),

    # Hyrule Field
    Regions.HYRULE_FIELD.value: SohRegionData([]),
    Regions.HF_SOUTHEAST_GROTTO.value: SohRegionData([]),
    Regions.HF_OPEN_GROTTO.value: SohRegionData([]),
    Regions.HF_INSIDE_FENCE_GROTTO.value: SohRegionData([]),
    Regions.HF_COW_GROTTO.value: SohRegionData([]),
    Regions.HF_COW_GROTTO_BEHIND_WEBS.value: SohRegionData([]),
    Regions.HF_NEAR_MARKET_GROTTO.value: SohRegionData([]),
    Regions.HF_FAIRY_GROTTO.value: SohRegionData([]),
    Regions.HF_NEAR_KAK_GROTTO.value: SohRegionData([]),
    Regions.HF_TEKTITE_GROTTO.value: SohRegionData([]),

    # Market
    Regions.MARKET_ENTRANCE.value: SohRegionData([]),
    Regions.THE_MARKET.value: SohRegionData([]),
    Regions.MARKET_BACK_ALLEY.value: SohRegionData([]),
    Regions.MARKET_GUARD_HOUSE.value: SohRegionData([]),
    Regions.MARKET_BAZAAR.value: SohRegionData([]),
    Regions.MARKET_MASK_SHOP.value: SohRegionData([]),
    Regions.MARKET_SHOOTING_GALLERY.value: SohRegionData([]),
    Regions.MARKET_BOMBCHU_BOWLING.value: SohRegionData([]),
    Regions.MARKET_POTION_SHOP.value: SohRegionData([]),
    Regions.MARKET_TREASURE_CHEST_GAME.value: SohRegionData([]),
    Regions.MARKET_BOMBCHU_SHOP.value: SohRegionData([]),
    Regions.MARKET_DOG_LADY_HOUSE.value: SohRegionData([]),
    Regions.MARKET_MAN_IN_GREEN_HOUSE.value: SohRegionData([]),

    # Temple of Time
    Regions.TOT_ENTRANCE.value: SohRegionData([]),
    Regions.TEMPLE_OF_TIME.value: SohRegionData([]),
    Regions.TOT_BEYOND_DOOR_OF_TIME.value: SohRegionData([]),

    # Deku Tree
    Regions.DEKU_TREE_ENTRYWAY.value: SohRegionData([Regions.KF_LINKS_HOUSE.value]),
    Regions.DEKU_TREE_LOBBY.value: SohRegionData([]),
    Regions.DEKU_TREE_2F_MIDDLE_ROOM.value: SohRegionData([]),
    Regions.DEKU_TREE_SLINGSHOT_ROOM.value: SohRegionData([]),
    Regions.DEKU_TREE_COMPASS_ROOM.value: SohRegionData([]),
    Regions.DEKU_TREE_BASEMENT_LOWER.value: SohRegionData([]),
    Regions.DEKU_TREE_BASEMENT_SCRUB_ROOM.value: SohRegionData([]),
    Regions.DEKU_TREE_BASEMENT_WATER_ROOM_FRONT.value: SohRegionData([]),
    Regions.DEKU_TREE_BASEMENT_WATER_ROOM_BACK.value: SohRegionData([]),
    Regions.DEKU_TREE_BASEMENT_TORCH_ROOM.value: SohRegionData([]),
    Regions.DEKU_TREE_BASEMENT_BACK_LOBBY.value: SohRegionData([]),
    Regions.DEKU_TREE_BASEMENT_BACK_ROOM.value: SohRegionData([]),
    Regions.DEKU_TREE_BASEMENT_UPPER.value: SohRegionData([]),
    Regions.DEKU_TREE_OUTSIDE_BOSS_ROOM.value: SohRegionData([]),
    Regions.DEKU_TREE_BOSS_ENTRYWAY.value: SohRegionData([]),
    Regions.DEKU_TREE_BOSS_EXIT.value: SohRegionData([]),
    Regions.DEKU_TREE_BOSS_ROOM.value: SohRegionData([]),

    # Dodongo's Cavern
    Regions.DODONGOS_CAVERN_ENTRYWAY.value: SohRegionData([Regions.KF_LINKS_HOUSE.value]),
    Regions.DODONGOS_CAVERN_BEGINNING.value: SohRegionData([]),
    Regions.DODONGOS_CAVERN_LOBBY.value: SohRegionData([]),
    Regions.DODONGOS_CAVERN_LOBBY_SWITCH.value: SohRegionData([]),
    Regions.DODONGOS_CAVERN_SE_CORRIDOR.value: SohRegionData([]),
    Regions.DODONGOS_CAVERN_SE_ROOM.value: SohRegionData([]),
    Regions.DODONGOS_CAVERN_NEAR_LOWER_LIZALFOS.value: SohRegionData([]),
    Regions.DODONGOS_CAVERN_LOWER_LIZALFOS.value: SohRegionData([]),
    Regions.DODONGOS_CAVERN_DODONGO_ROOM.value: SohRegionData([]),
    Regions.DODONGOS_CAVERN_NEAR_DODONGO_ROOM.value: SohRegionData([]),
    Regions.DODONGOS_CAVERN_STAIRS_LOWER.value: SohRegionData([]),
    Regions.DODONGOS_CAVERN_STAIRS_UPPER.value: SohRegionData([]),
    Regions.DODONGOS_CAVERN_COMPASS_ROOM.value: SohRegionData([]),
    Regions.DODONGOS_CAVERN_ARMOS_ROOM.value: SohRegionData([]),
    Regions.DODONGOS_CAVERN_BOMB_ROOM_LOWER.value: SohRegionData([]),
    Regions.DODONGOS_CAVERN_2F_SIDE_ROOM.value: SohRegionData([]),
    Regions.DODONGOS_CAVERN_FIRST_SLINGSHOT_ROOM.value: SohRegionData([]),
    Regions.DODONGOS_CAVERN_UPPER_LIZALFOS.value: SohRegionData([]),
    Regions.DODONGOS_CAVERN_SECOND_SLINGSHOT_ROOM.value: SohRegionData([]),
    Regions.DODONGOS_CAVERN_BOMB_ROOM_UPPER.value: SohRegionData([]),
    Regions.DODONGOS_CAVERN_FAR_BRIDGE.value: SohRegionData([]),
    Regions.DODONGOS_CAVERN_BOSS_AREA.value: SohRegionData([]),
    Regions.DODONGOS_CAVERN_BACK_ROOM.value: SohRegionData([]),
    Regions.DODONGOS_CAVERN_BOSS_ENTRYWAY.value: SohRegionData([]),
    Regions.DODONGOS_CAVERN_BOSS_ROOM.value: SohRegionData([]),

    # Ganon's Castle
    Regions.GANONS_CASTLE_ENTRYWAY.value: SohRegionData([]),
    Regions.GANONS_CASTLE_LOBBY.value: SohRegionData([]),
    Regions.GANONS_CASTLE_DEKU_SCRUBS.value: SohRegionData([]),
    Regions.GANONS_CASTLE_FOREST_TRIAL.value: SohRegionData([]),
    Regions.GANONS_CASTLE_FIRE_TRIAL.value: SohRegionData([]),
    Regions.GANONS_CASTLE_WATER_TRIAL.value: SohRegionData([]),
    Regions.GANONS_CASTLE_SHADOW_TRIAL.value: SohRegionData([]),
    Regions.GANONS_CASTLE_SPIRIT_TRIAL.value: SohRegionData([]),
    Regions.GANONS_CASTLE_LIGHT_TRIAL.value: SohRegionData([]),
    Regions.GANONS_TOWER_ENTRYWAY.value: SohRegionData([]),
    Regions.GANONS_TOWER_FLOOR_1.value: SohRegionData([]),
    Regions.GANONS_TOWER_FLOOR_2.value: SohRegionData([]),
    Regions.GANONS_TOWER_FLOOR_3.value: SohRegionData([]),
    Regions.GANONS_TOWER_BEFORE_GANONDORF_LAIR.value: SohRegionData([]),
    Regions.GANONS_TOWER_GANONDORF_LAIR.value: SohRegionData([]),
    Regions.GANONS_CASTLE_ESCAPE.value: SohRegionData([]),
    Regions.GANONS_CASTLE_GANON_ARENA.value: SohRegionData([]),
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

    child_access_table[Regions.ROOT.value] = not start_as_adult
    adult_access_table[Regions.ROOT.value] = start_as_adult

reset_age_access()

# Returns whether a change was made
def update_age_access(world: "SohWorld", state: CollectionState):
    # Spread from Menu
    # If ToT accessible, spread from ToT
    # Any access at our starting age that ToT access opens up would be covered in the ToT floodfill, since if it mattered, we wouldn't reach that point
    just_found_tot = _spread_age_access(world, state, Regions.ROOT.value)
    if just_found_tot: # As said, if we just found ToT, we probably need to do a floodfill from there
        _spread_age_access(world, state, Regions.TEMPLE_OF_TIME.value)

# Returns whether ToT was just found
def _spread_age_access(world: "SohWorld", state: CollectionState, root: str) -> bool:
    region_list = [root]
    just_found_tot = False
    while len(region_list) > 0:
        region = world.get_region(region_list.pop())
        if child_access_table[region.name]:
            for exit in region.exits:
                # The last part breaks an infinite loop; this way, any cycle in the graph is broken as the boolean will have been made true
                if exit.connected_region is None or (exit.name in entrance_data_table and not entrance_data_table[exit.name].can_pass_as_child) \
                    or (exit.connected_region.name in child_access_table and child_access_table[exit.connected_region.name]):
                    continue
                if state.can_reach_entrance(exit.name, world.player):
                    next_name = exit.connected_region.name
                    child_access_table[next_name] = True
                    if next_name not in region_list:
                        region_list.append(next_name)
                    if next_name == Regions.TEMPLE_OF_TIME.value: # If we just got access to ToT, we need to reset the floodfill to cover the adult side
                        # If we are in this clause, we first gained access as child, which must have been our starting age
                        adult_access_table[next_name] = True
                        just_found_tot = True
        if adult_access_table[region.name]:
            for exit in region.exits:
                # The last part breaks an infinite loop; this way, any cycle in the graph is broken as the boolean will have been made true
                if exit.connected_region is None or (exit.name in entrance_data_table and not entrance_data_table[exit.name].can_pass_as_adult) \
                    or (exit.connected_region.name in adult_access_table and adult_access_table[exit.connected_region.name]):
                    continue
                if state.can_reach_entrance(exit.name, world.player):
                    next_name = exit.connected_region.name
                    child_access_table[next_name] = True
                    if next_name not in region_list:
                        region_list.append(next_name)
                    if next_name == Regions.TEMPLE_OF_TIME.value: # If we just got access to ToT, we need to reset the floodfill to cover the child side
                        # If we're in this clause, we first gained access as adult, which must have been our starting age
                        child_access_table[next_name] = True
                        just_found_tot = True
    return just_found_tot

def can_access_region_as_child(state: CollectionState, world: "SohWorld", region: Region | str) -> bool:
    if region is Region:
        region = cast(Region, region).name
    region = cast(str, region)
    return region in child_access_table and child_access_table[region] and state.can_reach_region(region, world.player)

def can_access_region_as_adult(state: CollectionState, world: "SohWorld", region: Region | str) -> bool:
    if region is Region:
        region = cast(Region, region).name
    region = cast(str, region)
    return region in adult_access_table and adult_access_table[region] and state.can_reach_region(region, world.player)

def can_access_entrance_as_child( state: CollectionState, world: "SohWorld", entrance: Entrance | str) -> bool:
    if isinstance(entrance, Entrance):
        entrance = cast(Entrance, entrance)
        if entrance.parent_region is None:
            return False
        return entrance.name in entrance_data_table and entrance_data_table[entrance.name].can_pass_as_child and state.can_reach_entrance(entrance.name, world.player)\
              and can_access_region_as_child(state, world, entrance.parent_region)
    else:
        entrance = cast(str, entrance)
        return can_access_entrance_as_child(state, world, world.get_entrance(entrance))

def can_access_entrance_as_adult(state: CollectionState, world: "SohWorld", entrance: Entrance | str) -> bool:
    if isinstance(entrance, Entrance):
        entrance = cast(Entrance, entrance)
        if entrance.parent_region is None:
            return False
        return entrance.name in entrance_data_table and entrance_data_table[entrance.name].can_pass_as_adult and state.can_reach_entrance(entrance.name, world.player) \
              and can_access_region_as_adult(state, world, entrance.parent_region)
    else:
        entrance = cast(str, entrance)
        return can_access_entrance_as_adult(state, world, world.get_entrance(entrance))
