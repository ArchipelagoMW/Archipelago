from typing import Dict, Tuple, Optional

from BaseClasses import LocationProgressType as ProgType, Location, Region, LocationProgressType
from .data.strings import SPZ

connect_locations: Dict[str, Tuple[str, ProgType]] = {
    SPZ.location_connect: (SPZ.region_menu, ProgType.DEFAULT),
}

shapesanity_locations: Dict[str, Tuple[str, ProgType]] = {
    SPZ.location_shape_0: (SPZ.region_four_parts, ProgType.DEFAULT),
    SPZ.location_shape_1: (SPZ.region_four_parts, ProgType.DEFAULT),
    SPZ.location_shape_2: (SPZ.region_four_parts, ProgType.DEFAULT),
    SPZ.location_shape_3: (SPZ.region_four_parts, ProgType.DEFAULT),
}

location_table: Dict[str, Tuple[str, ProgType]] = {
    **connect_locations,
    **shapesanity_locations,
}


class Shapez2Location(Location):
    game = SPZ.game_name

    def __init__(self, player: int, name: str, address: Optional[int], region: Region,
                 progress_type: LocationProgressType):
        super(Shapez2Location, self).__init__(player, name, address, region)
        self.progress_type = progress_type
