import copy
from typing import TYPE_CHECKING

from .data import data as crystal_data, LearnsetData, TMHMData
from .options import RandomizeLearnsets

if TYPE_CHECKING:
    from . import PokemonCrystalWorld


def randomize_learnset(world: "PokemonCrystalWorld", pkmn_name):
    pkmn_data = world.generated_pokemon[pkmn_name]
    learn_levels = []
    for move in pkmn_data.learnset:
        if move.move != "NO_MOVE":
            learn_levels.append(move.level)
        elif world.options.randomize_learnsets == RandomizeLearnsets.option_start_with_four_moves:
            learn_levels.insert(0, 1)

    new_learnset = [LearnsetData(level, get_random_move(world.random)) for level in learn_levels]

    # All moves available at Lv.1 that do damage (and don't faint the user)
    start_attacking = [learnset for learnset in new_learnset if
                       crystal_data.moves[learnset.move].power > 0
                       and learnset.move not in ["EXPLOSION", "SELFDESTRUCT", "STRUGGLE"]
                       and learnset.level == 1]

    if not len(start_attacking):  # if there are no attacking moves at Lv.1, add one
        new_learnset[0] = LearnsetData(1, get_random_move(world.random, attacking=True))

    return new_learnset


def get_random_move(random, move_type=None, attacking=None):
    # exclude beat up as it can softlock the game if an enemy trainer uses it
    if move_type is None:
        move_pool = [move_name for move_name, move_data in crystal_data.moves.items() if
                     not move_data.is_hm and move_name not in ["STRUGGLE", "BEAT_UP", "NO_MOVE", "STRUGGLE"]]
    else:
        move_pool = [move_name for move_name, move_data in crystal_data.moves.items() if
                     not move_data.is_hm and move_data.type == move_type
                     and move_name not in ["STRUGGLE", "BEAT_UP", "NO_MOVE", "STRUGGLE"]]
    if attacking is not None:
        move_pool = [move_name for move_name in move_pool if crystal_data.moves[move_name].power > 0]

    return random.choice(move_pool)


def get_tmhm_compatibility(world: "PokemonCrystalWorld", pkmn_name):
    pkmn_data = world.generated_pokemon[pkmn_name]
    tm_value = world.options.tm_compatibility.value
    hm_value = world.options.hm_compatibility.value
    tmhms = []
    for tm_name, tm_data in world.generated_tms.items():
        use_value = hm_value if tm_data.is_hm else tm_value
        # if the value is 0, use vanilla compatibility
        if use_value == 0:
            if tm_name in pkmn_data.tm_hm:
                tmhms.append(tm_name)
                continue
        # double chance if types match
        if tm_data.type in pkmn_data.types:
            use_value = use_value * 2
        if world.random.randint(0, 99) < use_value:
            tmhms.append(tm_name)
    return tmhms


def randomize_tms(world: "PokemonCrystalWorld"):
    move_pool = [move_data for move_name, move_data in copy.deepcopy(crystal_data.moves).items() if
                 not move_data.is_hm and move_name not in ["ROCK_SMASH", "NO_MOVE", "STRUGGLE"]]
    world.random.shuffle(move_pool)
    for tm_name, tm_data in world.generated_tms.items():
        if tm_data.is_hm or tm_name == "ROCK_SMASH":
            continue
        new_move = move_pool.pop()
        world.generated_tms[tm_name] = TMHMData(tm_data.tm_num, new_move.type, False, new_move.id)


def get_random_move_from_learnset(world: "PokemonCrystalWorld", pokemon, level):
    move_pool = [move.move for move in world.generated_pokemon[pokemon].learnset if
                 move.level <= level and move.move != "NO_MOVE"]
    # double learnset pool to dilute HMs slightly
    # exclude beat up as it can softlock the game if an enemy trainer uses it
    move_pool += move_pool + [move for move in world.generated_pokemon[pokemon].tm_hm if move != "BEAT_UP"]
    return world.random.choice(move_pool)
