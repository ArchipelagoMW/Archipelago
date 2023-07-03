import typing
from BaseClasses import Entrance, Region
from worlds.AutoWorld import World
from .Locations import KDL3Location, location_table, level_consumables
from .Names import LocationName
from .Options import BossShuffle

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
    for level in levels:
        levels[level].add_locations(generate_locations_from_stages(world.player_levels[world.player][level],
                                                                   world.multiworld.consumables[world.player]),
                                    KDL3Location)

    for boss_flag, purification, idx, level in zip(["Level 1 Boss", "Level 2 Boss",
                                                    "Level 3 Boss", "Level 4 Boss", "Level 5 Boss"],
                                                   [LocationName.grass_land_whispy, LocationName.ripple_field_acro,
                                                    LocationName.sand_canyon_poncon, LocationName.cloudy_park_ado,
                                                    LocationName.iceberg_dedede],
                                                   [0x770200, 0x770201, 0x770202, 0x770203, 0x770204],
                                                   [level1, level2, level3, level4, level5]):
        level.add_locations({boss_flag: None, purification: idx, }, KDL3Location)

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
