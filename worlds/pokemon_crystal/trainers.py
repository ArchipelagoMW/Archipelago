from typing import TYPE_CHECKING

from .data import data as crystal_data
from .moves import get_random_move_from_learnset
from .options import RandomizeTrainerParties, RandomizeLearnsets
from .pokemon import get_random_pokemon, get_random_nezumi
from .utils import get_random_filler_item

if TYPE_CHECKING:
    from . import PokemonCrystalWorld


def is_rival_starter_pokemon(trainer_name, trainer_data, index):
    if not trainer_name.startswith("RIVAL"):
        return False
    # last pokemon
    return index == len(trainer_data.pokemon) - 1


def randomize_trainers(world: "PokemonCrystalWorld"):
    for trainer_name, trainer_data in world.generated_trainers.items():
        new_party = trainer_data.pokemon
        for i, pkmn_data in enumerate(trainer_data.pokemon):
            new_pokemon = pkmn_data.pokemon
            new_item = pkmn_data.item
            new_moves = pkmn_data.moves
            if not is_rival_starter_pokemon(trainer_name, trainer_data, i):
                match_types = [None, None]
                if world.options.randomize_trainer_parties == RandomizeTrainerParties.option_match_types:
                    match_types = crystal_data.pokemon[pkmn_data.pokemon].types
                if "LASS_3" in trainer_name:
                    new_pokemon = get_random_nezumi(world.random)
                else:
                    new_pokemon = get_random_pokemon(world, match_types)
            if pkmn_data.item is not None:
                # If this trainer has items, add an item
                new_item = get_random_filler_item(world.random)
            if len(pkmn_data.moves):
                new_moves = randomize_trainer_pokemon_moves(world, pkmn_data, new_pokemon)
            new_party[i] = pkmn_data._replace(pokemon=new_pokemon, item=new_item, moves=new_moves)
        world.generated_trainers[trainer_name] = world.generated_trainers[trainer_name]._replace(pokemon=new_party)


def vanilla_trainer_movesets(world: "PokemonCrystalWorld"):
    # if trainers parties are vanilla but learnsets are randomized,
    # we need to change the predefined trainer movesets to account for this
    for trainer_name, trainer_data in world.generated_trainers.items():
        if trainer_data.trainer_type not in ["TRAINERTYPE_MOVES", "TRAINERTYPE_ITEM_MOVES"]:
            # if there's no predefined moveset, skip
            continue
        new_party = trainer_data.pokemon
        for i, pkmn_data in enumerate(trainer_data.pokemon):
            new_moves = randomize_trainer_pokemon_moves(world, pkmn_data, pkmn_data.pokemon)
            new_party[i] = pkmn_data._replace(moves=new_moves)
        world.generated_trainers[trainer_name] = world.generated_trainers[trainer_name]._replace(pokemon=new_party)


def randomize_trainer_pokemon_moves(world, pkmn_data, new_pokemon):
    new_moves = pkmn_data.moves
    for i, move in enumerate(pkmn_data.moves):
        # fill out all four moves if start_with_four_moves, else skip empty slots
        if move != "NO_MOVE" or world.options.randomize_learnsets == RandomizeLearnsets.option_start_with_four_moves:
            new_move = get_random_move_from_learnset(world, new_pokemon, pkmn_data.level)
            new_moves[i] = new_move
    return new_moves
