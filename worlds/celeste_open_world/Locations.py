from typing import NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import Location, Region
from rule_builder.rules import Has, HasAll, Or

from .Levels import Level, LocationType, level_id_to_name
from .Names import ItemName

if TYPE_CHECKING:
    from . import CelesteOpenWorld
else:
    CelesteOpenWorld = object


celeste_base_id: int = 0xCA10000


class CelesteLocation(Location):
    game = "Celeste (Open World)"


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
    LocationType.breaker:           None,
}


def generate_location_table() -> dict[str, int]:
    from .Levels import Level, LocationType, load_logic_data
    level_data: dict[str, Level] = load_logic_data()
    location_table = {}

    location_table["Poetry Slam"] = celeste_base_id - 1

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

    per_level_side_items: dict[str, set[str]] = {}
    per_level_items: dict[str, set[str]] = {}
    per_side_items: dict[str, set[str]] = {}

    for _, level in level_data.items():
        if level.name[:-1] not in per_level_items:
            per_level_items[level.name[:-1]] = level.items.copy()
        else:
            per_level_items[level.name[:-1]].update(level.items)

        if level.name[:-1] != "10":
            per_level_side_items[level.name] = level.items.copy()

            if level.name[-1] not in per_side_items:
                per_side_items[level.name[-1]] = level.items.copy()
            else:
                per_side_items[level.name[-1]].update(level.items)
        else:
            per_side_items["a"].update(level.items)


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

    from .Items import add_interactable_to_table
    for level_name, level_items in per_level_side_items.items():
        for item_name in sorted(level_items):
            add_interactable_to_table(item_name, level_name[:-1], level_name[-1])

    for level_name, level_items in per_level_items.items():
        for item_name in sorted(level_items):
            add_interactable_to_table(item_name, level_name, None)

    for side_name, side_items in per_side_items.items():
        for item_name in sorted(side_items):
            add_interactable_to_table(item_name, None, side_name)

    return location_table


def convert_item(world: CelesteOpenWorld, level: Level, item: str) -> str:
    converted_item = item

    from .Items import interactable_item_data_table
    if item in interactable_item_data_table:
        if world.options.split_interactables.value == 1:
            converted_item = level_id_to_name[level.name[:-1]] + " - " + item
        elif world.options.split_interactables.value == 2:
            if level.name[:-1] != "10":
                converted_item = level.name[-1].upper() + "-Side " + item
            else:
                converted_item = "A-Side " + item
        elif world.options.split_interactables.value == 3:
            if level.name[:-1] != "10":
                converted_item = level_id_to_name[level.name[:-1]] + " " + level.name[-1].upper() + " - " + item
            else:
                converted_item = level_id_to_name[level.name[:-1]] + " - " + item

    return converted_item

def convert_item_list(world: CelesteOpenWorld, level: Level, item_list: list[str]) -> list[str]:
    converted_list: list[str] = []

    for item in item_list:
        converted_list.append(convert_item(world, level, item))

    return converted_list

def convert_item_list_list(world: CelesteOpenWorld, level: Level, item_list_list: list[list[str]]) -> list[list[str]]:
    converted_list_list: list[list[str]] = []

    for item_list in item_list_list:
        converted_list_list.append(convert_item_list(world, level, item_list))

    return converted_list_list


def create_regions_and_locations(world: CelesteOpenWorld):
    menu_region = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu_region)

    if world.options.goal_area.value == 9:
        from .Items import crystal_heart_item_data_table
        poetry_location = CelesteLocation(world.player, "Poetry Slam", world.location_name_to_id["Poetry Slam"], menu_region)
        world.set_rule(poetry_location, HasAll(*(crystal_heart_item_data_table.keys())))
        menu_region.locations.append(poetry_location)

    world.active_checkpoint_names: list[str] = []
    world.goal_checkpoint_names: dict[str, str] = dict()
    world.active_key_names: list[str] = []
    world.active_gem_names: list[str] = []
    world.active_clutter_names: list[str] = []
    world.active_breaker_names: list[str] = []

    golden_items: list[list[str]]

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
                    active_possible_access: list[list[str]] = level_location.possible_access

                    if world.options.logic_difficulty.value == 1:
                        active_possible_access = level_location.possible_access_vanilla
                    elif world.options.logic_difficulty.value == 2:
                        active_possible_access = level_location.possible_access_assist

                    if level_location.loc_type == LocationType.golden_strawberry:
                        if level_location.display_name == "Farewell - Golden Strawberry":
                            if not world.options.goal_area == "farewell_golden":
                                continue
                            golden_items = convert_item_list_list(world, level, active_possible_access)
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
                    if len(active_possible_access) == 1:
                        only_access = convert_item_list(world, level, active_possible_access[0])
                        if len(only_access) == 1:
                            location_rule = Has(only_access[0])
                        else:
                            location_rule = HasAll(*only_access)
                    elif len(active_possible_access) > 0:
                        possible_access = convert_item_list_list(world, level, active_possible_access)
                        location_rule = Or(*[HasAll(*sublist) for sublist in possible_access])

                    if level_location.loc_type == LocationType.clutter:
                        world.active_clutter_names.append(level_location.display_name)
                        location = CelesteLocation(world.player, level_location.display_name, None, region)
                        if location_rule is not None:
                            world.set_rule(location, location_rule)
                        region.locations.append(location)
                        continue

                    if level_location.loc_type == LocationType.breaker:
                        world.active_breaker_names.append(level_location.display_name)
                        location = CelesteLocation(world.player, level_location.display_name, None, region)
                        if location_rule is not None:
                            world.set_rule(location, location_rule)
                        region.locations.append(location)
                        continue

                    location = CelesteLocation(world.player, level_location.display_name, world.location_name_to_id[level_location.display_name], region)
                    if location_rule is not None:
                        world.set_rule(location, location_rule)
                    region.locations.append(location)

            for pre_region in room.regions:
                region = world.get_region(pre_region.name)
                for connection in pre_region.connections:
                    active_possible_access: list[list[str]] = connection.possible_access

                    if world.options.logic_difficulty.value == 1:
                        active_possible_access = connection.possible_access_vanilla
                    elif world.options.logic_difficulty.value == 2:
                        active_possible_access = connection.possible_access_assist

                    connection_rule = None
                    if len(active_possible_access) == 1:
                        only_access = convert_item_list(world, level, active_possible_access[0])
                        if len(only_access) == 1:
                            if only_access[0] == ItemName.cannot_access:
                                connection_rule = False
                            else:
                                connection_rule = Has(only_access[0])
                        else:
                            connection_rule = HasAll(*only_access)
                    elif len(active_possible_access) > 0:
                        possible_access = convert_item_list_list(world, level, active_possible_access)
                        connection_rule = Or(*[HasAll(*sublist) for sublist in possible_access])

                    if connection_rule == False:
                        continue
                    elif connection_rule is None:
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
                    checkpoint_rule = Has(checkpoint_location_name)
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
            def golden_access_rule_func(state, golden_items=golden_items.copy()):
                for sublist in golden_items:
                    if state.has_all(sublist, world.player):
                        return True
                return False

            source_region_end = world.get_region("10b_j-19_top")
            source_region_end.add_exits(["10c_end-golden_bottom"], {"10c_end-golden_bottom": golden_access_rule_func})
            source_region_moon = world.get_region("10b_j-16_east")
            source_region_moon.add_exits(["10c_end-golden_bottom"], {"10c_end-golden_bottom": golden_access_rule_func})
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
