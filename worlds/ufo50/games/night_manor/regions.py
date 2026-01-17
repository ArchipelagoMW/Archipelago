from typing import Dict, NamedTuple, TYPE_CHECKING, List
from BaseClasses import Region

from .locations import create_locations
from .rules import create_rules

if TYPE_CHECKING:
    from ... import UFO50World


# not sure if we really need this yet, but making it in case we need it later since it's easy to remove
class RegionInfo(NamedTuple):
    rooms: List[str] = []  # rooms this region contains, for the purpose of the garden prize access rule


regions: List[str] = [
    "Menu",  # the non-existent start menu, every game needs a region named "Game Name - Menu"
    "Starting Room",  # the initial room the game starts in
    "First Floor & Exterior",  # the floor accessible immediately after you exit the starting area
    "Second Floor",  # second floor accessible after you get powered flashlight
    "Shed",  # shed accessible after you get copper key
    "Master Bedroom",  # master bedroom accessible after you get gold key
    "Maze",  # maze accessible after you get 4 gems
    "Basement",  # accessible after you get the iron key
]


# this function is required, and its only argument can be the world class
# it must return the regions that it created
# it is recommended that you prepend each region name with the game it is from to avoid overlap
def create_regions_and_rules(world: "UFO50World") -> Dict[str, Region]:
    night_manor_regions: Dict[str, Region] = {}
    for region_name in regions:
        night_manor_regions[region_name] = Region(f"Night Manor - {region_name}", world.player, world.multiworld)

    create_locations(world, night_manor_regions)
    create_rules(world, night_manor_regions)

    return night_manor_regions
