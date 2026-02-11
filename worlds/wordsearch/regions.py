from typing import Callable, Dict, List, NamedTuple
from BaseClasses import CollectionState


class WordSearchRegionData(NamedTuple):
    connecting_regions: List[str] = []
    rules: Dict[str, Callable[[CollectionState], bool]] = None

region_data_table: Dict[str, WordSearchRegionData] = {
    "Menu": WordSearchRegionData(["Words"]),
    "Words": WordSearchRegionData(),
}
