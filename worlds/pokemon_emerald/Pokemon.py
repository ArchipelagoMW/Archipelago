import os
from typing import Dict, List, NamedTuple, Tuple, Optional
from .Data import get_extracted_data, load_json


all_pokemon_species = None


class BaseStats(NamedTuple):
    hp: int
    attack: int
    defense: int
    speed: int
    special_attack: int
    special_defense: int


class PokemonSpecies(NamedTuple):
    label: str
    id: int
    national_dex_number: int
    base_stats: BaseStats
    types: Tuple[str, str]
    abilities: Tuple[str, str]
    catch_rate: int
    tm_hm_compatibility: str


def get_random_species(random, nearby_bst: Optional[int] = None) -> PokemonSpecies:
    pokemon_species_list = [species for species in get_pokemon_species().values()]
    if (nearby_bst != None):
        pokemon_species_list = [species for species in pokemon_species_list if abs(sum(species.base_stats) - nearby_bst) < (nearby_bst / 10)]
    return pokemon_species_list[random.randint(0, len(pokemon_species_list) - 1)]


def get_species_by_id(id: int) -> PokemonSpecies:
    return next(p for p in get_pokemon_species().values() if p.id == id)


def get_species_by_name(name: str) -> PokemonSpecies:
    return next(p for p in get_pokemon_species().values() if p.label == name)


def get_pokemon_species() -> Dict[str, PokemonSpecies]:
    global all_pokemon_species

    if (all_pokemon_species == None):
        all_pokemon_species = {}

        extracted_data = get_extracted_data()
        pokemon_data = load_json(os.path.join(os.path.dirname(__file__), "data/pokemon.json"))

        for species_constant_name, species_data in pokemon_data.items():
            all_pokemon_species[species_constant_name] = PokemonSpecies(
                    species_data["label"],
                    extracted_data["constants"][species_constant_name],
                    species_data["national_dex_number"],
                    BaseStats(
                        species_data["base_hp"],
                        species_data["base_attack"],
                        species_data["base_defense"],
                        species_data["base_speed"],
                        species_data["base_special_attack"],
                        species_data["base_special_defense"]
                    ),
                    [species_data["types"][0], species_data["types"][1]],
                    [species_data["abilities"][0], species_data["abilities"][1]],
                    species_data["catch_rate"],
                    species_data["tm_hm_compatibility"]
                )

    return all_pokemon_species
