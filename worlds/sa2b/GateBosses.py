import typing

speed_characters_1 = "Sonic vs Shadow 1"
speed_characters_2 = "Sonic vs Shadow 2"
mech_characters_1 = "Tails vs Eggman 1"
mech_characters_2 = "Tails vs Eggman 2"
hunt_characters_1 = "Knuckles vs Rouge 1"
big_foot = "F-6t BIG FOOT"
hot_shot = "B-3x HOT SHOT"
flying_dog = "R-1/A FLYING DOG"
egg_golem_sonic = "Egg Golem (Sonic)"
egg_golem_eggman = "Egg Golem (Eggman)"
king_boom_boo = "King Boom Boo"

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

all_gate_bosses_table = {
    **gate_bosses_no_requirements_table,
    **gate_bosses_with_requirements_table,
}


def get_boss_name(boss: int):
    for key, value in gate_bosses_no_requirements_table.items():
        if value == boss:
            return key
    for key, value in gate_bosses_with_requirements_table.items():
        if value == boss:
            return key


def boss_has_requirement(boss: int):
    return boss >= len(gate_bosses_no_requirements_table)


def get_gate_bosses(world, player: int):
    selected_bosses: typing.List[int] = []
    boss_gates: typing.List[int] = []
    available_bosses: typing.List[str] = list(gate_bosses_no_requirements_table.keys())
    world.random.shuffle(available_bosses)
    halfway = False

    for x in range(world.number_of_level_gates[player]):
        if (not halfway) and ((x + 1) / world.number_of_level_gates[player]) > 0.5:
            available_bosses.extend(gate_bosses_with_requirements_table)
            world.random.shuffle(available_bosses)
            halfway = True
        selected_bosses.append(all_gate_bosses_table[available_bosses[0]])
        boss_gates.append(x + 1)
        available_bosses.remove(available_bosses[0])

    bosses: typing.Dict[int, int] = dict(zip(boss_gates, selected_bosses))

    return bosses
