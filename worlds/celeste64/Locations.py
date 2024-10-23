from typing import Dict, NamedTuple, Optional

from BaseClasses import Location
from .Names import LocationName


celeste_64_base_id: int = 0xCA0000


class Celeste64Location(Location):
    game = "Celeste 64"


class Celeste64LocationData(NamedTuple):
    region: str
    address: Optional[int] = None


strawberry_location_data_table: Dict[str, Celeste64LocationData] = {
    LocationName.strawberry_1:  Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x00),
    LocationName.strawberry_2:  Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x01),
    LocationName.strawberry_3:  Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x02),
    LocationName.strawberry_4:  Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x03),
    LocationName.strawberry_5:  Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x04),
    LocationName.strawberry_6:  Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x05),
    LocationName.strawberry_7:  Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x06),
    LocationName.strawberry_8:  Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x07),
    LocationName.strawberry_9:  Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x08),
    LocationName.strawberry_10: Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x09),
    LocationName.strawberry_11: Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x0A),
    LocationName.strawberry_12: Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x0B),
    LocationName.strawberry_13: Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x0C),
    LocationName.strawberry_14: Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x0D),
    LocationName.strawberry_15: Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x0E),
    LocationName.strawberry_16: Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x0F),
    LocationName.strawberry_17: Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x10),
    LocationName.strawberry_18: Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x11),
    LocationName.strawberry_19: Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x12),
    LocationName.strawberry_20: Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x13),
    LocationName.strawberry_21: Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x14),
    LocationName.strawberry_22: Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x15),
    LocationName.strawberry_23: Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x16),
    LocationName.strawberry_24: Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x17),
    LocationName.strawberry_25: Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x18),
    LocationName.strawberry_26: Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x19),
    LocationName.strawberry_27: Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x1A),
    LocationName.strawberry_28: Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x1B),
    LocationName.strawberry_29: Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x1C),
    LocationName.strawberry_30: Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x1D),
}

friend_location_data_table: Dict[str, Celeste64LocationData] = {
    LocationName.granny_1:   Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x100 + 0x00),
    LocationName.granny_2:   Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x100 + 0x01),
    LocationName.granny_3:   Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x100 + 0x02),
    LocationName.theo_1:     Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x100 + 0x03),
    LocationName.theo_2:     Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x100 + 0x04),
    LocationName.theo_3:     Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x100 + 0x05),
    LocationName.badeline_1: Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x100 + 0x06),
    LocationName.badeline_2: Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x100 + 0x07),
    LocationName.badeline_3: Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x100 + 0x08),
}

sign_location_data_table: Dict[str, Celeste64LocationData] = {
    LocationName.sign_1: Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x200 + 0x00),
    LocationName.sign_2: Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x200 + 0x01),
    LocationName.sign_3: Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x200 + 0x02),
    LocationName.sign_4: Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x200 + 0x03),
    LocationName.sign_5: Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x200 + 0x04),
}

car_location_data_table: Dict[str, Celeste64LocationData] = {
    LocationName.car_1: Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x300 + 0x00),
    LocationName.car_2: Celeste64LocationData("Forsaken City", celeste_64_base_id + 0x300 + 0x01),
}

location_data_table: Dict[str, Celeste64LocationData] = {**strawberry_location_data_table,
                                                         **friend_location_data_table,
                                                         **sign_location_data_table,
                                                         **car_location_data_table}

location_table = {name: data.address for name, data in location_data_table.items() if data.address is not None}
