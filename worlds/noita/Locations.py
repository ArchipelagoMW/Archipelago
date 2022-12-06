# Locations are specific points that you would obtain an item at.
import functools
from typing import Dict
from BaseClasses import Location
from .Options import TotalLocations


class NoitaLocation(Location):
    game: str = "Noita"


# 111000 - 111034
# Mapping of items in each region
location_region_mapping: Dict[str, Dict[str, int]] = {
    "Forest": {
        # 110000 - 110500
        # Just putting these here for now
        f"Chest{i+1}": 110000+i for i in range(TotalLocations.range_end)
    },
    "Holy Mountain 1 (To Coal Pits)": {
        "Holy Mountain 1 (To Coal Pits) Shop Item 1": 111000,
        "Holy Mountain 1 (To Coal Pits) Shop Item 2": 111001,
        "Holy Mountain 1 (To Coal Pits) Shop Item 3": 111002,
        "Holy Mountain 1 (To Coal Pits) Shop Item 4": 111003,
        "Holy Mountain 1 (To Coal Pits) Shop Item 5": 111004,
    },
    "Holy Mountain 2 (To Snowy Depths)": {
        "Holy Mountain 2 (To Snowy Depths) Shop Item 1": 111005,
        "Holy Mountain 2 (To Snowy Depths) Shop Item 2": 111006,
        "Holy Mountain 2 (To Snowy Depths) Shop Item 3": 111007,
        "Holy Mountain 2 (To Snowy Depths) Shop Item 4": 111008,
        "Holy Mountain 2 (To Snowy Depths) Shop Item 5": 111009,
    },
    "Holy Mountain 3 (To Hiisi Base)": {
        "Holy Mountain 3 (To Hiisi Base) Shop Item 1": 111010,
        "Holy Mountain 3 (To Hiisi Base) Shop Item 2": 111011,
        "Holy Mountain 3 (To Hiisi Base) Shop Item 3": 111012,
        "Holy Mountain 3 (To Hiisi Base) Shop Item 4": 111013,
        "Holy Mountain 3 (To Hiisi Base) Shop Item 5": 111014,
    },
    "Holy Mountain 4 (To Underground Jungle)": {
        "Holy Mountain 4 (To Underground Jungle) Shop Item 1": 111015,
        "Holy Mountain 4 (To Underground Jungle) Shop Item 2": 111016,
        "Holy Mountain 4 (To Underground Jungle) Shop Item 3": 111017,
        "Holy Mountain 4 (To Underground Jungle) Shop Item 4": 111018,
        "Holy Mountain 4 (To Underground Jungle) Shop Item 5": 111019,
    },
    "Holy Mountain 5 (To The Vault)": {
        "Holy Mountain 5 (To The Vault) Shop Item 1": 111020,
        "Holy Mountain 5 (To The Vault) Shop Item 2": 111021,
        "Holy Mountain 5 (To The Vault) Shop Item 3": 111022,
        "Holy Mountain 5 (To The Vault) Shop Item 4": 111023,
        "Holy Mountain 5 (To The Vault) Shop Item 5": 111024,
    },
    "Holy Mountain 6 (To Temple of the Art)": {
        "Holy Mountain 6 (To Temple of the Art) Shop Item 1": 111025,
        "Holy Mountain 6 (To Temple of the Art) Shop Item 2": 111026,
        "Holy Mountain 6 (To Temple of the Art) Shop Item 3": 111027,
        "Holy Mountain 6 (To Temple of the Art) Shop Item 4": 111028,
        "Holy Mountain 6 (To Temple of the Art) Shop Item 5": 111029,
    },
    "Holy Mountain 7 (To The Laboratory)": {
        "Holy Mountain 7 (To The Laboratory) Shop Item 1": 111030,
        "Holy Mountain 7 (To The Laboratory) Shop Item 2": 111031,
        "Holy Mountain 7 (To The Laboratory) Shop Item 3": 111032,
        "Holy Mountain 7 (To The Laboratory) Shop Item 4": 111033,
        "Holy Mountain 7 (To The Laboratory) Shop Item 5": 111034,
    }
}

location_name_to_id: Dict[str, int] = {}
for location_group in location_region_mapping.values():
    location_name_to_id.update(location_group)
