import typing

from BaseClasses import MultiWorld, Region, Entrance
from .Items import CV64Item
from .Locations import CV64Location
from .Names import LocationName, ItemName
from .Rom import rom_loc_offsets


class LevelGate:
    gate_levels: typing.List[int]
    gate_emblem_count: int

    def __init__(self, emblems):
        self.gate_emblem_count = emblems
        self.gate_levels = list()


shuffleable_regions = [
    LocationName.forest_of_silence,
    LocationName.castle_wall,
    LocationName.villa,
    LocationName.tunnel,
    LocationName.underground_waterway,
    LocationName.castle_center,
    LocationName.duel_tower,
    LocationName.tower_of_execution,
    LocationName.tower_of_science,
    LocationName.tower_of_sorcery,
    LocationName.room_of_clocks,
    LocationName.clock_tower,
]


def create_regions(world, player: int, active_locations):
    menu_region = create_region(world, player, active_locations, 'Menu', None, None)
    warp2_region = create_region(world, player, active_locations, 'Warp 2', None, None)
    warp3_region = create_region(world, player, active_locations, 'Warp 3', None, None)
    warp4_region = create_region(world, player, active_locations, 'Warp 4', None, None)
    warp5_region = create_region(world, player, active_locations, 'Warp 5', None, None)
    warp6_region = create_region(world, player, active_locations, 'Warp 6', None, None)
    warp7_region = create_region(world, player, active_locations, 'Warp 7', None, None)
    warp8_region = create_region(world, player, active_locations, 'Warp 8', None, None)

    # Forest of Silence regions
    forest_start_region_locations = [
        LocationName.forest_pillars_right,
        LocationName.forest_pillars_top,
        LocationName.forest_bone_mom,
        LocationName.forest_lgaz_in,
        LocationName.forest_lgaz_top,
        LocationName.forest_hgaz_in,
        LocationName.forest_hgaz_top,
        LocationName.forest_weretiger_sw,
        LocationName.forest_weretiger_gate,
        LocationName.forest_dirge_tomb,
        LocationName.forest_corpse_save,
        LocationName.forest_dbridge_wall,
        LocationName.forest_dbridge_sw,
        LocationName.forest_dbridge_gate_r,
        LocationName.forest_dbridge_tomb,
        LocationName.forest_bface_tomb,
        LocationName.forest_ibridge,
        LocationName.forest_werewolf_tomb,
        LocationName.forest_werewolf_tree,
        LocationName.forest_final_sw,
    ]
    forest_start_region = create_region(world, player, active_locations, LocationName.forest_of_silence,
                                        forest_start_region_locations, None)

    # Castle Wall regions
    cw_main_region_locations = [
        LocationName.cw_bottom_middle,
        LocationName.cw_rrampart,
        LocationName.cw_lrampart,
        LocationName.cw_dragon_sw,
        LocationName.cwr_bottom,
    ]
    cw_start_region = create_region(world, player, active_locations, LocationName.castle_wall,
                                    cw_main_region_locations, None)

    cw_ltower_region_locations = [
        LocationName.cw_drac_sw,
        LocationName.cwl_bottom,
        LocationName.cwl_bridge,
        LocationName.the_end
    ]
    cw_ltower_region = create_region(world, player, active_locations, LocationName.cw_ltower,
                                     cw_ltower_region_locations, None)


    # Set up the regions correctly.
    world.regions += [
        menu_region,
        warp2_region,
        warp3_region,
        warp4_region,
        warp5_region,
        warp6_region,
        warp7_region,
        warp8_region,
        forest_start_region,
        cw_start_region,
        cw_ltower_region,
    ]


def connect_regions(world, player):
    names: typing.Dict[str, int] = {}
    connect(world, player, names, 'Menu', 'Warp 2',
            lambda state: (state.has(ItemName.special_two + 3, player)))

    connect(world, player, names, 'Menu', LocationName.forest_of_silence)

    connect(world, player, names, LocationName.forest_of_silence, LocationName.castle_wall)

    connect(world, player, names, LocationName.castle_wall, LocationName.cw_ltower,
            lambda state: (state.has(ItemName.left_tower_key, player)))


def create_region(world: MultiWorld, player: int, active_locations, name: str, locations=None, exits=None):
    # Shamelessly stolen from the SA2B definition, which was in turn shamelessly stolen from the ROR2 definition.
    # Perhaps one day the chain will continue?
    ret = Region(name, None, name, player)
    ret.world = world
    if locations:
        for location in locations:
            loc_id = active_locations.get(location, 0)
            if loc_id:
                location = CV64Location(player, location, loc_id, ret)
                if loc_id != 0xC64000:
                    location.rom_offset = rom_loc_offsets[loc_id]
                ret.locations.append(location)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, exit, ret))

    return ret


def connect(world: MultiWorld, player: int, used_names: typing.Dict[str, int], source: str, target: str,
            rule: typing.Optional[typing.Callable] = None):
    source_region = world.get_region(source, player)
    target_region = world.get_region(target, player)

    if target not in used_names:
        used_names[target] = 1
        name = target
    else:
        used_names[target] += 1
        name = target + (' ' * used_names[target])

    connection = Entrance(player, name, source_region)

    if rule:
        connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)
