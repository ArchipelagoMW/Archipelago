import copy
from typing import TYPE_CHECKING

from .data import data as crystal_data
from .moves import get_tmhm_compatibility, randomize_learnset
from .options import RandomizeTypes, RandomizePalettes, RandomizeBaseStats, RandomizeStarters
from .utils import get_random_filler_item

if TYPE_CHECKING:
    from . import PokemonCrystalWorld


def randomize_pokemon(world: "PokemonCrystalWorld"):
    # follow_evolutions can change types after the pokemon has already been randomized,
    # so we randomize types before all else
    if world.options.randomize_types.value:
        for pkmn_name, pkmn_data in world.generated_pokemon.items():
            evolution_line_list = [pkmn_name]
            if world.options.randomize_types.value == RandomizeTypes.option_follow_evolutions:
                # skip evolved pokemon if follow_evolutions
                if (not pkmn_data.is_base
                        and pkmn_name not in ["FLAREON", "JOLTEON", "VAPOREON", "ESPEON", "UMBREON"]):
                    continue
                for evo in pkmn_data.evolutions:
                    evolution_line_list.append(evo.pokemon)
                    evo_poke = world.generated_pokemon[evo.pokemon]
                    for second_evo in evo_poke.evolutions:
                        evolution_line_list.append(second_evo.pokemon)

            new_types = get_random_types(world.random)
            for pokemon in evolution_line_list:
                world.generated_pokemon[pokemon] = world.generated_pokemon[pokemon]._replace(types=new_types)

    for pkmn_name, pkmn_data in world.generated_pokemon.items():
        new_base_stats = pkmn_data.base_stats
        new_learnset = pkmn_data.learnset
        new_tm_hms = pkmn_data.tm_hm

        if world.options.randomize_palettes.value:
            if world.options.randomize_palettes.value == RandomizePalettes.option_match_types:
                world.generated_palettes[pkmn_name] = get_type_colors(pkmn_data.types, world.random)
            else:
                world.generated_palettes[pkmn_name] = get_random_colors(world.random)

        if world.options.randomize_base_stats.value:
            if world.options.randomize_base_stats.value == RandomizeBaseStats.option_keep_bst:
                new_base_stats = get_random_base_stats(world.random, pkmn_data.bst)
            else:
                new_base_stats = get_random_base_stats(world.random)

        if world.options.randomize_learnsets:
            new_learnset = randomize_learnset(world, pkmn_name)

        if world.options.tm_compatibility.value or world.options.hm_compatibility.value:
            new_tm_hms = get_tmhm_compatibility(world, pkmn_name)

        world.generated_pokemon[pkmn_name] = world.generated_pokemon[pkmn_name]._replace(tm_hm=new_tm_hms,
                                                                                         learnset=new_learnset,
                                                                                         base_stats=new_base_stats)


def randomize_starters(world: "PokemonCrystalWorld"):
    def get_starter_rival_fights(starter_name):
        return [(rival_name, rival) for rival_name, rival in world.generated_trainers.items() if
                rival_name.startswith("RIVAL_" + starter_name)]

    def set_rival_fight_starter(rival_name, rival, new_pokemon):
        # starter is always the last pokemon
        rival_pkmn = rival.pokemon[-1]._replace(pokemon=new_pokemon)
        new_party = rival.pokemon[:-1] + [rival_pkmn]
        world.generated_trainers[rival_name] = world.generated_trainers[rival_name]._replace(pokemon=new_party)

    base_only = world.options.randomize_starters.value == RandomizeStarters.option_unevolved_only
    for evo_line in world.generated_starters:
        # get all rival fights where the starter is unevolved
        rival_fights = get_starter_rival_fights(evo_line[0])
        # randomize starter
        starter_pokemon = get_random_pokemon(world, base_only=base_only)
        starter_data = world.generated_pokemon[starter_pokemon]
        evo_line[0] = starter_pokemon
        # replace unevolved starter rival fights with new starter
        for trainer_name, trainer in rival_fights:
            set_rival_fight_starter(trainer_name, trainer, starter_pokemon)

        # get all rival fights where the starter is middle evolution
        rival_fights = get_starter_rival_fights(evo_line[1])
        # get random evolution of randomized starter
        middle_evo_pokemon = get_random_pokemon_evolution(world.random, starter_pokemon, starter_data)
        middle_data = world.generated_pokemon[middle_evo_pokemon]
        evo_line[1] = middle_evo_pokemon
        # replace middle evolution rival fights with new middle evolution
        for trainer_name, trainer in rival_fights:
            set_rival_fight_starter(trainer_name, trainer, middle_evo_pokemon)

        # get all rival fights where the starter is final evolution
        rival_fights = get_starter_rival_fights(evo_line[2])
        # get random evolution of randomized starter
        final_evo_pokemon = get_random_pokemon_evolution(world.random, middle_evo_pokemon, middle_data)
        evo_line[2] = final_evo_pokemon
        # replace final evolution rival fights with new final evolution
        for trainer_name, trainer in rival_fights:
            set_rival_fight_starter(trainer_name, trainer, final_evo_pokemon)

    new_helditems = (get_random_filler_item(world.random),
                     get_random_filler_item(world.random),
                     get_random_filler_item(world.random))

    world.generated_starter_helditems = new_helditems


def get_random_pokemon(world: "PokemonCrystalWorld", types=None, base_only=False):
    # unown is excluded because it has a tendency to crash the game
    if types is None or types[0] is None:
        pokemon_pool = [pkmn_name for pkmn_name, pkmn_data in world.generated_pokemon.items() if
                        pkmn_name != "UNOWN" and (pkmn_data.is_base or not base_only)]
    else:
        pokemon_pool = [pkmn_name for pkmn_name, pkmn_data in world.generated_pokemon.items()
                        if pkmn_name != "UNOWN" and types[0] in pkmn_data.types or types[-1] in pkmn_data.types]
    return world.random.choice(pokemon_pool)


def get_random_nezumi(random):
    # 🐁
    pokemon_pool = ["RATTATA", "RATICATE", "NIDORAN_F", "NIDORAN_M", "NIDORINA", "NIDORINO", "PIKACHU", "RAICHU",
                    "SANDSHREW", "SANDSLASH", "CYNDAQUIL", "QUILAVA", "SENTRET", "FURRET", "MARILL"]
    return random.choice(pokemon_pool)


def get_random_pokemon_evolution(random, pkmn_name, pkmn_data):
    # if the pokemon has no evolutions
    if not len(pkmn_data.evolutions):
        # return the same pokemon
        return pkmn_name
    return random.choice(pkmn_data.evolutions).pokemon


def get_random_base_stats(random, bst=None):
    if bst is None:
        # sunkern to mewtwo
        bst = random.randint(180, 680)
    # add 0.5 to prevent a single stat exceeding 255
    # biggest possible variance on max bst is (1.5 * 680) / 4 = 255
    randoms = [random.random() + 0.5 for _i in range(0, 6)]
    total = sum(randoms)
    return [int((stat * bst) / total) for stat in randoms]


def get_random_types(random):
    data_types = copy.deepcopy(crystal_data.types)
    random.shuffle(data_types)
    new_types = [data_types.pop()]
    # approx. 110/251 pokemon are dual type in gen 2
    if random.randint(0, 24) < 11:
        new_types.append(data_types.pop())
    return new_types


# palettes stuff
def get_random_colors(random):
    colors = []
    for i in range(4):  # 2 normal colors, 2 shiny colors
        colors += convert_color(random.randint(0, 31), random.randint(0, 31), random.randint(0, 31))
    return list(colors)


def get_type_colors(types, random):
    type1 = types[0]
    type2 = types[-1]

    c1 = type_palettes[type1][0]
    c2 = type_palettes[type2][1]

    r1, g1, b1 = shift_color(c1[0], c1[1], c1[2], random)
    r2, g2, b2 = shift_color(c2[0], c2[1], c2[2], random)

    # normal colors
    color1 = convert_color(r1, g1, b1)
    color2 = convert_color(r2, g2, b2)

    # invert colors for shiny palette
    color3 = convert_color(31 - r1, 31 - g1, 31 - b1)
    color4 = convert_color(31 - r2, 31 - g2, 31 - b2)
    return list(color1 + color2 + color3 + color4)


def shift_color(r: int, g: int, b: int, random):
    return r + random.randint(-1, 1), \
           g + random.randint(-1, 1), \
           b + random.randint(-1, 1)


def convert_color(r: int, g: int, b: int):
    color = 0
    color += sorted((0, r, 31))[1]
    color += (sorted((0, g, 31))[1] << 5)
    color += (sorted((0, b, 31))[1] << 10)
    return color.to_bytes(2, "little")


type_palettes = {
    "NORMAL": [[31, 27, 31], [31, 24, 30]],
    "FIGHTING": [[30, 17, 1], [24, 9, 0]],
    "FLYING": [[17, 21, 31], [15, 11, 28]],
    "POISON": [[27, 21, 31], [15, 10, 24]],
    "GROUND": [[28, 19, 13], [24, 14, 0]],
    "ROCK": [[21, 20, 22], [18, 15, 4]],
    "BUG": [[23, 25, 6], [16, 18, 4]],
    "GHOST": [[10, 8, 14], [5, 3, 15]],
    "STEEL": [[19, 19, 21], [12, 14, 13]],
    "FIRE": [[31, 7, 0], [31, 15, 0]],
    "WATER": [[5, 8, 31], [2, 4, 26]],
    "GRASS": [[8, 31, 5], [4, 24, 2]],
    "ELECTRIC": [[31, 23, 7], [31, 17, 0]],
    "PSYCHIC_TYPE": [[31, 14, 30], [24, 4, 14]],
    "ICE": [[17, 25, 30], [22, 27, 30]],
    "DRAGON": [[16, 20, 25], [9, 12, 23]],
    "DARK": [[4, 2, 7], [3, 2, 6]],
}
