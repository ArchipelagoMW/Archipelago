from typing import Dict, List, NamedTuple, cast, TYPE_CHECKING
from .Enums import Regions

if TYPE_CHECKING:
    from . import SohWorld

class SohRegionData(NamedTuple):
    connecting_regions: List[str] = []

def double_link_regions(world: "SohWorld", region1: str, region2: str):
    world.get_region(region1).connect(world.get_region(region2))
    world.get_region(region2).connect(world.get_region(region1))

# Fill region data table based on the regions enum list
region_data_table: Dict[str, SohRegionData] = {}
for entry in Regions:
    region_data_table[entry.value] = SohRegionData([])
