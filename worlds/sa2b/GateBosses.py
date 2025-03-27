import typing

from BaseClasses import MultiWorld
from worlds.AutoWorld import World

from .Names import LocationName
from .Options import GateBossPlando


speed_characters_1 = "sonic vs shadow 1"
speed_characters_2 = "sonic vs shadow 2"
mech_characters_1 = "tails vs eggman 1"
mech_characters_2 = "tails vs eggman 2"
hunt_characters_1 = "knuckles vs rouge 1"
big_foot = "big foot"
hot_shot = "hot shot"
flying_dog = "flying dog"
egg_golem_sonic = "egg golem (sonic)"
egg_golem_eggman = "egg golem (eggman)"
king_boom_boo = "king boom boo"

gate_bosses_no_requirements_table = {
    speed_characters_1: 0,
    speed_characters_2: 1,
    mech_characters_1: 2,
    mech_characters_2: 3,
    hunt_characters_1: 4,
    big_foot: 5,
    hot_shot: 6,
    flying_dog: 7,
    egg_golem_sonic: 8,
    egg_golem_eggman: 9,
}

gate_bosses_with_requirements_table = {
    king_boom_boo: 10,
}

extra_boss_rush_bosses_table = {
    speed_characters_1: 11,
    speed_characters_2: 12,
    mech_characters_1: 13,
    mech_characters_2: 14,
    hunt_characters_1: 15,
}

all_gate_bosses_table = {
    **gate_bosses_no_requirements_table,
    **gate_bosses_with_requirements_table,
}


boss_id_to_name = {
    0: "Sonic vs Shadow 1",
    1: "Sonic vs Shadow 2",
    2: "Tails vs Eggman 1",
    3: "Tails vs Eggman 2",
    4: "Knuckles vs Rouge 1",
    5: "F-6t BIG FOOT",
    6: "B-3x HOT SHOT",
    7: "R-1/A FLYING DOG",
    8: "Egg Golem (Sonic)",
    9: "Egg Golem (Eggman)",
    10: "King Boom Boo",
    11: "Sonic vs Shadow 1",
    12: "Sonic vs Shadow 2",
    13: "Tails vs Eggman 1",
    14: "Tails vs Eggman 2",
    15: "Knuckles vs Rouge 1",
}

def get_boss_name(boss: int):
    return boss_id_to_name[boss]


def boss_has_requirement(boss: int):
    return boss >= len(gate_bosses_no_requirements_table)


def get_gate_bosses(world: World):
    selected_bosses: typing.List[int] = []
    boss_gates: typing.List[int] = []
    available_bosses: typing.List[str] = list(gate_bosses_no_requirements_table.keys())
    world.random.shuffle(available_bosses)

    gate_boss_plando: typing.Union[int, str] = world.options.gate_boss_plando.value
    plando_bosses = ["None", "None", "None", "None", "None"]
    if isinstance(gate_boss_plando, str):
        # boss plando
        options = gate_boss_plando.split(";")
        gate_boss_plando = GateBossPlando.options[options.pop()]
        for option in options:
            if "-" in option:
                loc, boss = option.split("-")
                boss_num = LocationName.boss_gate_names[loc]

                if boss_num >= world.options.number_of_level_gates.value:
                    # Don't reject bosses plando'd into gate bosses that won't exist
                    pass

                if boss in plando_bosses:
                    # TODO: Raise error here. Duplicates not allowed
                    pass

                plando_bosses[boss_num] = boss

                if boss in available_bosses:
                    available_bosses.remove(boss)

    for x in range(world.options.number_of_level_gates):
        if ("king boom boo" not in selected_bosses) and ("king boom boo" not in available_bosses) and ((x + 1) / world.options.number_of_level_gates) > 0.5:
            available_bosses.extend(gate_bosses_with_requirements_table)
            world.random.shuffle(available_bosses)

        chosen_boss = available_bosses[0]
        if plando_bosses[x] != "None":
            available_bosses.append(plando_bosses[x])
            chosen_boss = plando_bosses[x]

        selected_bosses.append(all_gate_bosses_table[chosen_boss])
        boss_gates.append(x + 1)
        available_bosses.remove(chosen_boss)

    bosses: typing.Dict[int, int] = dict(zip(boss_gates, selected_bosses))

    return bosses


def get_boss_rush_bosses(world: World):

    if world.options.boss_rush_shuffle == 0:
        boss_list_o = list(range(0, 16))
        boss_list_s = [5, 2, 0, 10, 8, 4, 3, 1, 6, 13, 7, 11, 9, 15, 14, 12]

        return dict(zip(boss_list_o, boss_list_s))
    elif world.options.boss_rush_shuffle == 1:
        boss_list_o = list(range(0, 16))
        boss_list_s = boss_list_o.copy()
        world.random.shuffle(boss_list_s)

        return dict(zip(boss_list_o, boss_list_s))
    elif world.options.boss_rush_shuffle == 2:
        boss_list_o = list(range(0, 16))
        boss_list_s = [world.random.choice(boss_list_o) for i in range(0, 16)]
        if 10 not in boss_list_s:
            boss_list_s[world.random.randint(0, 15)] = 10

        return dict(zip(boss_list_o, boss_list_s))
    elif world.options.boss_rush_shuffle == 3:
        boss_list_o = list(range(0, 16))
        boss_list_s = [world.random.choice(boss_list_o)] * len(boss_list_o)
        if 10 not in boss_list_s:
            boss_list_s[world.random.randint(0, 15)] = 10

        return dict(zip(boss_list_o, boss_list_s))
    else:
        return dict()
