import orjson
import os
import typing
from pkgutil import get_data

from BaseClasses import Region
from worlds.generic.Rules import add_item_rule
from .Locations import KDL3Location
from .Names import LocationName
from .Options import BossShuffle
from .Room import KDL3Room

if typing.TYPE_CHECKING:
    from . import KDL3World

default_levels = {
    1: [0x770001, 0x770002, 0x770003, 0x770004, 0x770005, 0x770006, 0x770200],
    2: [0x770007, 0x770008, 0x770009, 0x77000A, 0x77000B, 0x77000C, 0x770201],
    3: [0x77000D, 0x77000E, 0x77000F, 0x770010, 0x770011, 0x770012, 0x770202],
    4: [0x770013, 0x770014, 0x770015, 0x770016, 0x770017, 0x770018, 0x770203],
    5: [0x770019, 0x77001A, 0x77001B, 0x77001C, 0x77001D, 0x77001E, 0x770204],
}

first_stage_blacklist = {
    # We want to confirm that the first stage can be completed without any items
    0x77000B,  # 2-5 needs Kine
    0x770011,  # 3-5 needs Cutter
    0x77001C,  # 5-4 needs Burning
}

first_world_limit = {
    # We need to limit the number of very restrictive stages in level 1 on solo gens
    *first_stage_blacklist,  # all three of the blacklist stages need 2+ items for both checks
    0x770007,
    0x770008,
    0x770013,
    0x77001E,

}


def generate_valid_level(world: "KDL3World", level, stage, possible_stages, placed_stages):
    new_stage = world.random.choice(possible_stages)
    if level == 1:
        if stage == 0 and new_stage in first_stage_blacklist:
            return generate_valid_level(world, level, stage, possible_stages, placed_stages)
        elif not (world.multiworld.players > 1 or world.options.consumables or world.options.starsanity) and \
                new_stage in first_world_limit and \
                sum(p_stage in first_world_limit for p_stage in placed_stages) >= 2:
            return generate_valid_level(world, level, stage, possible_stages, placed_stages)
    return new_stage


def generate_rooms(world: "KDL3World", level_regions: typing.Dict[int, Region]):
    level_names = {LocationName.level_names[level]: level for level in LocationName.level_names}
    room_data = orjson.loads(get_data(__name__, os.path.join("data", "Rooms.json")))
    rooms: typing.Dict[str, KDL3Room] = dict()
    for room_entry in room_data:
        room = KDL3Room(room_entry["name"], world.player, world.multiworld, None, room_entry["level"],
                        room_entry["stage"], room_entry["room"], room_entry["pointer"], room_entry["music"],
                        room_entry["default_exits"], room_entry["animal_pointers"], room_entry["enemies"],
                        room_entry["entity_load"], room_entry["consumables"], room_entry["consumables_pointer"])
        room.add_locations({location: world.location_name_to_id[location] if location in world.location_name_to_id else
                            None for location in room_entry["locations"]
                            if (not any(x in location for x in ["1-Up", "Maxim"]) or
                                world.options.consumables.value) and ("Star" not in location
                                                                      or world.options.starsanity.value)},
                           KDL3Location)
        rooms[room.name] = room
        for location in room.locations:
            if "Animal" in location.name:
                add_item_rule(location, lambda item: item.name in {
                    "Rick Spawn", "Kine Spawn", "Coo Spawn", "Nago Spawn", "ChuChu Spawn", "Pitch Spawn"
                })
    world.rooms = list(rooms.values())
    world.multiworld.regions.extend(world.rooms)

    first_rooms: typing.Dict[int, KDL3Room] = dict()
    for name, room in rooms.items():
        if room.room == 0:
            if room.stage == 7:
                first_rooms[0x770200 + room.level - 1] = room
            else:
                first_rooms[0x770000 + ((room.level - 1) * 6) + room.stage] = room
        exits = dict()
        for def_exit in room.default_exits:
            target = f"{level_names[room.level]} {room.stage} - {def_exit['room']}"
            access_rule = tuple(def_exit["access_rule"])
            exits[target] = lambda state, rule=access_rule: state.has_all(rule, world.player)
        room.add_exits(
            exits.keys(),
            exits
        )
        if world.options.open_world:
            if any("Complete" in location.name for location in room.locations):
                room.add_locations({f"{level_names[room.level]} {room.stage} - Stage Completion": None},
                                   KDL3Location)

    for level in world.player_levels:
        for stage in range(6):
            proper_stage = world.player_levels[level][stage]
            stage_name = world.multiworld.get_location(world.location_id_to_name[proper_stage],
                                                       world.player).name.replace(" - Complete", "")
            stage_regions = [rooms[room] for room in rooms if stage_name in rooms[room].name]
            for region in stage_regions:
                region.level = level
                region.stage = stage
            if world.options.open_world or stage == 0:
                level_regions[level].add_exits([first_rooms[proper_stage].name])
            else:
                world.multiworld.get_location(world.location_id_to_name[world.player_levels[level][stage - 1]],
                                              world.player).parent_region.add_exits([first_rooms[proper_stage].name])
        level_regions[level].add_exits([first_rooms[0x770200 + level - 1].name])


def generate_valid_levels(world: "KDL3World", enforce_world: bool, enforce_pattern: bool) -> dict:
    levels: typing.Dict[int, typing.List[typing.Optional[int]]] = {
        1: [None] * 7,
        2: [None] * 7,
        3: [None] * 7,
        4: [None] * 7,
        5: [None] * 7,
    }

    possible_stages = [default_levels[level][stage] for level in default_levels for stage in range(6)]
    if world.multiworld.plando_connections[world.player]:
        for connection in world.multiworld.plando_connections[world.player]:
            try:
                entrance_world, entrance_stage = connection.entrance.rsplit(" ", 1)
                stage_world, stage_stage = connection.exit.rsplit(" ", 1)
                new_stage = default_levels[LocationName.level_names[stage_world.strip()]][int(stage_stage) - 1]
                levels[LocationName.level_names[entrance_world.strip()]][int(entrance_stage) - 1] = new_stage
                possible_stages.remove(new_stage)

            except Exception:
                raise Exception(
                    f"Invalid connection: {connection.entrance} =>"
                    f" {connection.exit} for player {world.player} ({world.player_name})")

    for level in range(1, 6):
        for stage in range(6):
            # Randomize bosses separately
            try:
                if levels[level][stage] is None:
                    stage_candidates = [candidate for candidate in possible_stages
                                        if (enforce_world and candidate in default_levels[level])
                                        or (enforce_pattern and ((candidate - 1) & 0x00FFFF) % 6 == stage)
                                        or (enforce_pattern == enforce_world)
                                        ]
                    new_stage = generate_valid_level(world, level, stage, stage_candidates, levels[level])
                    possible_stages.remove(new_stage)
                    levels[level][stage] = new_stage
            except Exception:
                raise Exception(f"Failed to find valid stage for {level}-{stage}. Remaining Stages:{possible_stages}")

    # now handle bosses
    boss_shuffle: typing.Union[int, str] = world.options.boss_shuffle.value
    plando_bosses = []
    if isinstance(boss_shuffle, str):
        # boss plando
        options = boss_shuffle.split(";")
        boss_shuffle = BossShuffle.options[options.pop()]
        for option in options:
            if "-" in option:
                loc, boss = option.split("-")
                loc = loc.title()
                boss = boss.title()
                levels[LocationName.level_names[loc]][6] = LocationName.boss_names[boss]
                plando_bosses.append(LocationName.boss_names[boss])
            else:
                option = option.title()
                for level in levels:
                    if levels[level][6] is None:
                        levels[level][6] = LocationName.boss_names[option]
                        plando_bosses.append(LocationName.boss_names[option])

    if boss_shuffle > 0:
        if boss_shuffle == BossShuffle.option_full:
            possible_bosses = [default_levels[world.random.randint(1, 5)][6]
                               for _ in range(5 - len(plando_bosses))]
        elif boss_shuffle == BossShuffle.option_singularity:
            boss = world.random.randint(1, 5)
            possible_bosses = [default_levels[boss][6] for _ in range(5 - len(plando_bosses))]
        else:
            possible_bosses = [default_levels[level][6] for level in default_levels
                               if default_levels[level][6] not in plando_bosses]
        for level in levels:
            if levels[level][6] is None:
                boss = world.random.choice(possible_bosses)
                levels[level][6] = boss
                possible_bosses.remove(boss)
    else:
        for level in levels:
            if levels[level][6] is None:
                levels[level][6] = default_levels[level][6]

    for level in levels:
        for stage in range(7):
            assert levels[level][stage] is not None, "Level tried to be sent with a None stage, incorrect plando?"

    return levels


def create_levels(world: "KDL3World") -> None:
    menu = Region("Menu", world.player, world.multiworld)
    level1 = Region("Grass Land", world.player, world.multiworld)
    level2 = Region("Ripple Field", world.player, world.multiworld)
    level3 = Region("Sand Canyon", world.player, world.multiworld)
    level4 = Region("Cloudy Park", world.player, world.multiworld)
    level5 = Region("Iceberg", world.player, world.multiworld)
    level6 = Region("Hyper Zone", world.player, world.multiworld)
    levels = {
        1: level1,
        2: level2,
        3: level3,
        4: level4,
        5: level5,
    }
    level_shuffle = world.options.stage_shuffle.value
    if level_shuffle != 0:
        world.player_levels = generate_valid_levels(
            world,
            level_shuffle == 1,
            level_shuffle == 2)

    generate_rooms(world, levels)

    level6.add_locations({LocationName.goals[world.options.goal]: None}, KDL3Location)

    menu.connect(level1, "Start Game")
    level1.connect(level2, "To Level 2")
    level2.connect(level3, "To Level 3")
    level3.connect(level4, "To Level 4")
    level4.connect(level5, "To Level 5")
    menu.connect(level6, "To Level 6")  # put the connection on menu, since you can reach it before level 5 on fast goal
    world.multiworld.regions += [menu, level1, level2, level3, level4, level5, level6]
