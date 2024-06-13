from typing import TYPE_CHECKING

from .data import FishData, EncounterMon, StaticPokemon
from .pokemon import get_random_pokemon

if TYPE_CHECKING:
    from . import PokemonCrystalWorld


def randomize_wild_pokemon(world: "PokemonCrystalWorld"):
    world.generated_wooper = get_random_pokemon(world)

    for grass_name, grass_encounters in world.generated_wild.grass.items():
        new_encounters = []
        for encounter in grass_encounters:
            new_encounters.append(encounter._replace(pokemon=get_random_pokemon(world)))
        world.generated_wild.grass[grass_name] = new_encounters

    for water_name, water_encounter in world.generated_wild.water.items():
        new_encounters = []
        for encounter in water_encounter:
            new_encounters.append(encounter._replace(pokemon=get_random_pokemon(world)))
        world.generated_wild.water[water_name] = new_encounters

    for fish_name, fish_area in world.generated_wild.fish.items():
        old_encounters = []
        good_encounters = []
        super_encounters = []
        for encounter in fish_area.old:
            old_encounters.append(encounter._replace(pokemon=get_random_pokemon(world)))
        for encounter in fish_area.good:
            good_encounters.append(encounter._replace(pokemon=get_random_pokemon(world)))
        for encounter in fish_area.super:
            super_encounters.append(encounter._replace(pokemon=get_random_pokemon(world)))

        world.generated_wild.fish[fish_name] = FishData(
            old_encounters,
            good_encounters,
            super_encounters
        )

    for tree_name, tree_data in world.generated_wild.tree.items():
        new_common = []
        new_rare = []
        for encounter in tree_data.common:
            new_common.append(encounter._replace(pokemon=get_random_pokemon(world)))
        for encounter in tree_data.rare:
            new_rare.append(encounter._replace(pokemon=get_random_pokemon(world)))


def randomize_static_pokemon(world: "PokemonCrystalWorld"):
    for static_name, pkmn_data in world.generated_static.items():
        world.generated_static[static_name] = pkmn_data._replace(pokemon=get_random_pokemon(world))
