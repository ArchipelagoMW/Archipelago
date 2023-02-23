import os
from typing import Dict
from .Data import get_extracted_data, load_json


all_pokemon_species = None


class PokemonSpecies:
    label: str
    id: int
    national_dex_number: int

    def __init__(self, label: str, id: int, national_dex_number: int):
        self.label = label
        self.id = id
        self.national_dex_number = national_dex_number


def get_random_species(random) -> PokemonSpecies:
    pokemon_species_list = [species for species in get_pokemon_species().values()]
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

        for species_name, species_data in pokemon_data.items():
            all_pokemon_species[species_name] = \
                PokemonSpecies(
                    species_data["label"],
                    extracted_data["constants"][species_name],
                    species_data["national_dex_number"],
                )
    
    return all_pokemon_species
