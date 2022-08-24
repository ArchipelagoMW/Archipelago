import typing

from BaseClasses import MultiWorld, Region, Entrance
from .Items import CV64Item
from .Locations import CV64Location
from .Names import LocationName, ItemName


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
    ]
    forest_start_region = create_region(world, player, active_locations, LocationName.forest_of_silence,
                                        forest_start_region_locations, None)

    forest_switch1_region_locations = [
        LocationName.forest_main_torch4,
        LocationName.forest_main_torch5,
        LocationName.forest_main_torch6,
        LocationName.forest_main_torch7,
        LocationName.forest_main_torch8,
    ]
    forest_switch1_region = create_region(world, player, active_locations, LocationName.forest_switch1,
                                          forest_switch1_region_locations, None)

    forest_switch2_region_locations = [
        LocationName.forest_main_torch9,
        LocationName.forest_main_torch10,
        LocationName.forest_main_torch11,
        LocationName.forest_main_torch12,
        LocationName.forest_main_torch13,
    ]
    forest_switch2_region = create_region(world, player, active_locations, LocationName.forest_switch2,
                                          forest_switch2_region_locations, None)

    forest_switch3_region_locations = [
        LocationName.forest_main_torch14,
        LocationName.forest_main_torch15,
        LocationName.forest_main_torch16,
        LocationName.forest_main_torch17,
        LocationName.forest_main_torch18,
        LocationName.forest_main_torch19,
        LocationName.forest_main_torch20,
    ]
    forest_switch3_region = create_region(world, player, active_locations, LocationName.forest_switch3,
                                          forest_switch3_region_locations, None)

    forest_end_region_locations = []
    forest_end_region = create_region(world, player, active_locations, LocationName.forest_end,
                                      forest_end_region_locations, None)

    # Castle Wall regions

    cw_start_region_locations = []
    cw_start_region = create_region(world, player, active_locations, LocationName.castle_wall,
                                    cw_start_region_locations, None)

    cw_exit_region_locations = [
        LocationName.cw_main_torch4
    ]
    cw_exit_region = create_region(world, player, active_locations, LocationName.cw_exit,
                                   cw_exit_region_locations, None)

    cw_descent_region_locations = [
        LocationName.cw_main_torch5,
        LocationName.cw_main_torch6
    ]
    cw_descent_region = create_region(world, player, active_locations, LocationName.cw_descent,
                                      cw_descent_region_locations, None)

    cw_bone_dragon_region_locations = [
        LocationName.cw_main_torch7
    ]
    cw_bone_dragon_region = create_region(world, player, active_locations, LocationName.cw_bd_switch,
                                          cw_bone_dragon_region_locations, None)

    cw_dracula_region_locations = [
        LocationName.cw_main_torch8
    ]
    cw_dracula_region = create_region(world, player, active_locations, LocationName.cw_drac_switch,
                                      cw_dracula_region_locations, None)

    cw_rtower_region_locations = [
        LocationName.cw_main_torch1
    ]
    cw_rtower_region = create_region(world, player, active_locations, LocationName.cw_rtower,
                                     cw_rtower_region_locations, None)

    cw_ltower_region_locations = [
        LocationName.cw_main_torch2,
        LocationName.cw_main_torch3
    ]
    cw_ltower_region = create_region(world, player, active_locations, LocationName.cw_ltower,
                                     cw_ltower_region_locations, None)

    villa_start_region_locations = [
        LocationName.the_end
    ]
    villa_start_region = create_region(world, player, active_locations, LocationName.villa,
                                       villa_start_region_locations, None)

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
        forest_switch1_region,
        forest_switch2_region,
        forest_switch3_region,
        forest_end_region,
        cw_start_region,
        cw_exit_region,
        cw_bone_dragon_region,
        cw_dracula_region,
        cw_rtower_region,
        cw_ltower_region,
        villa_start_region
    ]


def connect_regions(world, player, gates: typing.List[LevelGate], cannon_core_emblems, gate_bosses):
    names: typing.Dict[str, int] = {}

    connect(world, player, names, 'Menu', LocationName.forest_of_silence)
    connect(world, player, names, LocationName.forest_of_silence, LocationName.forest_switch1)
    connect(world, player, names, LocationName.forest_switch1, LocationName.forest_switch2)
    connect(world, player, names, LocationName.forest_switch3, LocationName.forest_switch3)
    connect(world, player, names, LocationName.forest_switch3, LocationName.forest_end)
    connect(world, player, names, LocationName.forest_end, LocationName.castle_wall)
    connect(world, player, names, LocationName.castle_wall, LocationName.cw_rtower)
    connect(world, player, names, LocationName.cw_rtower, LocationName.cw_bd_switch)
    connect(world, player, names, LocationName.cw_bd_switch, LocationName.cw_descent)
    connect(world, player, names, LocationName.cw_bd_switch, LocationName.cw_exit)
    connect(world, player, names, LocationName.cw_descent, LocationName.castle_wall)
    connect(world, player, names, LocationName.castle_wall, LocationName.cw_ltower,
            lambda state: (state.has(ItemName.left_tower_key, player)))
    connect(world, player, names, LocationName.cw_ltower, LocationName.cw_drac_switch)
    connect(world, player, names, LocationName.cw_drac_switch, LocationName.cw_descent)
    connect(world, player, names, LocationName.cw_exit, LocationName.villa,
            lambda state: (state.can_reach(LocationName.cw_drac_switch, player)))


def create_region(world: MultiWorld, player: int, active_locations, name: str, locations=None, exits=None):
    # Shamelessly stolen from the SA2B definition, which was in turn shamelessly stolen from the ROR2 definition.
    # Anyone want to continue the chain?
    ret = Region(name, None, name, player)
    ret.world = world
    if locations:
        for location in locations:
            loc_id = active_locations.get(location, 0)
            if loc_id:
                location = CV64Location(player, location, loc_id, ret)
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
