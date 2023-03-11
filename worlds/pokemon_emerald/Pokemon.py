import os
import random
from typing import Dict, List, NamedTuple, Tuple, Optional, FrozenSet
from .Data import get_extracted_data, load_json


all_pokemon_species = None
_move_blacklist = frozenset([
    165, # Struggle
    57,  # Surf
    249, # Rock Smash
    127, # Waterfall
    148, # Flash
    70,  # Strength
    19   # Fly
])


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


def get_random_species(random: random, nearby_bst: Optional[int] = None) -> PokemonSpecies:
    pokemon_species_list = [species for species in get_pokemon_species().values()]
    if (nearby_bst != None):
        pokemon_species_list = [species for species in pokemon_species_list if abs(sum(species.base_stats) - nearby_bst) < (nearby_bst / 10)]
    return pokemon_species_list[random.randrange(0, len(pokemon_species_list))]


def get_random_move(random: random, blacklist: Optional[FrozenSet[int]]) -> int:
    expanded_blacklist = _move_blacklist | (blacklist if blacklist != None else set())
    num_moves = get_extracted_data()["constants"]["MOVES_COUNT"]

    move = random.randrange(1, num_moves)
    while (move in expanded_blacklist):
        move = random.randrange(1, num_moves)

    return move


def get_random_damaging_move(random: random, blacklist: Optional[FrozenSet[int]]) -> int:
    expanded_blacklist = _move_blacklist | (blacklist if blacklist != None else set())

    move = random.choice(damaging_moves)
    while (move in expanded_blacklist):
        move = random.choice(damaging_moves)

    return move


def get_species_by_id(id: int) -> PokemonSpecies:
    return next(p for p in get_pokemon_species().values() if p.id == id)


def get_species_by_name(name: str) -> PokemonSpecies:
    return next(p for p in get_pokemon_species().values() if p.label == name)


def get_pokemon_species() -> Dict[str, PokemonSpecies]:
    global all_pokemon_species

    if (all_pokemon_species == None):
        all_pokemon_species = {}

        extracted_data = get_extracted_data()
        pokemon_attributes = load_json(os.path.join(os.path.dirname(__file__), "data/pokemon.json"))

        for species_constant_name, species_attributes in pokemon_attributes.items():
            species_id = extracted_data["constants"][species_constant_name]
            species_data = extracted_data["species"][species_id]

            all_pokemon_species[species_constant_name] = PokemonSpecies(
                    species_attributes["label"],
                    species_id,
                    species_attributes["national_dex_number"],
                    BaseStats(
                        species_data["base_stats"][0],
                        species_data["base_stats"][1],
                        species_data["base_stats"][2],
                        species_data["base_stats"][3],
                        species_data["base_stats"][4],
                        species_data["base_stats"][5]
                    ),
                    [species_data["types"][0], species_data["types"][1]],
                    [species_data["abilities"][0], species_data["abilities"][1]],
                    species_data["catch_rate"],
                    species_attributes["tm_hm_compatibility"]
                )

    return all_pokemon_species


damaging_moves = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 40, 41, 42, 44, 48, 49, 51, 52, 53, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 69, 70, 71, 72, 73, 75, 76, 80, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 93, 94, 98, 99, 101, 117, 118, 119, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 134, 136, 139, 140, 141, 142, 143, 144, 145, 146, 149, 152, 154, 155, 157, 158, 161, 162, 163, 167, 168, 172, 175, 177, 179, 180, 181, 183, 184, 185, 188, 189, 190, 192, 196, 198, 200, 202, 205, 206, 209, 210, 211, 216, 217, 218, 221, 222, 223, 224, 225, 228, 229, 231, 232, 233, 237, 238, 239, 242, 244, 245, 246, 247, 248, 249, 250, 251, 253, 257, 263, 264, 265, 276, 279, 280, 282, 284, 290, 291, 292, 295, 296, 299, 301, 302, 304, 305, 306, 307, 308, 309, 310, 311, 314, 315, 317, 318, 322, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 337, 338, 340, 341, 342, 344, 345, 348, 350, 351, 352, 353, 354]
