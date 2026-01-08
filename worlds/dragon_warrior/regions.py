from BaseClasses import Entrance, Region
from worlds.AutoWorld import World
from typing import Dict, Optional, Callable

from . import locations
from . import names

"""
CHEST MEMORY NOTES:

ROM Data for chests starts at offset 0x5DDD, each are stored in 4 bytes
Format: Map ID, X, Y, Chest Contents

OFFSET |        MAP      | CONTENTS
-------|-----------------|---------
0x5DDD | Tantegel Castle |   ~10G
0x5DE1 | Tantegel Castle |   ~10G
0x5DE5 | Tantegel Castle |   ~10G
0x5DE9 | Tantegel Castle |   ~10G
0x5DED |   Throne Room   |   120G
0x5DF1 |   Throne Room   |   Torch
0x5DF5 |   Throne Room   |    Key
0x5DF9 |     Rimuldar    |   Wings
0x5DFD |     Garinham    |   ~10G
0x5E01 |     Garinham    |   Herb
0x5E05 |     Garinham    |   Torch
0x5E09 |    Dragonlord   |   Herb
0x5E0D |    Dragonlord   | High Gold
0x5E11 |    Dragonlord   |   Wings
0x5E15 |    Dragonlord   |    Key
0x5E19 |    Dragonlord   | Cursed Belt
0x5E1D |    Dragonlord   |   Herb
0x5E21 |    Sun Shrine   | St. of Sunl.
0x5E25 |   Rain Shrine   | St. of Rain
0x5E29 |  Garin Grave B1 |   Herb
0x5E2D |  Garin Grave B1 |   ~10G
0x5E31 |  Garin Grave B1 |   ~10G
0x5E35 |  Garin Grave B3 | Cursed Belt
0x5E39 |  Garin Grave B3 | Silv. Harp
0x5E3D |   Charlock B2   | Erdr. Sword
0x5E41 | MountainCave B2 |   ~107G
0x5E45 | MountainCave B2 |   Torch
0x5E49 | MountainCave B2 | Fight. Ring
0x5E4D | MountainCave B2 |   ~10G
0x5E51 | MountainCave B1 |   Herb
0x5E55 | Erdrick Cave B2 | Erd. Tablet
"""

class DWRegion(Region):
    game = "Dragon Warrior"

def create_regions(world: World, level_locations, high_level_locations) -> None:
    # Deal with conditional locations
    brecconary_locations = {}
    kol_locations = {}
    garinham_locations = {}
    mountain_cave_locations = {**locations.mountain_cave_locations}
    rimuldar_locations = {}
    cantlin_locations = {}
    swamp_cave_locations = {**locations.swamp_cave_locations}
    hauksness_locations = {}
    token_locations = {}
    charlock_locations = {**locations.charlock_locations}
    dragonlord_locations = {}

    if world.options.searchsanity:
        kol_locations = {**kol_locations, **locations.kol_locations}
        hauksness_locations = {**hauksness_locations, **locations.hauksness_locations}
        token_locations = {**token_locations, **locations.erdricks_token_locations}

    if world.options.shopsanity:
        brecconary_locations = {**brecconary_locations, **locations.brecconary_locations}
        kol_locations = {**kol_locations, **locations.kol_shop_locations}
        garinham_locations = {**garinham_locations, **locations.garinham_locations}
        rimuldar_locations = {**rimuldar_locations, **locations.rimuldar_locations}
        cantlin_locations = {**cantlin_locations, **locations.cantlin_locations}

    if world.options.monstersanity:
        brecconary_locations = {**brecconary_locations, **locations.brecconary_monster_locations}
        garinham_locations = {**garinham_locations, **locations.garinham_monster_locations}
        kol_locations = {**kol_locations, **locations.kol_monster_locations}
        mountain_cave_locations = {**mountain_cave_locations, **locations.mountain_cave_monster_locations}
        rimuldar_locations = {**rimuldar_locations, **locations.rimuldar_monster_locations}
        cantlin_locations = {**cantlin_locations, **locations.cantlin_monster_locations}
        swamp_cave_locations = {**swamp_cave_locations, **locations.swamp_cave_monster_locations}
        hauksness_locations = {**hauksness_locations, **locations.hauksness_monster_locations}
        charlock_locations = {**charlock_locations, **locations.charlock_monster_locations}
        dragonlord_locations = {**dragonlord_locations, **locations.charlock_dragonlord_locations}

        
    
    menu_region = create_region(world, 'Menu', None)

    overworld_region = create_region(world, names.overworld, level_locations)

    # For location checks on levels 10-30
    strong_overworld_region = create_region(world, names.strong_overworld, high_level_locations)

    tantegel_throne_room_region = create_region(world, names.tantegel_throne_room, locations.throne_room_locations)
    
    tantegel_castle_region = create_region(world, names.tantegel_castle, locations.tantegel_castle_locations)

    brecconary_region = create_region(world, names.breconnary, brecconary_locations)

    garinham_region = create_region(world, names.garinham, garinham_locations)

    garinham_key_region = create_region(world, names.garinham_keys, locations.garinham_key_locations)

    kol_region = create_region(world, names.kol, kol_locations)

    rimuldar_region = create_region(world, names.rimuldar, rimuldar_locations)    

    rimuldar_key_region = create_region(world, names.rimuldar_keys, locations.rimuldar_key_locations)

    cantlin_region = create_region(world, names.cantlin, cantlin_locations)

    mountain_cave_region = create_region(world, names.mountain_cave, mountain_cave_locations)

    swamp_cave_region = create_region(world, names.swamp_cave, swamp_cave_locations)

    garins_grave_region = create_region(world, names.garins_grave, locations.garins_grave_locations)

    charlock_region = create_region(world, names.charlock_castle, charlock_locations)

    # For MonsterSanity, connect with equipment so the Dragonlord kills don't have any
    dragonlord_region = create_region(world, names.charlock_dragonlord, dragonlord_locations)

    hauksness_region = create_region(world, names.hauksness, hauksness_locations)

    erdricks_cave_region = create_region(world, names.erdricks_cave, locations.erdricks_cave_locations)

    shrine_of_rain_region = create_region(world, names.staff_of_rain_shrine, locations.shrine_of_rain_locations)

    erdricks_token_region = create_region(world, names.erdricks_token_tile, token_locations)

    rainbow_shrine_reigon = create_region(world, names.rainbow_drop_shrine, locations.rainbow_shrine_locations)

    world.multiworld.regions += [
        menu_region,
        overworld_region,
        strong_overworld_region,
        tantegel_throne_room_region,
        tantegel_castle_region,
        brecconary_region,
        garinham_region,
        garinham_key_region,
        kol_region,
        rimuldar_region,
        rimuldar_key_region,
        cantlin_region,
        mountain_cave_region,
        swamp_cave_region,
        garins_grave_region,
        charlock_region,
        dragonlord_region,
        hauksness_region,
        erdricks_cave_region,
        shrine_of_rain_region,
        erdricks_token_region,
        rainbow_shrine_reigon,
    ]


def connect_regions(world: World) -> None:
    # I'm gonna be lazy and just restrict where the magic key is on random maps to prevent softlocks
    random_map = world.options.random_map
    searchsanity = world.options.searchsanity
    shopsanity = world.options.shopsanity
    region_names: Dict[str, int] = {}

    connect(world, world.player, region_names, 'Menu', names.tantegel_throne_room)
    connect(world, world.player, region_names, 'Menu', names.overworld)
    connect(world, world.player, region_names, names.overworld, names.strong_overworld,
        equipment_helper(world, 3, 3, 2, True))
    connect(world, world.player, region_names, names.overworld, names.breconnary)
    connect(world, world.player, region_names, names.overworld, names.garinham, 
        equipment_helper(world, 2, 2, 1))
    connect(world, world.player, region_names, names.overworld, names.kol,
        equipment_helper(world, 1, 1, 1))
    connect(world, world.player, region_names, names.overworld, names.rimuldar,
        equipment_helper(world, 3, 3, 1))
    connect(world, world.player, region_names, names.garinham, names.hauksness,
        equipment_helper(world, 5, 5, 3))
    connect(world, world.player, region_names, names.garinham, names.cantlin,
        equipment_helper(world, 4, 4, 2, True))
    connect(world, world.player, region_names, names.overworld, names.erdricks_cave,
            lambda state: (not random_map or state.has(names.magic_key, world.player)))
    connect(world, world.player, region_names, names.garinham, names.mountain_cave,
        equipment_helper(world, 3, 3, 2, random_map))
    connect(world, world.player, region_names, names.overworld, names.swamp_cave,
        equipment_helper(world, 4, 4, 2, random_map))


    connect(world, world.player, region_names, names.rimuldar, names.rainbow_drop_shrine,
        lambda state: (state.has(names.staff_of_rain, world.player) and 
                        state.has(names.stones_of_sunlight, world.player) and
                        state.has(names.magic_key, world.player) and
                        (not searchsanity or (state.has(names.erdricks_token, world.player) and
                                              state.has(names.fairy_flute, world.player)))))

    connect(world, world.player, region_names, names.overworld, names.tantegel_castle, 
        lambda state: (state.has(names.magic_key, world.player)))
    connect(world, world.player, region_names, names.garinham, names.garinham_keys, 
        lambda state: (state.has(names.magic_key, world.player)))
    connect(world, world.player, region_names, names.rimuldar, names.rimuldar_keys,
        lambda state: (state.has(names.magic_key, world.player)))
    connect(world, world.player, region_names, names.garinham_keys, names.garins_grave,
        equipment_helper(world, 4, 3, 2))
    connect(world, world.player, region_names, names.rimuldar, names.staff_of_rain_shrine, 
        lambda state: (state.has(names.silver_harp, world.player) and 
                       (not random_map or state.has(names.magic_key, world.player))))
    connect(world, world.player, region_names, names.cantlin, names.erdricks_token_tile,
        lambda state: (state.has(names.gwaelins_love, world.player)))
    connect(world, world.player, region_names, names.rainbow_drop_shrine, names.charlock_castle,
        equipment_helper(world, 6, 6, 2))
    connect(world, world.player, region_names, names.charlock_castle, names.charlock_dragonlord,
        equipment_helper(world, 7, 7, 3))

def create_region(world: World, name: str, location_checks=None):
    ret = DWRegion(name, world.player, world.multiworld)
    if location_checks:
        for locName, locId in location_checks.items():
            location = locations.DWLocation(world.player, locName, locId, ret)
            ret.locations.append(location)

    return ret

def connect(world: World, player: int, used_names: Dict[str, int], source: str, target: str,
            rule: Optional[Callable] = None):
    source_region = world.multiworld.get_region(source, player)
    target_region = world.multiworld.get_region(target, player)

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

def equipment_helper(world, weapons: int, armors: int, shields: int, key: bool = False):
    if not world.options.shopsanity:
        return lambda state: (True)
    return lambda state: (state.has(names.progressive_weapon, world.player, weapons) and 
                          state.has(names.progressive_armor, world.player, armors) and
                          state.has(names.progressive_shield, world.player, shields) and
                          (not key or state.has(names.magic_key, world.player)))
