import typing

from BaseClasses import MultiWorld, Region, RegionType, Entrance
from .Locations import YILocation
from .Names import LocationName, ItemName
from ..generic.Rules import add_rule, set_rule

def create_regions(world, player: int, active_locations):
    menu_region = create_region(world, player, active_locations, 'Menu', None)

    world1_region = create_region(world, player, active_locations, LocationName.world1_region, None)
    world2_region = create_region(world, player, active_locations, LocationName.world2_region, None)
    world3_region = create_region(world, player, active_locations, LocationName.world3_region, None)
    world4_region = create_region(world, player, active_locations, LocationName.world4_region, None)
    world5_region = create_region(world, player, active_locations, LocationName.world5_region, None)
    world6_region = create_region(world, player, active_locations, LocationName.world6_region, None)

    w1_l1_tile = create_region(world, player, active_locations, LocationName.w1_l1_tile, None)
    w1_l1_region = create_region(world, player, active_locations, LocationName.w1_l1_region, None)
    W1_L1_flowers = create_region(world, player, active_locations, LocationName.W1_L1_flowers, None)

    W6_L8_clear = create_region(world, player, active_locations, LocationName.W6_L8_clear, None)


    world.regions += [
        menu_region,
        world1_region,
        world2_region,
        world3_region,
        world4_region,
        world5_region,
        world6_region,
        w1_l1_tile,
        w1_l1_region,
        W1_L1_flowers,
        W6_L8_clear,
    ]


def connect_regions(world, player, level_to_tile_dict):
    names: typing.Dict[str, int] = {}

    connect(world, player, names, "Menu", LocationName.world1_region)
    connect(world, player, names, LocationName.world1_region, LocationName.w1_l1_tile)
    connect(world, player, names, LocationName.world1_region, LocationName.world6_region)


    connect(world, player, names, LocationName.w1_l1_region, LocationName.W1_L1_flowers)


def create_region(world: MultiWorld, player: int, active_locations, name: str, locations=None):
    ret = Region(name, RegionType.Generic, name, player)
    ret.world = world
    if locations:
        for locationName in locations:
            loc_id = active_locations.get(locationName, 0)
            if loc_id:
                location = YILocation(player, locationName, loc_id, ret)
                ret.locations.append(Location)
    return ret


def add_location_to_region(world: MultiWorld, player: int, active_locations, region_name: str, location_name: str,
                            rule: typing.Optional[typing.Callable] = None):
    region = world.get_region(region_name, player)
    loc_id = active_locations.get(location_name, 0)
    if loc_id:
        location = YILocation(player, location_name, loc_id, region)
        region.locations.append(location)
        if rule:
            add_rule(location, rule)


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