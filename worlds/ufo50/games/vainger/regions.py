from typing import Dict, NamedTuple, TYPE_CHECKING, List
from BaseClasses import Region

from .locations import create_locations
from .rules import create_rules

if TYPE_CHECKING:
    from ... import UFO50World

# adapted from Barbuta, thanks Scipio! <3


class RegionInfo(NamedTuple):
    pass


# using genepods as the main regions instead of rooms/entrances to avoid having to use
# state logic to deal with conflicting mod allocations and damage tracking. basing everything 
# on genepods guarantees the player can recharge and alter their configuration between legs
# of logic. item rules will be based on getting to the item and back using at most two clones.
#
# based on a map at https://steamcommunity.com/sharedfiles/filedetails/?id=3341323146
regions: List[str] = [
    "Menu",

    "LatomR6C3 Genepod",
    "LatomR9C3 Genepod",
    "LatomR3C4 Genepod",
    "LatomR5C4 Genepod",
    "LatomR5C6 Genepod",
    "LatomR7C6 Genepod",
    "LatomR4C9 Genepod",
    "ThetaR4C1 Genepod",
    "ThetaR9C5 Genepod",
    "ThetaR5C6 Genepod",  # starting room genepod
    "ThetaR6C6 Genepod",
    "ThetaR7C9 Genepod",
    "ThetaR9C9 Genepod",
    "VerdeR1C1 Genepod",
    "VerdeR1C5 Genepod",
    "VerdeR6C5 Genepod",
    "VerdeR7C9 Genepod",
    "VerdeR9C9 Genepod",
    "Control Genepod",
    
    "LatomR6C4 Area",
    "VerdeSW Area",
    "VerdeR7C8 Location",
    "ThetaR8C3 Location",
    "ThetaR10C3 Location"
]


def create_regions_and_rules(world: "UFO50World") -> Dict[str, Region]:
    vainger_regions: Dict[str, Region] = {}
    for region_name in regions:
        vainger_regions[f"Vainger - {region_name}"] = Region(f"Vainger - {region_name}", world.player, world.multiworld)

    create_locations(world, vainger_regions)
    create_rules(world, vainger_regions)

    return vainger_regions
