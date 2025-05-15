from BaseClasses import Entrance, Region
from worlds.AutoWorld import World
from typing import Dict, Optional, Callable

from .Locations import DWLocation


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
