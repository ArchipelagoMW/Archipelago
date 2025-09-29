from typing import Dict, List, NamedTuple, cast, TYPE_CHECKING
from .Enums import Regions


class SohRegionData(NamedTuple):
    connecting_regions: List[str] = []


# Fill region data table based on the regions enum list
region_data_table: Dict[str, SohRegionData] = {}
for entry in Regions:
    region_data_table[entry.value] = SohRegionData([])
