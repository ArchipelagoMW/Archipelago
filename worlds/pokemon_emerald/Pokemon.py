import os
import random
from typing import List, NamedTuple, Tuple, Optional, FrozenSet
from .Data import get_extracted_data, load_json


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
    types: Tuple[int, int]
    abilities: Tuple[int, int]
    catch_rate: int
    tm_hm_compatibility: str


species_data: List[PokemonSpecies] = []
_damaging_moves = frozenset([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 40, 41, 42, 44, 48, 49, 51, 52, 53, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 69, 70, 71, 72, 73, 75, 76, 80, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 93, 94, 98, 99, 101, 117, 118, 119, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 134, 136, 139, 140, 141, 142, 143, 144, 145, 146, 149, 152, 154, 155, 157, 158, 161, 162, 163, 167, 168, 172, 175, 177, 179, 180, 181, 183, 184, 185, 188, 189, 190, 192, 196, 198, 200, 202, 205, 206, 209, 210, 211, 216, 217, 218, 221, 222, 223, 224, 225, 228, 229, 231, 232, 233, 237, 238, 239, 242, 244, 245, 246, 247, 248, 249, 250, 251, 253, 257, 263, 264, 265, 276, 279, 280, 282, 284, 290, 291, 292, 295, 296, 299, 301, 302, 304, 305, 306, 307, 308, 309, 310, 311, 314, 315, 317, 318, 322, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 337, 338, 340, 341, 342, 344, 345, 348, 350, 351, 352, 353, 354])
_move_blacklist = frozenset([
    0,   # MOVE_NONE
    165, # Struggle
    15,  # Cut
    148, # Flash
    249, # Rock Smash
    70,  # Strength
    57,  # Surf
    19,  # Fly
    291, # Dive
    127  # Waterfall
])


def get_species_by_id(id: int) -> Optional[PokemonSpecies]:
    for species in species_data:
        if species.id == id:
            return species
        if species.id > id:
            return None

    return None


def get_species_by_name(name: str) -> Optional[PokemonSpecies]:
    for species in species_data:
        if species.label == name:
            return species

    return None


def get_random_species(random: random, nearby_bst: Optional[int] = None, type: Optional[int] = None) -> PokemonSpecies:
    pokemon_species_list = species_data

    if nearby_bst is not None:
        def has_nearby_bst(species: PokemonSpecies):
            return abs(sum(species.base_stats) - nearby_bst) < nearby_bst / 10

        pokemon_species_list = list(filter(has_nearby_bst, pokemon_species_list))
    if type is not None:
        pokemon_species_list = [species for species in pokemon_species_list if type in species.types]

    return pokemon_species_list[random.randrange(0, len(pokemon_species_list))]


def get_random_move(random: random, blacklist: Optional[FrozenSet[int]] = None) -> int:
    global _move_blacklist
    expanded_blacklist = _move_blacklist | (blacklist if blacklist is not None else set())
    num_moves = get_extracted_data()["constants"]["MOVES_COUNT"]

    move = random.randrange(1, num_moves)
    while (move in expanded_blacklist):
        move = random.randrange(1, num_moves)

    return move


def get_random_damaging_move(random: random, blacklist: Optional[FrozenSet[int]] = None) -> int:
    global _move_blacklist
    global _damaging_moves
    expanded_blacklist = _move_blacklist | (blacklist if blacklist is not None else set())

    move_options = list(_damaging_moves)

    move = random.choice(move_options)
    while (move in expanded_blacklist):
        move = random.choice(move_options)

    return move


def init_species_data():
    global species_data

    species_data = []

    extracted_data = get_extracted_data()
    pokemon_attributes = load_json(os.path.join(os.path.dirname(__file__), "data/pokemon.json"))

    for species_constant_name, species_attributes in pokemon_attributes.items():
        species_id = extracted_data["constants"][species_constant_name]
        individual_species_data = extracted_data["species"][species_id]

        species_data.append(PokemonSpecies(
            species_attributes["label"],
            species_id,
            species_attributes["national_dex_number"],
            BaseStats(
                individual_species_data["base_stats"][0],
                individual_species_data["base_stats"][1],
                individual_species_data["base_stats"][2],
                individual_species_data["base_stats"][3],
                individual_species_data["base_stats"][4],
                individual_species_data["base_stats"][5]
            ),
            [individual_species_data["types"][0], individual_species_data["types"][1]],
            [individual_species_data["abilities"][0], individual_species_data["abilities"][1]],
            individual_species_data["catch_rate"],
            species_attributes["tm_hm_compatibility"]
        ))

    species_data = sorted(species_data, key=lambda species: species.id)

init_species_data()
