from typing import List, Dict, Tuple

from BaseClasses import Region, LocationProgressType as ProgType, MultiWorld
from .data.strings import SPZ
from .locations import Shapez2Location
from worlds.generic.Rules import set_rule

all_regions = [
    SPZ.region_menu,
    SPZ.region_four_parts,
]


def get_regions(location_name_to_id: Dict[str, int], player: int, multiworld: MultiWorld) -> List[Region]:

    region_menu = Region(SPZ.region_menu, player, multiworld)
    region_four_parts = Region(SPZ.region_four_parts, player, multiworld)
    region_menu.connect(region_four_parts, "Ingame", lambda state: True)

    region_menu.locations.append(Shapez2Location(player, SPZ.location_connect,
                                                 location_name_to_id[SPZ.location_connect], region_menu,
                                                 ProgType.DEFAULT))
    for shape in SPZ.shapes:
        location = Shapez2Location(player, shape, location_name_to_id[shape], region_four_parts, ProgType.DEFAULT)
        region_four_parts.locations.append(location)
        set_rule(location, lambda state: state.has(shape, player))

    return [region_menu, region_four_parts]
