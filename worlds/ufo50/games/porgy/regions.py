from typing import Dict, NamedTuple, TYPE_CHECKING, List
from BaseClasses import Region

from .locations import create_locations
from .rules import create_rules

if TYPE_CHECKING:
    from ... import UFO50World


regions: List[str] = [
    "Menu",
    "Shallows",
    "Shallows - Buster",
    "Shallows - Missile",
    "Shallows - Depth",
    "Sunken Ship",
    "Sunken Ship - Buster",
    "Deeper",
    "Abyss",
    "Boss Area",
]


# this function is required, and its only argument can be the world class
# it must return the regions that it created
# it is recommended that you prepend each region name with the game it is from to avoid overlap
def create_regions_and_rules(world: "UFO50World") -> Dict[str, Region]:
    porgy_regions: Dict[str, Region] = {}
    for region_name in regions:
        porgy_regions[region_name] = Region(f"Porgy - {region_name}", world.player, world.multiworld)

    create_locations(world, porgy_regions)
    create_rules(world, porgy_regions)

    return porgy_regions
