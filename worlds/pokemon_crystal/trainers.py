from typing import TYPE_CHECKING

from .data import data as crystal_data
from .moves import get_random_move_from_learnset
from .options import RandomizeTrainerParties, RandomizeLearnsets
from .pokemon import get_random_pokemon, get_random_nezumi
from .utils import get_random_filler_item

if TYPE_CHECKING:
    from . import PokemonCrystalWorld
else:
    PokemonCrystalWorld = object


def is_rival_starter_pokemon(trainer_name, trainer_data, index):
    if not trainer_name.startswith("RIVAL"):
        return False
    # last pokemon
    return index == len(trainer_data.pokemon) - 1


def randomize_trainers(world: PokemonCrystalWorld):
    for trainer_name, trainer_data in world.generated_trainers.items():
        new_party = trainer_data.pokemon
        for i, pkmn_data in enumerate(trainer_data.pokemon):
            new_pkmn_data = pkmn_data

            if not is_rival_starter_pokemon(trainer_name, trainer_data, i):
                match_types = [None, None]
                if world.options.randomize_trainer_parties == RandomizeTrainerParties.option_match_types:
                    match_types = crystal_data.pokemon[new_pkmn_data[1]].types
                if "LASS_3" in trainer_name:
                    # easter egg
                    new_pokemon = get_random_nezumi(world.random)
                else:
                    new_pokemon = get_random_pokemon(world, match_types)
                new_pkmn_data[1] = new_pokemon
            if trainer_data.trainer_type in ["TRAINERTYPE_ITEM", "TRAINERTYPE_ITEM_MOVES"]:
                # If this trainer has items, add an item
                new_pkmn_data[2] = get_random_filler_item(world.random)
            if trainer_data.trainer_type not in ["TRAINERTYPE_MOVES", "TRAINERTYPE_ITEM_MOVES"]:
                # If this trainer doesn't have a predefined moveset, skip adding moves
                continue
            # we need to increase the offset by 1 to account for the item
            move_offset = 3 if trainer_data.trainer_type == "TRAINERTYPE_ITEM_MOVES" else 2
            while move_offset < len(new_pkmn_data):
                if (new_pkmn_data[move_offset] != "NO_MOVE"
                        or world.options.randomize_learnsets == RandomizeLearnsets.option_start_with_four_moves):
                    level = int(new_pkmn_data[0])
                    new_pkmn_data[move_offset] = get_random_move_from_learnset(world, new_pkmn_data[1], level)
                move_offset += 1
            new_party[i] = new_pkmn_data
        world.generated_trainers[trainer_name] = world.generated_trainers[trainer_name]._replace(pokemon=new_party)


def vanilla_trainer_movesets(world: PokemonCrystalWorld):
    # if trainers parties are vanilla but learnsets are randomized,
    # we need to change the predefined trainer movesets to account for this
    for trainer_name, trainer_data in world.generated_trainers.items():
        if trainer_data.trainer_type not in ["TRAINERTYPE_MOVES", "TRAINERTYPE_ITEM_MOVES"]:
            # if there's no predefined moveset, skip
            continue
        new_party = trainer_data.pokemon
        for i, pkmn_data in enumerate(trainer_data.pokemon):
            new_pkmn_data = pkmn_data
            # we need to increase the offset by 1 to account for the item
            move_offset = 3 if trainer_data.trainer_type == "TRAINERTYPE_ITEM_MOVES" else 2
            while move_offset < len(new_pkmn_data):
                # skip empty move slots, unless start with four moves is selected
                if (new_pkmn_data[move_offset] != "NO_MOVE"
                        or world.options.randomize_learnsets == RandomizeLearnsets.option_start_with_four_moves):
                    level = int(new_pkmn_data[0])
                    new_pkmn_data[move_offset] = get_random_move_from_learnset(world, new_pkmn_data[1], level)
                move_offset += 1
            new_party[i] = new_pkmn_data
        world.generated_trainers[trainer_name] = world.generated_trainers[trainer_name]._replace(pokemon=new_party)
