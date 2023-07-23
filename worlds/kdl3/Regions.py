import json
import os
import typing
from pkgutil import get_data

from BaseClasses import Entrance, Region
from worlds.AutoWorld import World
from .Locations import KDL3Location, location_table, level_consumables
from .Names import LocationName
from .Names.AnimalFriendSpawns import animal_friend_spawns
from .Options import BossShuffle
from .Room import Room
from ..generic.Rules import add_item_rule, add_rule

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
    0x77000B,  # 2-5 needs Kine
    0x770011,  # 3-5 needs Cutter
    0x77001C,  # 5-4 needs Burning
}


def generate_valid_level(level, stage, possible_stages, slot_random):
    new_stage = slot_random.choice(possible_stages)
    if level == 1 and stage == 0 and new_stage in first_stage_blacklist:
        return generate_valid_level(level, stage, possible_stages, slot_random)
    else:
        return new_stage


def generate_rooms(world: World, door_shuffle: bool, level_regions: typing.Dict[int, Region]):
    level_names = {LocationName.level_names[level]: level for level in LocationName.level_names}
    room_data = json.loads(get_data(__name__, os.path.join("data", "Rooms.json")))
    rooms: typing.Dict[str, Room] = dict()
    for room_entry in room_data:
        room = Room(room_entry["name"], world.player, world.multiworld, None, room_entry["level"], room_entry["stage"],
                    room_entry["room"], room_entry["pointer"], room_entry["music"], room_entry["default_exits"],
                    room_entry["animal_pointers"])
        room.add_locations({location: world.location_name_to_id[location] if location in world.location_name_to_id else
        None for location in room_entry["locations"] if not any([x in location for x in ["1-Up", "Maxim"]]) or
                            world.multiworld.consumables[world.player]}, KDL3Location)
        rooms[room.name] = room
    world.multiworld.regions.extend([rooms[room] for room in rooms])
    # fill animals, and set item rule
    if world.multiworld.animal_randomization[world.player] == 1:
        animal_pool = [animal_friend_spawns[spawn] for spawn in animal_friend_spawns
                       if spawn != "Ripple Field 5 - Animal 2"]
        if world.multiworld.accessibility[world.player] == 2:
            animal_pool.append("Pitch Spawn")
        world.multiworld.per_slot_randoms[world.player].shuffle(
            animal_pool)  # TODO: change to world.random once 0.4.1 support is deprecated
        if world.multiworld.accessibility[world.player] != 2:
            animal_pool.insert(28, "Pitch Spawn")
        # Ripple Field 5 - Animal 2 needs to be Pitch to ensure accessibility on non-minimal and non-door rando
        animal_friends = dict(zip(animal_friend_spawns.keys(), animal_pool))
    elif world.multiworld.animal_randomization[world.player] == 2:
        animal_base = ["Rick Spawn", "Kine Spawn", "Coo Spawn", "Nago Spawn", "ChuChu Spawn", "Pitch Spawn"]
        animal_pool = [world.multiworld.per_slot_randoms[world.player].choice(animal_base)
                       for _ in range(len(animal_friend_spawns) -
                                      (7 if world.multiworld.accessibility[world.player] < 2 else 6))]
        # have to guarantee one of each animal
        animal_pool.extend(animal_base)
        world.multiworld.per_slot_randoms[world.player].shuffle(
            animal_pool)  # TODO: change to world.random once 0.4.1 support is deprecated
        if world.multiworld.accessibility[world.player] != 2:
            animal_pool.insert(28, "Pitch Spawn")
        animal_friends = dict(zip(animal_friend_spawns.keys(), animal_pool))
    else:
        animal_friends = animal_friend_spawns.copy()
    for name in rooms:
        room = rooms[name]
        for location in room.locations:
            if "Animal" in location.name:
                add_item_rule(location, lambda item: item.name in {
                    "Rick Spawn", "Kine Spawn", "Coo Spawn", "Nago Spawn", "ChuChu Spawn", "Pitch Spawn"
                })
                location.place_locked_item(world.create_item(animal_friends[location.name]))
    first_rooms: typing.Dict[int, Room] = dict()
    if not door_shuffle:
        for name in rooms:
            room = rooms[name]
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
            if any(["Complete" in location.name for location in room.locations]):
                room.add_locations({f"{level_names[room.level]} {room.stage} - Stage Completion": None}, KDL3Location)

    for level in world.player_levels[world.player]:
        for stage in range(6):
            proper_stage = world.player_levels[world.player][level][stage]
            level_regions[level].add_exits([first_rooms[proper_stage].name],
                                           {first_rooms[proper_stage].name:
                                            (lambda state: True) if world.multiworld.open_world[world.player] or
                                            stage == 0 else lambda state, level=level, stage=stage: state.has(
                                                    f"{LocationName.level_names_inverse[level]} "
                                                    f"{f'{stage}'}"
                                                    f" - Stage Completion", world.player)})
        else:
            level_regions[level].add_exits([first_rooms[0x770200 + level - 1].name])


def generate_valid_levels(world: World, enforce_world: bool, enforce_pattern: bool) -> dict:
    levels: typing.Dict[int, typing.List[typing.Optional[int]]] = {
        1: [None for _ in range(7)],
        2: [None for _ in range(7)],
        3: [None for _ in range(7)],
        4: [None for _ in range(7)],
        5: [None for _ in range(7)]
    }

    possible_stages = list()
    for level in default_levels:
        for stage in range(6):
            possible_stages.append(default_levels[level][stage])

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
                    f" {connection.exit} for player {world.player} ({world.multiworld.player_name[world.player]})")

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
                    new_stage = generate_valid_level(level, stage, stage_candidates,
                                                     world.multiworld.per_slot_randoms[world.player])
                    possible_stages.remove(new_stage)
                    levels[level][stage] = new_stage
            except Exception:
                raise Exception(f"Failed to find valid stage for {level}-{stage}. Remaining Stages:{possible_stages}")

    # now handle bosses
    boss_shuffle: typing.Union[int, str] = world.multiworld.boss_shuffle[world.player].value
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
        if boss_shuffle == 2:
            possible_bosses = [default_levels[world.multiworld.per_slot_randoms[world.player].randint(1, 5)][6]
                               for _ in range(5 - len(plando_bosses))]
        elif boss_shuffle == 3:
            boss = world.multiworld.per_slot_randoms[world.player].randint(1, 5)
            possible_bosses = [default_levels[boss][6] for _ in range(5 - len(plando_bosses))]
        else:
            possible_bosses = [default_levels[level][6] for level in default_levels
                               if default_levels[level][6] not in plando_bosses]
        for level in levels:
            if levels[level][6] is None:
                boss = world.multiworld.per_slot_randoms[world.player].choice(possible_bosses)
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


def generate_locations_from_stages(stages: typing.List[int],
                                   consumables: bool) -> typing.Dict[str, typing.Optional[int]]:
    locations = dict()
    for stage in stages[:-1]:
        locations[location_table[stage]] = stage
        locations[location_table[stage + 0x100]] = stage + 0x100
        if consumables:
            stage_idx = stage & 0xFF
            if stage_idx in level_consumables:
                for consumable in level_consumables[stage_idx]:
                    loc_id = consumable + 0x770300
                    locations[location_table[loc_id]] = loc_id

    return locations


def create_levels(world: World) -> None:
    menu = Region("Menu", world.player, world.multiworld)
    start = Entrance(world.player, "Start Game", menu)
    menu.exits.append(start)
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
    start.connect(level1)
    level_shuffle = world.multiworld.stage_shuffle[world.player]
    if level_shuffle != 0:
        world.player_levels[world.player] = generate_valid_levels(
            world,
            level_shuffle == 1,
            level_shuffle == 2)
    else:
        world.player_levels[world.player] = default_levels.copy()
    generate_rooms(world, False, levels)

    level6.add_locations({LocationName.goals[world.multiworld.goal[world.player]]: None}, KDL3Location)

    tlv2 = Entrance(world.player, "To Level 2", level1)
    level1.exits.append(tlv2)
    tlv2.connect(level2)
    tlv3 = Entrance(world.player, "To Level 3", level2)
    level2.exits.append(tlv3)
    tlv3.connect(level3)
    tlv4 = Entrance(world.player, "To Level 4", level3)
    level3.exits.append(tlv4)
    tlv4.connect(level4)
    tlv5 = Entrance(world.player, "To Level 5", level4)
    level4.exits.append(tlv5)
    tlv5.connect(level5)
    tlv6 = Entrance(world.player, "To Level 6", menu)
    menu.exits.append(tlv6)
    tlv6.connect(level6)
    world.multiworld.regions += [menu, level1, level2, level3, level4, level5, level6]
