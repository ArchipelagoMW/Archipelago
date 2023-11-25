from typing import Dict, List, NamedTuple


class CliqueRegionData(NamedTuple):
    connecting_regions: List[str] = []


region_data_table: Dict[str, CliqueRegionData] = {
    "Menu": CliqueRegionData(["The Button Realm"]),
    "The Button Realm": CliqueRegionData(),
}
