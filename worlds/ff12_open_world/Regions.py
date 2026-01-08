from typing import Dict, List, NamedTuple


class FF12OpenWorldRegionData(NamedTuple):
    connecting_regions: List[str] = []


# TODO: Switch to actually use the regions once the standalone randomizer uses regions as well.
region_data_table: Dict[str, FF12OpenWorldRegionData] = {
    "Menu": FF12OpenWorldRegionData(["Ivalice"]),
    "Ivalice": FF12OpenWorldRegionData(),
}
