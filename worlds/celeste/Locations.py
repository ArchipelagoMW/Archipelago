from typing import Dict, NamedTuple, Optional

from BaseClasses import Location, Region

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
    LocationType.strawberry:        celeste_base_id,
    LocationType.golden_strawberry: celeste_base_id + 0x100,
    LocationType.cassette:          celeste_base_id + 0x200,
    LocationType.crystal_heart:     celeste_base_id + 0x300,
    LocationType.checkpoint:        celeste_base_id + 0x400,
    LocationType.level_clear:       celeste_base_id + 0x500,
    LocationType.room_enter:        celeste_base_id + 0x800,
}


def generate_location_table(level_data: Dict[str, Level]):
    location_table = {name: data.address for name, data in location_data_table.items() if data.address is not None}

    location_counts: Dict[LocationType, int] = {
        LocationType.strawberry:        0,
        LocationType.golden_strawberry: 0,
        LocationType.cassette:          0,
        LocationType.crystal_heart:     0,
        LocationType.checkpoint:        0,
        LocationType.level_clear:       0,
        LocationType.room_enter:        0,
    }

    for _, level in level_data.items():
        for room in level.rooms:
            location_table[level.display_name + " - " + room.display_name] = location_id_offsets[LocationType.room_enter] + location_counts[LocationType.room_enter]
            location_counts[LocationType.room_enter] += 1

            if room.checkpoint != None and room.checkpoint != "Start":
                location_table[level.display_name + " - " + room.checkpoint] = location_id_offsets[LocationType.checkpoint] + location_counts[LocationType.checkpoint]
                location_counts[LocationType.checkpoint] += 1

            for region in room.regions:
                for location in region.locations:
                    location_table[location.display_name] = location_id_offsets[location.loc_type] + location_counts[location.loc_type]
                    location_counts[location.loc_type] += 1

    for loc_name in location_table.keys():
        print(loc_name) 
    return location_table

# TODO: Finish this function
def create_regions_and_locations(world):
    menu_region = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu_region)

    # TEMP
    temp_region = Region("Forsaken City", world.player, world.multiworld)
    world.multiworld.regions.append(temp_region)

    for _, level in world.level_data.items():
        if level.name[-2] == "8" and not world.options.include_core:
            continue
        if level.name[-1] == "9" and not world.options.include_farewell:
            continue
        if level.name[-1] == "b" and not world.options.include_b_sides:
            continue
        if level.name[-1] == "c" and not world.options.include_c_sides:
            continue

        for room in level.rooms:
            room_region = Region(room.name + "_room", world.player, world.multiworld)
            world.multiworld.regions.append(room_region)

            for pre_region in room.regions:
                region = Region(pre_region.name, world.player, world.multiworld)
                world.multiworld.regions.append(region)
                region.add_locations({
                    location.display_name: world.location_name_to_id[location.display_name] for location in pre_region.locations
                }, CelesteLocation)

            for pre_region in room.regions:
                region = world.multiworld.get_region(pre_region.name, world.player)
                region.add_exits(
                    [connection.destination_name for connection in pre_region.connections],
                    {connection.destination_name: connection.rule for connection in pre_region.connections}
                )
                region.add_exits([room_region.name])
                print([exit.name for exit in region.exits])

            if room.checkpoint != None:
                checkpoint_rule = None
                if room.checkpoint != "Start":
                    checkpoint_location_name = level.display_name + " - " + room.checkpoint
                    checkpoint_rule = lambda state: state.has(checkpoint_location_name)
                    room_region.add_locations({
                        checkpoint_location_name: world.location_name_to_id[checkpoint_location_name]
                    }, CelesteLocation)
                print(room.checkpoint)
                print(room.checkpoint_region)
                menu_region.add_exits([room.checkpoint_region], {room.checkpoint_region: checkpoint_rule})

            if world.options.roomsanity:
                room_location_name = room.display_name
                room_region.add_locations({
                    room_location_name: world.location_name_to_id[checkpoint_location_name]
                }, CelesteLocation)
        print([exit.name for exit in menu_region.exits])

        for room_connection in level.room_connections:
            source_region = world.multiworld.get_region(room_connection.source.name, world.player)
            source_region.add_exits([room_connection.dest.name])
            if room_connection.two_way:
                dest_region = world.multiworld.get_region(room_connection.dest.name, world.player)
                dest_region.add_exits([room_connection.source.name])
            print([exit.name for exit in source_region.exits])
