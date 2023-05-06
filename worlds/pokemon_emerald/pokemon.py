"""
Functions related to pokemon species and moves
"""
import random
from typing import List, Set, Optional

from .data import SpeciesData, data


_damaging_moves = frozenset([
     1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 15, 16,
    17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31, 32,
    33, 34, 35, 36, 37, 38, 40, 41, 42, 44, 48, 49, 51, 52, 53,
    55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 69, 70,
    71, 72, 73, 75, 76, 80, 82, 83, 84, 85, 86, 87, 88, 89, 90,
    91, 93, 94, 98, 99, 101, 117, 118, 119, 121, 122, 123, 124,
    125, 126, 127, 128, 129, 130, 131, 132, 134, 136, 139, 140,
    141, 142, 143, 144, 145, 146, 149, 152, 154, 155, 157, 158,
    161, 162, 163, 167, 168, 172, 175, 177, 179, 180, 181, 183,
    184, 185, 188, 189, 190, 192, 196, 198, 200, 202, 205, 206,
    209, 210, 211, 216, 217, 218, 221, 222, 223, 224, 225, 228,
    229, 231, 232, 233, 237, 238, 239, 242, 244, 245, 246, 247,
    248, 249, 250, 251, 253, 257, 263, 264, 265, 276, 279, 280,
    282, 284, 290, 291, 292, 295, 296, 299, 301, 302, 304, 305,
    306, 307, 308, 309, 310, 311, 314, 315, 317, 318, 322, 324,
    325, 326, 327, 328, 329, 330, 331, 332, 333, 337, 338, 340,
    341, 342, 344, 345, 348, 350, 351, 352, 353, 354
])
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
_legendary_pokemon = frozenset([
    'Mew',
    'Mewtwo',
    'Articuno',
    'Zapdos',
    'Moltres',
    'Lugia',
    'Ho-oh',
    'Raikou',
    'Suicune',
    'Entei',
    'Celebi',
    'Groudon',
    'Kyogre',
    'Rayquaza',
    'Latios',
    'Latias',
    'Registeel',
    'Regirock',
    'Regice',
    'Jirachi',
    'Deoxys'
])


def get_species_by_id(species_id: int) -> Optional[SpeciesData]:
    for species in data.species:
        if species.species_id == species_id:
            return species

    return None


def get_species_by_name(name: str) -> Optional[SpeciesData]:
    for species in data.species:
        if species.label == name:
            return species

    return None


def get_random_species(
        rand: random,
        candidates: List[SpeciesData],
        nearby_bst: Optional[int] = None,
        species_type: Optional[int] = None,
        allow_legendaries: bool = True) -> SpeciesData:
    if nearby_bst is not None:
        def has_nearby_bst(species: SpeciesData):
            return abs(sum(species.base_stats) - nearby_bst) < nearby_bst / 10

        candidates = list(filter(has_nearby_bst, candidates))

    if species_type is not None:
        candidates = [species for species in candidates if species_type in species.types]

    if not allow_legendaries:
        candidates = [species for species in candidates if species.label not in _legendary_pokemon]

    return candidates[rand.randrange(0, len(candidates))]


def get_random_move(rand: random, blacklist: Optional[Set[int]] = None) -> int:
    expanded_blacklist = _move_blacklist | (blacklist if blacklist is not None else set())
    num_moves = data.constants["MOVES_COUNT"]

    move = rand.randrange(1, num_moves)
    while move in expanded_blacklist:
        move = rand.randrange(1, num_moves)

    return move


def get_random_damaging_move(rand: random, blacklist: Optional[Set[int]] = None) -> int:
    expanded_blacklist = _move_blacklist | (blacklist if blacklist is not None else set())

    move_options = list(_damaging_moves)

    move = rand.choice(move_options)
    while move in expanded_blacklist:
        move = rand.choice(move_options)

    return move
