from typing import NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import Location, Region
from worlds.generic.Rules import set_rule

from .Levels import Level, LocationType
from .Names import ItemName

if TYPE_CHECKING:
    from . import CelesteOpenWorld
else:
    CelesteOpenWorld = object


celeste_base_id: int = 0xCA10000


class CelesteLocation(Location):
    game = "Celeste"


class CelesteLocationData(NamedTuple):
    region: str
    address: Optional[int] = None


checkpoint_location_data_table: dict[str, CelesteLocationData] = {}
key_location_data_table: dict[str, CelesteLocationData] = {}

location_id_offsets: dict[LocationType, int | None] = {
    LocationType.strawberry:        celeste_base_id,
    LocationType.golden_strawberry: celeste_base_id + 0x1000,
    LocationType.cassette:          celeste_base_id + 0x2000,
    LocationType.car:               celeste_base_id + 0x2A00,
    LocationType.crystal_heart:     celeste_base_id + 0x3000,
    LocationType.checkpoint:        celeste_base_id + 0x4000,
    LocationType.level_clear:       celeste_base_id + 0x5000,
    LocationType.key:               celeste_base_id + 0x6000,
    LocationType.gem:               celeste_base_id + 0x6A00,
    LocationType.binoculars:        celeste_base_id + 0x7000,
    LocationType.room_enter:        celeste_base_id + 0x8000,
    LocationType.clutter:           None,
}


def generate_location_table() -> dict[str, int]:
    from .Levels import Level, LocationType, load_logic_data
    level_data: dict[str, Level] = load_logic_data()
    location_table = {}

    location_counts: dict[LocationType, int] = {
        LocationType.strawberry:        0,
        LocationType.golden_strawberry: 0,
        LocationType.cassette:          0,
        LocationType.car:               0,
        LocationType.crystal_heart:     0,
        LocationType.checkpoint:        0,
        LocationType.level_clear:       0,
        LocationType.key:               0,
        LocationType.gem:               0,
        LocationType.binoculars:        0,
        LocationType.room_enter:        0,
    }

    for _, level in level_data.items():
        for room in level.rooms:
            if room.name != "10b_GOAL":
                location_table[room.display_name] = location_id_offsets[LocationType.room_enter] + location_counts[LocationType.room_enter]
                location_counts[LocationType.room_enter] += 1

            if room.checkpoint is not None and room.checkpoint != "Start":
                checkpoint_id: int = location_id_offsets[LocationType.checkpoint] + location_counts[LocationType.checkpoint]
                checkpoint_name: str = level.display_name + " - " + room.checkpoint
                location_table[checkpoint_name] = checkpoint_id
                location_counts[LocationType.checkpoint] += 1
                checkpoint_location_data_table[checkpoint_name] = CelesteLocationData(level.display_name, checkpoint_id)

                from .Items import add_checkpoint_to_table
                add_checkpoint_to_table(checkpoint_id, checkpoint_name)

            for region in room.regions:
                for location in region.locations:
                    if location_id_offsets[location.loc_type] is not None:
                        location_id = location_id_offsets[location.loc_type] + location_counts[location.loc_type]
                        location_table[location.display_name] = location_id
                        location_counts[location.loc_type] += 1

                        if location.loc_type == LocationType.key:
                            from .Items import add_key_to_table
                            add_key_to_table(location_id, location.display_name)

                        if location.loc_type == LocationType.gem:
                            from .Items import add_gem_to_table
                            add_gem_to_table(location_id, location.display_name)

    return location_table


def create_regions_and_locations(world: CelesteOpenWorld):
    menu_region = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu_region)

    world.active_checkpoint_names: list[str] = []
    world.goal_checkpoint_names: dict[str, str] = dict()
    world.active_key_names: list[str] = []
    world.active_gem_names: list[str] = []
    world.active_clutter_names: list[str] = []

    for _, level in world.level_data.items():
        if level.name not in world.active_levels:
            continue

        for room in level.rooms:
            room_region = Region(room.name + "_room", world.player, world.multiworld)
            world.multiworld.regions.append(room_region)

            for pre_region in room.regions:
                region = Region(pre_region.name, world.player, world.multiworld)
                world.multiworld.regions.append(region)

                for level_location in pre_region.locations:
                    if level_location.loc_type == LocationType.golden_strawberry:
                        if level_location.display_name == "Farewell - Golden Strawberry":
                            if not world.options.goal_area == "farewell_golden":
                                continue
                        elif not world.options.include_goldens:
                            continue

                    if level_location.loc_type == LocationType.car and not world.options.carsanity:
                        continue

                    if level_location.loc_type == LocationType.binoculars and not world.options.binosanity:
                        continue

                    if level_location.loc_type == LocationType.key:
                        world.active_key_names.append(level_location.display_name)

                    if level_location.loc_type == LocationType.gem:
                        world.active_gem_names.append(level_location.display_name)

                    location_rule = None
                    if len(level_location.possible_access) == 1:
                        only_access = level_location.possible_access[0]
                        if len(only_access) == 1:
                            only_item = level_location.possible_access[0][0]
                            def location_rule_func(state, only_item=only_item):
                                return state.has(only_item, world.player)
                            location_rule = location_rule_func
                        else:
                            def location_rule_func(state, only_access=only_access):
                                return state.has_all(only_access, world.player)
                            location_rule = location_rule_func
                    elif len(level_location.possible_access) > 0:
                        def location_rule_func(state, level_location=level_location):
                            for sublist in level_location.possible_access:
                                if state.has_all(sublist, world.player):
                                    return True
                            return False
                        location_rule = location_rule_func

                    if level_location.loc_type == LocationType.clutter:
                        world.active_clutter_names.append(level_location.display_name)
                        location = CelesteLocation(world.player, level_location.display_name, None, region)
                        if location_rule is not None:
                            set_rule(location, location_rule)
                        region.locations.append(location)
                        continue

                    location = CelesteLocation(world.player, level_location.display_name, world.location_name_to_id[level_location.display_name], region)
                    if location_rule is not None:
                        set_rule(location, location_rule)
                    region.locations.append(location)

            for pre_region in room.regions:
                region = world.get_region(pre_region.name)
                for connection in pre_region.connections:
                    connection_rule = None
                    if len(connection.possible_access) == 1:
                        only_access = connection.possible_access[0]
                        if len(only_access) == 1:
                            only_item = connection.possible_access[0][0]
                            def connection_rule_func(state, only_item=only_item):
                                return state.has(only_item, world.player)
                            connection_rule = connection_rule_func
                        else:
                            def connection_rule_func(state, only_access=only_access):
                                return state.has_all(only_access, world.player)
                            connection_rule = connection_rule_func
                    elif len(connection.possible_access) > 0:
                        def connection_rule_func(state, connection=connection):
                            for sublist in connection.possible_access:
                                if state.has_all(sublist, world.player):
                                    return True
                            return False

                        connection_rule = connection_rule_func

                    if connection_rule is None:
                        region.add_exits([connection.destination_name])
                    else:
                        region.add_exits([connection.destination_name], {connection.destination_name: connection_rule})
                region.add_exits([room_region.name])

            if room.checkpoint != None:
                if room.checkpoint == "Start":
                    if world.options.lock_goal_area and (level.name == world.goal_area or (level.name[:2] == world.goal_area[:2] == "10")):
                        world.goal_start_region: str = room.checkpoint_region
                    elif level.name == "8a":
                        world.epilogue_start_region: str = room.checkpoint_region
                    else:
                        menu_region.add_exits([room.checkpoint_region])
                else:
                    checkpoint_location_name = level.display_name + " - " + room.checkpoint
                    world.active_checkpoint_names.append(checkpoint_location_name)
                    checkpoint_rule = lambda state, checkpoint_location_name=checkpoint_location_name: state.has(checkpoint_location_name, world.player)
                    room_region.add_locations({
                        checkpoint_location_name: world.location_name_to_id[checkpoint_location_name]
                    }, CelesteLocation)

                    if world.options.lock_goal_area and (level.name == world.goal_area or (level.name[:2] == world.goal_area[:2] == "10")):
                        world.goal_checkpoint_names[room.checkpoint_region] = checkpoint_location_name
                    else:
                        menu_region.add_exits([room.checkpoint_region], {room.checkpoint_region: checkpoint_rule})

            if world.options.roomsanity:
                if room.name != "10b_GOAL":
                    room_location_name = room.display_name
                    room_region.add_locations({
                        room_location_name: world.location_name_to_id[room_location_name]
                    }, CelesteLocation)

        for room_connection in level.room_connections:
            source_region = world.get_region(room_connection.source.name)
            source_region.add_exits([room_connection.dest.name])
            if room_connection.two_way:
                dest_region = world.get_region(room_connection.dest.name)
                dest_region.add_exits([room_connection.source.name])

        if level.name == "10b":
            # Manually connect the two parts of Farewell
            source_region = world.get_region("10a_e-08_east")
            source_region.add_exits(["10b_f-door_west"])

        if level.name == "10c":
            # Manually connect the Golden room of Farewell
            golden_items: list[str] = [ItemName.traffic_blocks, ItemName.dash_refills, ItemName.double_dash_refills, ItemName.dream_blocks, ItemName.swap_blocks, ItemName.move_blocks, ItemName.blue_boosters, ItemName.springs, ItemName.feathers, ItemName.coins, ItemName.red_boosters, ItemName.kevin_blocks, ItemName.core_blocks, ItemName.fire_ice_balls, ItemName.badeline_boosters, ItemName.bird, ItemName.breaker_boxes, ItemName.pufferfish, ItemName.jellyfish, ItemName.pink_cassette_blocks, ItemName.blue_cassette_blocks, ItemName.yellow_cassette_blocks, ItemName.green_cassette_blocks]
            golden_rule = lambda state: state.has_all(golden_items, world.player)

            source_region_end = world.get_region("10b_j-19_top")
            source_region_end.add_exits(["10c_end-golden_bottom"], {"10c_end-golden_bottom": golden_rule})
            source_region_moon = world.get_region("10b_j-16_east")
            source_region_moon.add_exits(["10c_end-golden_bottom"], {"10c_end-golden_bottom": golden_rule})
            source_region_golden = world.get_region("10c_end-golden_top")
            source_region_golden.add_exits(["10b_GOAL_main"])


location_data_table: dict[str, int] = generate_location_table()


def generate_location_groups() -> dict[str, list[str]]:
    from .Levels import Level, LocationType, load_logic_data
    level_data: dict[str, Level] = load_logic_data()

    location_groups: dict[str, list[str]] = {
        "Strawberries": [name for name, id in location_data_table.items() if id >= location_id_offsets[LocationType.strawberry] and id < location_id_offsets[LocationType.golden_strawberry]],
        "Golden Strawberries": [name for name, id in location_data_table.items() if id >= location_id_offsets[LocationType.golden_strawberry] and id < location_id_offsets[LocationType.cassette]],
        "Cassettes": [name for name, id in location_data_table.items() if id >= location_id_offsets[LocationType.cassette] and id < location_id_offsets[LocationType.car]],
        "Cars": [name for name, id in location_data_table.items() if id >= location_id_offsets[LocationType.car] and id < location_id_offsets[LocationType.crystal_heart]],
        "Crystal Hearts": [name for name, id in location_data_table.items() if id >= location_id_offsets[LocationType.crystal_heart] and id < location_id_offsets[LocationType.checkpoint]],
        "Checkpoints": [name for name, id in location_data_table.items() if id >= location_id_offsets[LocationType.checkpoint] and id < location_id_offsets[LocationType.level_clear]],
        "Level Clears": [name for name, id in location_data_table.items() if id >= location_id_offsets[LocationType.level_clear] and id < location_id_offsets[LocationType.key]],
        "Keys": [name for name, id in location_data_table.items() if id >= location_id_offsets[LocationType.key] and id < location_id_offsets[LocationType.gem]],
        "Gems": [name for name, id in location_data_table.items() if id >= location_id_offsets[LocationType.gem] and id < location_id_offsets[LocationType.binoculars]],
        "Binoculars": [name for name, id in location_data_table.items() if id >= location_id_offsets[LocationType.binoculars] and id < location_id_offsets[LocationType.room_enter]],
        "Rooms": [name for name, id in location_data_table.items() if id >= location_id_offsets[LocationType.room_enter]],
    }

    for level in level_data.values():
        location_groups.update({level.display_name: [loc_name for loc_name, id in location_data_table.items() if level.display_name in loc_name]})

    return location_groups
