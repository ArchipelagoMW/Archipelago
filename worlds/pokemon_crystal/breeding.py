from dataclasses import replace
from typing import TYPE_CHECKING

from .data import LogicalAccess
from .options import RandomizeBreeding, BreedingMethodsRequired
from .utils import pokemon_convert_friendly_to_ids

if TYPE_CHECKING:
    from .world import PokemonCrystalWorld


def randomize_breeding(world: "PokemonCrystalWorld", preevolutions: dict[str, list[str]]) -> None:
    if world.is_universal_tracker or not world.options.randomize_breeding: return

    blocklist = pokemon_convert_friendly_to_ids(world, world.options.breeding_blocklist)
    global_breeding_pool = [poke for poke in world.generated_pokemon.keys() if poke not in blocklist]

    if "UNOWN" in global_breeding_pool: global_breeding_pool.remove("UNOWN")

    if not global_breeding_pool:
        global_breeding_pool = sorted(world.generated_pokemon.keys())
        global_breeding_pool.remove("UNOWN")

    global_base_pool = [poke for poke in global_breeding_pool if world.generated_pokemon[poke].is_base]

    if not global_base_pool:
        global_base_pool = [poke for poke, data in world.generated_pokemon.items() if data.is_base]

    for pokemon, pokemon_data in world.generated_pokemon.items():
        if not can_breed(world, pokemon): continue

        if world.options.randomize_breeding == RandomizeBreeding.option_completely_random:
            world.generated_pokemon[pokemon] = replace(pokemon_data,
                                                       produces_egg=world.random.choice(global_breeding_pool))

        elif world.options.randomize_breeding == RandomizeBreeding.option_decrease_bst:
            local_breeding_pool = [poke for poke in global_breeding_pool if
                                   world.generated_pokemon[poke].bst <= pokemon_data.bst]

            if not local_breeding_pool:
                local_breeding_pool = global_breeding_pool

            world.generated_pokemon[pokemon] = replace(pokemon_data,
                                                       produces_egg=world.random.choice(local_breeding_pool))
        elif world.options.randomize_breeding == RandomizeBreeding.option_any_base:
            world.generated_pokemon[pokemon] = replace(pokemon_data, produces_egg=world.random.choice(global_base_pool))
        elif world.options.randomize_breeding == RandomizeBreeding.option_line_base:
            local_breeding_pool = sorted(set(_recursive_get_bases(pokemon, preevolutions)))

            if not local_breeding_pool:
                local_breeding_pool = global_base_pool

            world.generated_pokemon[pokemon] = replace(pokemon_data,
                                                       produces_egg=world.random.choice(local_breeding_pool))


def _recursive_get_bases(pokemon: str, preevolutions: dict[str, list[str]]) -> list[str]:
    if pokemon not in preevolutions: return [pokemon]
    return sum([_recursive_get_bases(poke, preevolutions) for poke in preevolutions[pokemon]], [])


def get_logically_available_breeding(world: "PokemonCrystalWorld") -> set[str]:
    breeding_pokemon = set()

    for pokemon_id, data in world.generated_pokemon.items():
        if pokemon_id not in world.logic.available_pokemon: continue
        if not can_breed(world, pokemon_id): continue
        can_breed_ditto = bool(world.options.breeding_methods_required)
        can_breed_without_ditto = (world.options.breeding_methods_required == BreedingMethodsRequired.option_any
                                   and data.gender_ratio not in ("GENDER_F100", "GENDER_F0", "GENDER_UNKNOWN"))
        logical_access = LogicalAccess.InLogic if (
                can_breed_ditto or can_breed_without_ditto) else LogicalAccess.OutOfLogic
        if not world.is_universal_tracker and logical_access is LogicalAccess.OutOfLogic: continue
        world.logic.breeding[data.produces_egg].append((pokemon_id, logical_access))
        if logical_access is LogicalAccess.InLogic:
            breeding_pokemon.add(data.produces_egg)
        if data.produces_egg == "NIDORAN_F":
            world.logic.breeding["NIDORAN_M"].append((pokemon_id, logical_access))
            if logical_access is LogicalAccess.InLogic:
                breeding_pokemon.add("NIDORAN_M")

    return breeding_pokemon


def can_breed(world: "PokemonCrystalWorld", parent: str) -> bool:
    data = world.generated_pokemon[parent]
    if "EGG_DITTO" in data.egg_groups or "EGG_NONE" in data.egg_groups: return False
    return True


def breeding_is_randomized(world: "PokemonCrystalWorld") -> bool:
    return (world.options.randomize_evolution and world.options.randomize_breeding) or \
        world.options.randomize_breeding.value > RandomizeBreeding.option_line_base
