import typing

from BaseClasses import Region, MultiWorld, Location, Entrance
from .Locations import leaf_forest_locations, hot_crater_locations, music_plant_locations, ice_paradise_locations, \
                        sky_canyon_locations, techno_base_locations, egg_utopia_locations, xx_locations, SADV2Location, \
                        all_locations
from .Items import zone_table, SADV2Item
from .Options import SADV2Options
from . import Names

class SADV2Region(Region):
    game: str = "Sonic Advance 2"

def create_regions(world: MultiWorld, options: SADV2Options, player: int, xx_coords: int):
    menu_region = Region("Menu", player, world, "Zone Select")
    world.regions.append(menu_region)

    leaf_forest = create_region("Leaf Forest", player, world)
    create_character_regions("Leaf Forest", leaf_forest_locations, player, world)
    connect(world, player, "Menu", "Leaf Forest", 
            lambda state: (state.has("Leaf Forest", player)))

    hot_crater = create_region("Hot Crater", player, world)
    create_character_regions("Hot Crater", hot_crater_locations, player, world)
    connect(world, player, "Menu", "Hot Crater",
            lambda state: (state.has("Hot Crater", player)))

    music_plant = create_region("Music Plant", player, world)
    create_character_regions("Music Plant", music_plant_locations, player, world)
    connect(world, player, "Menu", "Music Plant",
            lambda state: (state.has("Music Plant", player)))

    ice_paradise = create_region("Ice Paradise", player, world)
    create_character_regions("Ice Paradise", ice_paradise_locations, player, world)
    connect(world, player, "Menu", "Ice Paradise",
            lambda state: (state.has("Ice Paradise", player)))

    sky_canyon = create_region("Sky Canyon", player, world)
    create_character_regions("Sky Canyon", sky_canyon_locations, player, world)
    connect(world, player, "Menu", "Sky Canyon",
            lambda state: (state.has("Sky Canyon", player)))

    techno_base = create_region("Techno Base", player, world)
    create_character_regions("Techno Base", techno_base_locations, player, world)
    connect(world, player, "Menu", "Techno Base",
            lambda state: (state.has("Techno Base", player)))

    egg_utopia = create_region("Egg Utopia", player, world)
    create_character_regions("Egg Utopia", egg_utopia_locations, player, world)
    connect(world, player, "Menu", "Egg Utopia",
            lambda state: (state.has("Egg Utopia", player)))

    xx = create_region("XX", player, world)
    create_character_regions("XX", xx_locations, player, world)
    connect(world, player, "Menu", "XX",
            lambda state: (state.has_all_counts({Names.xx_unlock: xx_coords}, player)))
    
    true_area_53 = create_region("True Area 53", player, world)
    true_area_53.add_event("True Area 53", "Vanilla Rescued", location_type=SADV2Location, item_type=SADV2Item)
    connect(world, player, "Menu", "True Area 53", 
            lambda state: (state.has(Names.sonic_unlock, player),
                           state.has(Names.red_emerald, player),
                           state.has(Names.blue_emerald, player),
                           state.has(Names.yellow_emerald, player),
                           state.has(Names.green_emerald, player),
                           state.has(Names.cyan_emerald, player),
                           state.has(Names.white_emerald, player),
                           state.has(Names.purple_emerald, player)))



def create_region(name: str, player: int, world: MultiWorld) -> SADV2Region:
    region = SADV2Region(name, player, world)
    world.regions.append(region)

    return region

def create_locations(region: Region, *locations: str):
    region.locations += [SADV2Location(region.player, location_name, all_locations[location_name], region) for location_name in locations]

def connect(world: MultiWorld, player: int, outer_region: str, inner_region: str, \
            rule: typing.Optional[typing.Callable] = None):
    outer = world.get_region(outer_region, player)
    inner = world.get_region(inner_region, player)
    return outer.connect(inner, rule=rule)

def create_character_regions(region: str, locations: dict, player: int, world: MultiWorld):
    sonic_region = create_region(region + " - Sonic", player, world)
    cream_region = create_region(region + " - Cream", player, world)
    tails_region = create_region(region + " - Tails", player, world)
    knuckles_region = create_region(region + " - Knuckles", player, world)
    amy_region = create_region(region + " - Amy", player, world)

    for key in locations.keys():
        if "Sonic" in key:
            create_locations(sonic_region, key)
        elif "Cream" in key:
            create_locations(cream_region, key)
        elif "Tails" in key:
            create_locations(tails_region, key)
        elif "Knuckles" in key:
            create_locations(knuckles_region, key)
        else:
            create_locations(amy_region, key)
    
    connect(world, player, region, region + " - Sonic",
            lambda state: (state.has(Names.sonic_unlock, player)))
    connect(world, player, region, region + " - Cream", 
            lambda state: (state.has(Names.cream_unlock, player)))
    connect(world, player, region, region + " - Tails", 
            lambda state: (state.has(Names.tails_unlock, player)))
    connect(world, player, region, region + " - Knuckles",
            lambda state: (state.has(Names.knuckles_unlock, player)))
    connect(world, player, region, region + " - Amy",
            lambda state: (state.has(Names.amy_unlock, player)))