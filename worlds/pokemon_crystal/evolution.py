import logging
from collections import defaultdict
from dataclasses import replace
from random import Random
from typing import TYPE_CHECKING

from .data import data as crystal_data, PokemonData, EvolutionData, GrowthRate, EvolutionType, LogicalAccess
from .options import RandomizeEvolution, ConvergentEvolution
from .utils import pokemon_convert_friendly_to_ids

__ALL_KEY = "all"
__FINAL_KEY = "final"

if TYPE_CHECKING:
    from . import PokemonCrystalWorld


def randomize_evolution(world: "PokemonCrystalWorld") -> dict[str, list[str]]:
    # evolved_pkmn_dict:
    # Keys: Pokemon that can be evolved into.
    # Values: All Pokemon that evolve into this Pokemon. Relevant for breeding
    evolved_pkmn_dict: dict[str, list[str]] = defaultdict(list)

    if world.is_universal_tracker or not world.options.randomize_evolution:
        # Build the dict from original evolution data for breeding compatibility
        for pokemon_name, pokemon_data in world.generated_pokemon.items():
            for evolution in pokemon_data.evolutions:
                evolved_pkmn_dict[evolution.pokemon].append(pokemon_name)
        return evolved_pkmn_dict

    pkmn_groupings: dict[str, dict[str, PokemonData]] = generate_pokemon_groupings(world)

    for pokemon in world.generated_pokemon.keys():
        world.generated_pokemon[pokemon] = replace(world.generated_pokemon[pokemon], growth_rate=GrowthRate.MediumFast)

    evolving_pokemon = list((name, data) for name, data in world.generated_pokemon.items() if data.evolutions)
    if world.options.convergent_evolution == ConvergentEvolution.option_avoid:
        ordered_evolving_pokemon = sorted(evolving_pokemon, key=lambda pkmn: pkmn[1].bst, reverse=True)
    else:
        ordered_evolving_pokemon = sorted(evolving_pokemon, key=lambda pkmn: pkmn[1].id)

    for pkmn_name, pkmn_data in ordered_evolving_pokemon:

        new_evolutions: list[EvolutionData] = []
        valid_evolutions: dict[str, int] = __determine_valid_evolutions(world, pkmn_data, pkmn_groupings)

        if not valid_evolutions:
            valid_evolutions = __handle_no_valid_evolution(world, pkmn_data, pkmn_groupings)

        for evolution in pkmn_data.evolutions:
            new_evo_pkmn = world.random.choices(list(valid_evolutions.keys()),
                                                weights=list(valid_evolutions.values()))[0]
            evolved_pkmn_dict[new_evo_pkmn].append(pkmn_name)

            if world.options.convergent_evolution == ConvergentEvolution.option_avoid:
                for group in pkmn_groupings.values():
                    group.pop(new_evo_pkmn, None)

            new_evolutions.append(
                replace(
                    evolution,
                    pokemon=new_evo_pkmn
                )
            )

        world.generated_pokemon[pkmn_name] = replace(
            world.generated_pokemon[pkmn_name],
            evolutions=new_evolutions,
        )

    __update_base(evolved_pkmn_dict.keys(), world)

    return evolved_pkmn_dict


def generate_pokemon_groupings(world: "PokemonCrystalWorld") -> dict[str, dict[str, PokemonData]]:
    blocklist = pokemon_convert_friendly_to_ids(world, world.options.evolution_blocklist.value)
    blocklist.add("UNOWN")
    unblocked_pkmn: dict[str, PokemonData] = dict(
        (name, data) for name, data in world.generated_pokemon.items() if name not in blocklist
    )

    all_final_evolutions: dict[str, PokemonData] = dict(
        (name, data) for name, data in unblocked_pkmn.items() if not data.evolutions
    )

    if not all_final_evolutions:
        # If all final evolutions are blocklisted, throw the blocklist in the trash
        logging.warning(
            "Pokemon Crystal: Every final evolution is blocklisted for player %s. Ignoring the blocklist.",
            world.player_name)
        unblocked_pkmn = dict(
            (name, data) for name, data in world.generated_pokemon.items() if name != "UNOWN"
        )
        all_final_evolutions = dict(
            (name, data) for name, data in unblocked_pkmn.items() if not data.evolutions
        )

    pkmn_groupings = dict(all=unblocked_pkmn, final=all_final_evolutions)
    if world.options.randomize_evolution == RandomizeEvolution.option_match_a_type:
        pkmn_groupings = generate_type_groupings(pkmn_groupings)

    return pkmn_groupings


def generate_type_groupings(basic_groupings: dict[str, dict[str, PokemonData]]) -> dict[
    str, dict[str, PokemonData]]:
    type_groupings = dict((pkmn_type, dict()) for pkmn_type in crystal_data.types)

    for pkmn_name, pkmn_data in basic_groupings.get(__ALL_KEY).items():
        for pkmn_type in pkmn_data.types:
            type_groupings.get(pkmn_type)[pkmn_name] = pkmn_data

    return type_groupings | basic_groupings


def __determine_valid_evolutions(world: "PokemonCrystalWorld",
                                 pkmn_data: PokemonData,
                                 pkmn_groupings: dict[str, dict[str, PokemonData]]
                                 ) -> dict[str, int]:
    # dict of evolution -> weight
    valid_evolutions = dict()
    own_bst = pkmn_data.bst

    if world.options.randomize_evolution == RandomizeEvolution.option_match_a_type:
        for pkmn_type in pkmn_data.types:
            valid_evolutions.update(
                (name, 3 - len(data.types)) for name, data in pkmn_groupings.get(pkmn_type).items() if
                data.bst > own_bst
            )
    else:
        valid_evolutions.update(
            (name, 1) for name, data in pkmn_groupings.get(__ALL_KEY).items() if data.bst > own_bst
        )

    return valid_evolutions


def __update_base(evolved_pkmn, world: "PokemonCrystalWorld"):
    for pkmn_name in world.generated_pokemon.keys():
        world.generated_pokemon[pkmn_name] = replace(
            world.generated_pokemon[pkmn_name],
            is_base=pkmn_name not in evolved_pkmn,
        )


def __handle_no_valid_evolution(world: "PokemonCrystalWorld",
                                pkmn_data: PokemonData,
                                pkmn_groupings: dict[str, dict[str, PokemonData]]
                                ) -> dict[str, int]:
    if world.options.randomize_evolution == RandomizeEvolution.option_match_a_type:
        # Type backup: Highest BST final evolution within the type
        backup_evolution_options: dict[str, PokemonData] = dict()

        for pkmn_type in pkmn_data.types:
            backup_evolution_options.update(
                (name, data) for name, data in pkmn_groupings.get(pkmn_type).items() if not data.evolutions
            )

        if backup_evolution_options:
            max_bst: int = max(map(lambda data: data.bst, backup_evolution_options.values()))
            return dict(
                (name, 3 - len(data.types)) for name, data in backup_evolution_options.items() if data.bst == max_bst
            )
        else:
            # Type backup 2: Higher BST final evolution, dropping the type match
            own_bst = pkmn_data.bst

            second_backup: dict[str, int] = dict(
                (name, 3 - len(data.types)) for name, data in pkmn_groupings.get(__FINAL_KEY).items() if
                data.bst > own_bst
            )
            if second_backup:
                return second_backup

    # Just evolve into the final evolution with the highest bst
    final_group: dict[str, PokemonData] = pkmn_groupings.get(__FINAL_KEY)
    if final_group:
        max_bst: int = max(map(lambda data: data.bst, final_group.values()))
        return dict(
            (name, 1) for name, data in final_group.items() if data.bst == max_bst
        )
    else:
        # Last resort: Evolve into the blocklist
        # Because there are more final evolutions than evolving Pokemon, only a large blocklist can get here
        blocklist = pokemon_convert_friendly_to_ids(world, world.options.evolution_blocklist.value)
        blocked_final_evolutions = (
            name for name, data in world.generated_pokemon.items() if
            name in blocklist and not data.evolutions and name != "UNOWN"
        )
        return dict.fromkeys(blocked_final_evolutions, 1)


def get_logically_available_evolutions(world: "PokemonCrystalWorld") -> set[str]:
    evolution_pokemon = set()

    def recursive_evolution_add(evolving_pokemon):
        for evo in world.generated_pokemon[evolving_pokemon].evolutions:
            logical_access = LogicalAccess.InLogic if evolution_in_logic(world, evo) else LogicalAccess.OutOfLogic
            if not world.is_universal_tracker and logical_access is LogicalAccess.OutOfLogic: continue
            world.logic.evolution[evolving_pokemon].append((evo, logical_access))
            if evo.pokemon not in evolution_pokemon:
                if logical_access is LogicalAccess.InLogic:
                    evolution_pokemon.add(evo.pokemon)
                recursive_evolution_add(evo.pokemon)

    for pokemon in world.logic.available_pokemon:
        recursive_evolution_add(pokemon)

    return evolution_pokemon


def get_random_pokemon_evolution(random: Random, pkmn_name: str, pkmn_data: PokemonData):
    # if the Pokemon has no evolutions
    if not pkmn_data.evolutions:
        # return the same Pokemon
        return pkmn_name
    return random.choice(pkmn_data.evolutions).pokemon


def evolution_in_logic(world: "PokemonCrystalWorld", evolution: EvolutionData):
    if evolution.evo_type is EvolutionType.Level:
        return "Level" in world.options.evolution_methods_required.value
    if evolution.evo_type is EvolutionType.Happiness:
        return "Happiness" in world.options.evolution_methods_required.value
    if evolution.evo_type is EvolutionType.Item:
        return "Use Item" in world.options.evolution_methods_required.value
    if evolution.evo_type is EvolutionType.Stats:
        return "Level Tyrogue" in world.options.evolution_methods_required.value
    return False


def evolution_location_name(world: "PokemonCrystalWorld", from_pokemon: str, to_pokemon: str):
    return (f"Evolve {world.generated_pokemon[from_pokemon].friendly_name} "
            f"into {world.generated_pokemon[to_pokemon].friendly_name}")
