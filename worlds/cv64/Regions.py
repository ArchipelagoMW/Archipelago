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
    gate_0_region = create_region(world, player, active_locations, 'Gate 0', None, None)
    gate_1_region = create_region(world, player, active_locations, 'Gate 1', None, None)
    gate_2_region = create_region(world, player, active_locations, 'Gate 2', None, None)
    gate_3_region = create_region(world, player, active_locations, 'Gate 3', None, None)
    gate_4_region = create_region(world, player, active_locations, 'Gate 4', None, None)
    gate_5_region = create_region(world, player, active_locations, 'Gate 5', None, None)
    gate_6_region = create_region(world, player, active_locations, 'Gate 6', None, None)
    gate_7_region = create_region(world, player, active_locations, 'Gate 7', None, None)

    # Forest of Silence regions

    forest_start_region_locations = [
        LocationName.forest_main_torch1,
        LocationName.forest_main_torch2,
        LocationName.forest_main_torch3,
        LocationName.forest_main_torch4,
        LocationName.forest_main_torch5,
        LocationName.forest_main_torch6,
        LocationName.forest_main_torch7,
        LocationName.forest_main_torch8,
        LocationName.forest_main_torch9,
        LocationName.forest_main_torch10,
        LocationName.forest_main_torch11,
        LocationName.forest_main_torch12,
        LocationName.forest_main_torch13,
        LocationName.forest_main_torch14,
        LocationName.forest_main_torch15,
        LocationName.forest_main_torch16,
        LocationName.forest_main_torch17,
        LocationName.forest_main_torch18,
        LocationName.forest_main_torch19,
        LocationName.forest_main_torch20,
    ]
    forest_start_region = create_region(world, player, active_locations, LocationName.forest_of_silence,
                                        forest_start_region_locations, None)


    # Castle Wall regions

    cw_main_region_locations = [
        LocationName.cw_main_torch1,
        LocationName.cw_main_torch4,
        LocationName.cw_main_torch5,
        LocationName.cw_main_torch6,
        LocationName.cw_main_torch7,
    ]
    cw_start_region = create_region(world, player, active_locations, LocationName.castle_wall,
                                    cw_main_region_locations, None)

    cw_ltower_region_locations = [
        LocationName.cw_main_torch2,
        LocationName.cw_main_torch3,
        LocationName.cw_main_torch8,
        LocationName.the_end
    ]
    cw_ltower_region = create_region(world, player, active_locations, LocationName.cw_ltower,
                                     cw_ltower_region_locations, None)


    # Set up the regions correctly.
    world.regions += [
        menu_region,
        # gate_0_region,
        # gate_1_region,
        # gate_2_region,
        # gate_3_region,
        # gate_4_region,
        # gate_5_region,
        # gate_6_region,
        # gate_7_region,
        forest_start_region,
        cw_start_region,
        cw_ltower_region,
    ]


def connect_regions(world, player):
    names: typing.Dict[str, int] = {}

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
