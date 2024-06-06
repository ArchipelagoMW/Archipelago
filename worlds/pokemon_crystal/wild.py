from typing import TYPE_CHECKING

from .data import FishData, EncounterMon, StaticPokemon
from .pokemon import get_random_pokemon

if TYPE_CHECKING:
    from . import PokemonCrystalWorld
else:
    PokemonCrystalWorld = object


def randomize_wild_pokemon(world: PokemonCrystalWorld):
    world.generated_wooper = get_random_pokemon(world)

    for grass_name, grass_encounters in world.generated_wild.grass.items():
        new_encounters = []
        for encounter in grass_encounters:
            new_pokemon = get_random_pokemon(world)
            new_encounter = EncounterMon(encounter.level, new_pokemon)
            new_encounters.append(new_encounter)
        world.generated_wild.grass[grass_name] = new_encounters

    for water_name, water_encounter in world.generated_wild.water.items():
        new_encounters = []
        for encounter in water_encounter:
            new_pokemon = get_random_pokemon(world)
            new_encounter = EncounterMon(encounter.level, new_pokemon)
            new_encounters.append(new_encounter)
        world.generated_wild.water[water_name] = new_encounters

    for fish_name, fish_area in world.generated_wild.fish.items():
        old_encounters = []
        good_encounters = []
        super_encounters = []
        for encounter in fish_area.old:
            new_pokemon = get_random_pokemon(world)
            new_encounter = EncounterMon(encounter.level, new_pokemon)
            old_encounters.append(new_encounter)
        for encounter in fish_area.good:
            new_pokemon = get_random_pokemon(world)
            new_encounter = EncounterMon(encounter.level, new_pokemon)
            good_encounters.append(new_encounter)
        for encounter in fish_area.super:
            new_pokemon = get_random_pokemon(world)
            new_encounter = EncounterMon(encounter.level, new_pokemon)
            super_encounters.append(new_encounter)

        world.generated_wild.fish[fish_name] = FishData(
            old_encounters,
            good_encounters,
            super_encounters
        )

    for tree_name, tree_data in world.generated_wild.tree.items():
        new_common = []
        new_rare = []
        for encounter in tree_data.common:
            new_pokemon = get_random_pokemon(world)
            new_encounter = EncounterMon(encounter.level, new_pokemon)
            new_common.append(new_encounter)
        for encounter in tree_data.rare:
            new_pokemon = get_random_pokemon(world)
            new_encounter = EncounterMon(encounter.level, new_pokemon)
            new_rare.append(new_encounter)


def randomize_static_pokemon(world: PokemonCrystalWorld):
    for static_name, pkmn_data in world.generated_static.items():
        new_pokemon = get_random_pokemon(world)
        new_static = StaticPokemon(new_pokemon, pkmn_data.addresses)
        world.generated_static[static_name] = new_static
