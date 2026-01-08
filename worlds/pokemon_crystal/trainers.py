from dataclasses import replace
from typing import TYPE_CHECKING

from .data import data as crystal_data, TrainerPokemon
from .items import get_random_filler_item
from .moves import get_random_move_from_learnset
from .options import RandomizeTrainerParties, RandomizeLearnsets, BoostTrainerPokemonLevels
from .pokemon import get_random_pokemon, get_random_nezumi
from .utils import pokemon_convert_friendly_to_ids

if TYPE_CHECKING:
    from .world import PokemonCrystalWorld


def is_rival_starter_pokemon(trainer_name, trainer_data, index):
    if not trainer_name.startswith("RIVAL"):
        return False
    # last pokemon
    return index == len(trainer_data.pokemon) - 1


def get_last_evolution(world: "PokemonCrystalWorld", pokemon):
    """
    Returns the latest possible evolution for a Pokemon.
    If there's more than one way down through the evolution line, one is picked at random
    """
    pkmn_data = world.generated_pokemon[pokemon]
    if not pkmn_data.evolutions:
        return pokemon

    return get_last_evolution(world, world.random.choice(pkmn_data.evolutions).pokemon)


def randomize_trainers(world: "PokemonCrystalWorld"):
    if world.options.boost_trainers:
        boost_trainer_pokemon(world)

    if not world.options.randomize_trainer_parties:
        if world.options.randomize_learnsets:
            vanilla_trainer_movesets(world)
        return

    trainer_party_blocklist = pokemon_convert_friendly_to_ids(world, world.options.trainer_party_blocklist)

    for trainer_name, trainer_data in world.generated_trainers.items():
        new_party = []
        for i, pkmn_data in enumerate(trainer_data.pokemon):
            new_pokemon = pkmn_data.pokemon
            new_item = pkmn_data.item
            new_moves = pkmn_data.moves

            # If the current pokemon is rival's starter, don't change its evolution line
            if is_rival_starter_pokemon(trainer_name, trainer_data, i):
                if world.options.force_fully_evolved.value and pkmn_data.level >= world.options.force_fully_evolved:
                    new_pokemon = get_last_evolution(world, new_pokemon)
            else:
                match_types = None
                if world.options.randomize_trainer_parties == RandomizeTrainerParties.option_match_types:
                    match_types = crystal_data.pokemon[pkmn_data.pokemon].types

                if "LASS_ALICE" in trainer_name:
                    new_pokemon = get_random_nezumi(world.random)
                else:
                    new_pokemon = get_random_pokemon(
                        world,
                        types=match_types,
                        force_fully_evolved_at=world.options.force_fully_evolved,
                        current_level=pkmn_data.level,
                        blocklist=trainer_party_blocklist
                    )
            if pkmn_data.item is not None:
                # If this trainer has items, add an item
                new_item = get_random_filler_item(world)
            if pkmn_data.moves:
                new_moves = randomize_trainer_pokemon_moves(world, pkmn_data, new_pokemon)
            new_party.append(replace(pkmn_data, pokemon=new_pokemon, item=new_item, moves=new_moves))

        world.generated_trainers[trainer_name] = replace(world.generated_trainers[trainer_name], pokemon=new_party)


def vanilla_trainer_movesets(world: "PokemonCrystalWorld"):
    # if trainers parties are vanilla but learnsets are randomized,
    # we need to change the predefined trainer movesets to account for this
    for trainer_name, trainer_data in world.generated_trainers.items():
        if trainer_data.trainer_type not in ("TRAINERTYPE_MOVES", "TRAINERTYPE_ITEM_MOVES"):
            # if there's no predefined moveset, skip
            continue
        new_party = []
        for pkmn_data in trainer_data.pokemon:
            new_moves = randomize_trainer_pokemon_moves(world, pkmn_data, pkmn_data.pokemon)
            new_party.append(replace(pkmn_data, moves=new_moves))
        world.generated_trainers[trainer_name] = replace(world.generated_trainers[trainer_name], pokemon=new_party)


def randomize_trainer_pokemon_moves(world: "PokemonCrystalWorld", pkmn_data: TrainerPokemon, new_pokemon: str):
    new_moves = []
    for move in pkmn_data.moves:
        # fill out all four moves if start_with_four_moves, else append NO_MOVE
        if move != "NO_MOVE" or world.options.randomize_learnsets == RandomizeLearnsets.option_start_with_four_moves:
            new_move = get_random_move_from_learnset(world, new_pokemon, pkmn_data.level)
            new_moves.append(new_move)
        else:
            new_moves.append("NO_MOVE")
    return new_moves


def boost_trainer_pokemon(world: "PokemonCrystalWorld"):
    if not world.options.boost_trainers: return
    # mode 1 multiplies PKMN levels by boost | mode 2 sets the levels to boost
    for trainer_name, trainer_data in world.generated_trainers.items():
        new_party = []
        for trainer_mon in trainer_data.pokemon:
            new_level = trainer_mon.level
            if world.options.boost_trainers == BoostTrainerPokemonLevels.option_percentage_boost:
                new_level = int(trainer_mon.level * (1 + world.options.trainer_level_boost / 100))
                if new_level > 100: new_level = 100
            elif world.options.boost_trainers == BoostTrainerPokemonLevels.option_set_min_level:
                if new_level < world.options.trainer_level_boost:
                    new_level = world.options.trainer_level_boost
            new_party.append(replace(trainer_mon, level=new_level))
        world.generated_trainers[trainer_name] = replace(
            world.generated_trainers[trainer_name],
            pokemon=new_party
        )
