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
    "Starting Area",
    "Key Room",  # the room with the key, where you can access the key
    "Platforms above R4C4",  # the "first" moving platforms
    "Blood Sword Room",  # E3, probably unnecessary unless we randomize switches
    "R7C3 and Nearby",  # idk what to call this, it's up the poison ladder and right of some balls
    "R6C7 and Nearby",  # lots of purple blocks here
    "Bat Altar",  # the altar at D1 and the room next to it at D2
    "Above Entrance",  # in the sign
    "Wand Trade Room",  # where you trade your sword for a wand
    "R7C7 and Nearby",  # down where the shield guys are, need pin to get to wand
    "Mimic Room",  # H1, where the mimic is
    "Boss Area",  # B6, point of no return unless you paid $500 to break a wall
    "R3C7 above Ladders",  # C7, up by the little guy who breaks the wall
]


# this function is required, and its only argument can be the world class
# it must return the regions that it created
# it is recommended that you prepend each region name with the game it is from to avoid overlap
def create_regions_and_rules(world: "UFO50World") -> Dict[str, Region]:
    barbuta_regions: Dict[str, Region] = {}
    for region_name in regions:
        barbuta_regions[region_name] = Region(f"Barbuta - {region_name}", world.player, world.multiworld)

    create_locations(world, barbuta_regions)
    create_rules(world, barbuta_regions)

    return barbuta_regions
