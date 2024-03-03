from typing import Dict, NamedTuple, Optional

from BaseClasses import Location
from .Names import LocationName


celeste_64_base_id: int = 0xCA0000


class Celeste64Location(Location):
    game = "Celeste 64"


class Celeste64LocationData(NamedTuple):
    region: str
    address: Optional[int] = None


location_data_table: Dict[str, Celeste64LocationData] = {
    LocationName.strawberry_1 : Celeste64LocationData(
        region = "Forsaken City",
        address = celeste_64_base_id + 0,
    ),
    LocationName.strawberry_2 : Celeste64LocationData(
        region = "Forsaken City",
        address = celeste_64_base_id + 1,
    ),
    LocationName.strawberry_3 : Celeste64LocationData(
        region = "Forsaken City",
        address = celeste_64_base_id + 2,
    ),
    LocationName.strawberry_4 : Celeste64LocationData(
        region = "Forsaken City",
        address = celeste_64_base_id + 3,
    ),
    LocationName.strawberry_5 : Celeste64LocationData(
        region = "Forsaken City",
        address = celeste_64_base_id + 4,
    ),
    LocationName.strawberry_6 : Celeste64LocationData(
        region = "Forsaken City",
        address = celeste_64_base_id + 5,
    ),
    LocationName.strawberry_7 : Celeste64LocationData(
        region = "Forsaken City",
        address = celeste_64_base_id + 6,
    ),
    LocationName.strawberry_8 : Celeste64LocationData(
        region = "Forsaken City",
        address = celeste_64_base_id + 7,
    ),
    LocationName.strawberry_9 : Celeste64LocationData(
        region = "Forsaken City",
        address = celeste_64_base_id + 8,
    ),
    LocationName.strawberry_10 : Celeste64LocationData(
        region = "Forsaken City",
        address = celeste_64_base_id + 9,
    ),
    LocationName.strawberry_11 : Celeste64LocationData(
        region = "Forsaken City",
        address = celeste_64_base_id + 10,
    ),
    LocationName.strawberry_12 : Celeste64LocationData(
        region = "Forsaken City",
        address = celeste_64_base_id + 11,
    ),
    LocationName.strawberry_13 : Celeste64LocationData(
        region = "Forsaken City",
        address = celeste_64_base_id + 12,
    ),
    LocationName.strawberry_14 : Celeste64LocationData(
        region = "Forsaken City",
        address = celeste_64_base_id + 13,
    ),
    LocationName.strawberry_15 : Celeste64LocationData(
        region = "Forsaken City",
        address = celeste_64_base_id + 14,
    ),
    LocationName.strawberry_16 : Celeste64LocationData(
        region = "Forsaken City",
        address = celeste_64_base_id + 15,
    ),
    LocationName.strawberry_17 : Celeste64LocationData(
        region = "Forsaken City",
        address = celeste_64_base_id + 16,
    ),
    LocationName.strawberry_18 : Celeste64LocationData(
        region = "Forsaken City",
        address = celeste_64_base_id + 17,
    ),
    LocationName.strawberry_19 : Celeste64LocationData(
        region = "Forsaken City",
        address = celeste_64_base_id + 18,
    ),
    LocationName.strawberry_20 : Celeste64LocationData(
        region = "Forsaken City",
        address = celeste_64_base_id + 19,
    ),
    LocationName.strawberry_21 : Celeste64LocationData(
        region = "Forsaken City",
        address = celeste_64_base_id + 20,
    ),
    LocationName.strawberry_22 : Celeste64LocationData(
        region = "Forsaken City",
        address = celeste_64_base_id + 21,
    ),
    LocationName.strawberry_23 : Celeste64LocationData(
        region = "Forsaken City",
        address = celeste_64_base_id + 22,
    ),
    LocationName.strawberry_24 : Celeste64LocationData(
        region = "Forsaken City",
        address = celeste_64_base_id + 23,
    ),
    LocationName.strawberry_25 : Celeste64LocationData(
        region = "Forsaken City",
        address = celeste_64_base_id + 24,
    ),
    LocationName.strawberry_26 : Celeste64LocationData(
        region = "Forsaken City",
        address = celeste_64_base_id + 25,
    ),
    LocationName.strawberry_27 : Celeste64LocationData(
        region = "Forsaken City",
        address = celeste_64_base_id + 26,
    ),
    LocationName.strawberry_28 : Celeste64LocationData(
        region = "Forsaken City",
        address = celeste_64_base_id + 27,
    ),
    LocationName.strawberry_29 : Celeste64LocationData(
        region = "Forsaken City",
        address = celeste_64_base_id + 28,
    ),
    LocationName.strawberry_30 : Celeste64LocationData(
        region = "Forsaken City",
        address = celeste_64_base_id + 29,
    )
}

location_table = {name: data.address for name, data in location_data_table.items() if data.address is not None}
