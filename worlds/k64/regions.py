import typing

from BaseClasses import Region, CollectionState, ItemClassification
from .locations import K64Location, location_table
from .items import K64Item
from .names import LocationName, ItemName
from .rules import (burn_levels, needle_levels, stone_levels,
                    spark_levels, bomb_levels, ice_levels, cutter_levels, dedede_copy_levels, waddle_copy_levels)

if typing.TYPE_CHECKING:
    from . import K64World


class K64Region(Region):
    game = "Kirby 64 - The Crystal Shards"

    def copy_ability_sweep(self, state: "CollectionState"):
        for ability, regions in zip(["Burning Ability", "Stone Ability", "Ice Ability",
                                    "Needle Ability", "Bomb Ability", "Spark Ability", "Cutter Ability"],
                                    [burn_levels, stone_levels, ice_levels,
                                    needle_levels, bomb_levels, spark_levels, cutter_levels]):
            regions: list[str] = regions.copy()
            if ability in dedede_copy_levels and state.has(ItemName.king_dedede, self.player):
                regions.extend(dedede_copy_levels[ability])
            if ability in waddle_copy_levels and state.has(ItemName.waddle_dee, self.player):
                regions.extend(waddle_copy_levels[ability])
            if any(state.can_reach(region, "Region", self.player) for region in regions):
                state.prog_items[self.player][ability] = 1
            else:
                del state.prog_items[self.player][ability]

    def can_reach(self, state: CollectionState) -> bool:
        stale = state.k64_stale[self.player]
        if stale:
            state.k64_stale[self.player] = False
            self.copy_ability_sweep(state)
        return super().can_reach(state)


default_levels = {
    1: [0x640001, 0x640002, 0x640003, 0x640200],
    2: [0x640004, 0x640005, 0x640006, 0x640007, 0x640201],
    3: [0x640008, 0x640009, 0x64000A, 0x64000B, 0x640202],
    4: [0x64000C, 0x64000D, 0x64000E, 0x64000F, 0x640203],
    5: [0x640010, 0x640011, 0x640012, 0x640013, 0x640204],
    6: [0x640014, 0x640015, 0x640016, 0x640205],
}

first_stage_blacklist = {

}


def generate_valid_level(level, stage, possible_stages, slot_random):
    new_stage = slot_random.choice(possible_stages)
    if level == 1 and stage == 0 and new_stage in first_stage_blacklist:
        return generate_valid_level(level, stage, possible_stages, slot_random)
    else:
        return new_stage


def generate_valid_levels(world: "K64World", enforce_world: bool) -> dict:
    levels: typing.Dict[int, typing.List[typing.Optional[int]]] = {
        1: [None for _ in range(4)],
        2: [None for _ in range(5)],
        3: [None for _ in range(5)],
        4: [None for _ in range(5)],
        5: [None for _ in range(5)],
        6: [None for _ in range(4)]
    }

    possible_stages = list()
    for level in default_levels:
        for stage in range(len(default_levels[level]) - 1):
            possible_stages.append(default_levels[level][stage])

    if world.options.plando_connections:
        for connection in world.options.plando_connections:
            try:
                entrance_world, entrance_stage = connection.entrance.rsplit(" ", 1)
                stage_world, stage_stage = connection.exit.rsplit(" ", 1)
                new_stage = default_levels[LocationName.level_names_inverse[stage_world.strip()]][int(stage_stage) - 1]
                levels[LocationName.level_names_inverse[entrance_world.strip()]][int(entrance_stage) - 1] = new_stage
                possible_stages.remove(new_stage)

            except Exception:
                raise Exception(
                    f"Invalid connection: {connection.entrance} =>"
                    f" {connection.exit} for player {world.player} ({world.player_name})")

    for level in range(1, 7):
        for stage in range(len(default_levels[level]) - 1):
            # Randomize bosses separately
            try:
                if levels[level][stage] is None:
                    stage_candidates = [candidate for candidate in possible_stages
                                        if (not enforce_world)
                                        or (enforce_world and candidate in default_levels[level])
                                        ]
                    new_stage = generate_valid_level(level, stage, stage_candidates,
                                                     world.random)
                    possible_stages.remove(new_stage)
                    levels[level][stage] = new_stage
            except Exception:
                raise Exception(f"Failed to find valid stage for {level}-{stage}. Remaining Stages:{possible_stages}")
    """
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
        if boss_shuffle == 2:
            possible_bosses = [default_levels[world.random.randint(1, 5)][6]
                               for _ in range(5 - len(plando_bosses))]
        elif boss_shuffle == 3:
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
    else:"""
    for level in levels:
        if levels[level][len(default_levels[level]) - 1] is None:
            levels[level][len(default_levels[level]) - 1] = default_levels[level][len(default_levels[level]) - 1]

    return levels


def create_levels(world: "K64World") -> None:
    menu = K64Region("Menu", world.player, world.multiworld)
    level1 = K64Region("Pop Star", world.player, world.multiworld)
    level2 = K64Region("Rock Star", world.player, world.multiworld)
    level3 = K64Region("Aqua Star", world.player, world.multiworld)
    level4 = K64Region("Neo Star", world.player, world.multiworld)
    level5 = K64Region("Shiver Star", world.player, world.multiworld)
    level6 = K64Region("Ripple Star", world.player, world.multiworld)
    level7 = K64Region("Dark Star", world.player, world.multiworld)
    levels = {
        1: level1,
        2: level2,
        3: level3,
        4: level4,
        5: level5,
        6: level6,
    }
    level_shuffle = world.options.stage_shuffle.value
    if (hasattr(world.multiworld, "re_gen_passthrough")
        and "Kirby 64 - The Crystal Shards" in getattr(world.multiworld, "re_gen_passthrough")):
        slot_data = getattr(world.multiworld, "re_gen_passthrough")["Kirby 64 - The Crystal Shards"]
        world.player_levels = slot_data["player_levels"]
    elif level_shuffle != 0:
        world.player_levels = generate_valid_levels(world, level_shuffle == 1)

    for level in world.player_levels:
        for stage in range(len(world.player_levels[level])):
            real_stage = world.player_levels[level][stage]
            assert real_stage is not None, "Level tried to be sent with a None stage, incorrect plando?"
            # placeholder for when I want to add a data file eventually
            region = K64Region(location_table[real_stage].replace(" - Complete", "").replace(" Defeated", ""),
                               world.player, world.multiworld)
            levels[level].connect(region)
            crystals = [(((real_stage & 0xFF) - 1) * 3) + i + 0x640101 for i in range(3) if not real_stage & 0x200]
            locations = {
                location_table[code]: code for code in location_table
                if code in [real_stage, *crystals]
            }
            region.add_locations(locations, K64Location)
            world.multiworld.regions.append(region)

    level7.add_locations({LocationName.dark_star: None}, K64Location)

    menu.connect(level1, "Start Game")
    level1.connect(level2, "To Level 2")
    level2.connect(level3, "To Level 3")
    level3.connect(level4, "To Level 4")
    level4.connect(level5, "To Level 5")
    level5.connect(level6, "To Level 6")
    menu.connect(level7, "To Level 7")  # put the connection on menu, since you can reach it before level 6 on fast goal
    world.multiworld.regions.extend([menu, level1, level2, level3, level4, level5, level6, level7])

    goal_location = world.get_location(LocationName.dark_star)
    goal_location.place_locked_item(
        K64Item(ItemName.ribbons_crystal, ItemClassification.progression, None, world.player))
