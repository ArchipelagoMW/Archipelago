from typing import Dict, NamedTuple, Optional

from BaseClasses import Location

from .Levels import Level, LocationType
from .Names import LocationName


celeste_base_id: int = 0xCA1000


class CelesteLocation(Location):
    game = "Celeste"


class CelesteLocationData(NamedTuple):
    region: str
    address: Optional[int] = None


strawberry_location_data_table: Dict[str, CelesteLocationData] = {
    LocationName.strawberry_1:  CelesteLocationData("Forsaken City", celeste_base_id + 0x00),
}

checkpoint_location_data_table: Dict[str, CelesteLocationData] = {
    LocationName.fc_a_checkpoint_1: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x00),
    LocationName.fc_a_checkpoint_2: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x01),

    LocationName.fc_b_checkpoint_1: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x08),
    LocationName.fc_b_checkpoint_2: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x09),

    LocationName.os_a_checkpoint_1: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x10),
    LocationName.os_a_checkpoint_2: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x11),

    LocationName.os_b_checkpoint_1: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x18),
    LocationName.os_b_checkpoint_2: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x19),

    LocationName.cr_a_checkpoint_1: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x20),
    LocationName.cr_a_checkpoint_2: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x21),
    LocationName.cr_a_checkpoint_3: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x22),

    LocationName.cr_b_checkpoint_1: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x28),
    LocationName.cr_b_checkpoint_2: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x29),
    LocationName.cr_b_checkpoint_3: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x2A),

    LocationName.gr_a_checkpoint_1: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x30),
    LocationName.gr_a_checkpoint_2: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x31),
    LocationName.gr_a_checkpoint_3: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x32),

    LocationName.gr_b_checkpoint_1: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x38),
    LocationName.gr_b_checkpoint_2: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x39),
    LocationName.gr_b_checkpoint_3: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x3A),

    LocationName.mt_a_checkpoint_1: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x40),
    LocationName.mt_a_checkpoint_2: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x41),
    LocationName.mt_a_checkpoint_3: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x42),
    LocationName.mt_a_checkpoint_4: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x43),

    LocationName.mt_b_checkpoint_1: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x48),
    LocationName.mt_b_checkpoint_2: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x49),
    LocationName.mt_b_checkpoint_3: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x4A),

    LocationName.ref_a_checkpoint_1: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x50),
    LocationName.ref_a_checkpoint_2: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x51),
    LocationName.ref_a_checkpoint_3: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x52),
    LocationName.ref_a_checkpoint_4: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x53),
    LocationName.ref_a_checkpoint_5: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x54),

    LocationName.ref_b_checkpoint_1: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x58),
    LocationName.ref_b_checkpoint_2: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x59),
    LocationName.ref_b_checkpoint_3: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x5A),

    LocationName.sum_a_checkpoint_1: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x60),
    LocationName.sum_a_checkpoint_2: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x61),
    LocationName.sum_a_checkpoint_3: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x62),
    LocationName.sum_a_checkpoint_4: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x63),
    LocationName.sum_a_checkpoint_5: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x64),
    LocationName.sum_a_checkpoint_6: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x65),

    LocationName.sum_b_checkpoint_1: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x68),
    LocationName.sum_b_checkpoint_2: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x69),
    LocationName.sum_b_checkpoint_3: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x6A),
    LocationName.sum_b_checkpoint_4: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x6B),
    LocationName.sum_b_checkpoint_5: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x6C),
    LocationName.sum_b_checkpoint_6: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x6D),

    LocationName.core_a_checkpoint_1: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x70),
    LocationName.core_a_checkpoint_2: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x71),
    LocationName.core_a_checkpoint_3: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x72),

    LocationName.core_b_checkpoint_1: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x78),
    LocationName.core_b_checkpoint_2: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x79),
    LocationName.core_b_checkpoint_3: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x7A),

    LocationName.farewell_checkpoint_1: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x80),
    LocationName.farewell_checkpoint_2: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x81),
    LocationName.farewell_checkpoint_3: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x82),
    LocationName.farewell_checkpoint_4: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x83),
    LocationName.farewell_checkpoint_5: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x84),
    LocationName.farewell_checkpoint_6: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x85),
    LocationName.farewell_checkpoint_7: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x86),
    LocationName.farewell_checkpoint_8: CelesteLocationData("Forsaken City", celeste_base_id + 0x100 + 0x87),
}

location_data_table: Dict[str, CelesteLocationData] = {**strawberry_location_data_table,
                                                       **checkpoint_location_data_table}

location_id_offsets: Dict[LocationType, int] = {
    LocationType.Strawberry:        celeste_base_id,
    LocationType.Golden_Strawberry: celeste_base_id + 0x100,
    LocationType.Cassette:          celeste_base_id + 0x200,
    LocationType.Crystal_Heart:     celeste_base_id + 0x300,
    LocationType.Checkpoint:        celeste_base_id + 0x400,
    LocationType.Level_Clear:       celeste_base_id + 0x500,
    LocationType.Room_Enter:        celeste_base_id + 0x800,
}


def generate_location_table(level_data: Dict[str, Level]):
    location_table = {name: data.address for name, data in location_data_table.items() if data.address is not None}

    location_counts: Dict[LocationType, int] = {
        LocationType.Strawberry:        0,
        LocationType.Golden_Strawberry: 0,
        LocationType.Cassette:          0,
        LocationType.Crystal_Heart:     0,
        LocationType.Checkpoint:        0,
        LocationType.Level_Clear:       0,
        LocationType.Room_Enter:        0,
    }

    for _, level in level_data.items():
        for room in level.rooms:
            location_table[level.display_name + " - " + room.display_name] = location_id_offsets[LocationType.Room_Enter]
            location_counts[LocationType.Room_Enter] += 1

            for region in room.regions:
                for location in region.locations:
                    location_table[level.display_name + " - " + location.display_name] = location_id_offsets[location.loc_type] + location_counts[location.loc_type]
                    location_counts[location.loc_type] += 1

    for loc_name in location_table.keys():
        print(loc_name) 
    return location_table
