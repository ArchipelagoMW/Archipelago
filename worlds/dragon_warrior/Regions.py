from BaseClasses import Entrance, Region
from worlds.AutoWorld import World
from typing import Dict, Optional, Callable

from .Locations import DWLocation
import Names

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

TODO: Find where code for opening chests is and hijack to not grant chest contents,
as well as send data to the client regarding which check was opened
"""

def create_regions(world: World, active_locations):
    menu_region = create_region(world, active_locations, 'Menu', None)

    # TODO: Add these memory locations?
    tantegel_throne_room_region_locations = {
        Names.tantegel_throne_room_gold_chest,
        Names.tantegel_throne_room_key_chest,
        Names.tantegel_throne_room_torch_chest,
    }
    tantegel_throne_room_region = create_region(world, active_locations, Names.tantegel_throne_room,
                                       tantegel_throne_room_region_locations)



def create_region(world: World, active_locations, name: str, locations=None):
    # Shamelessly stolen from the DKC3 definition
    ret = Region(name, world.player, world.multiworld)
    if locations:
        for locationName, locationData in locations.items():
            loc_id = active_locations.get(locationName, 0)
            if loc_id:
                loc_byte   = locationData[0] if (len(locationData) > 0) else 0
                loc_bit    = locationData[1] if (len(locationData) > 1) else 0
                loc_invert = locationData[2] if (len(locationData) > 2) else False

                location = DWLocation(world.player, locationName, loc_id, ret, loc_byte, loc_bit, loc_invert)
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
