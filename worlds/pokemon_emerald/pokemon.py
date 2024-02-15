"""
Functions related to pokemon species and moves
"""
import time
from typing import TYPE_CHECKING, Dict, List, Set, Optional, Tuple

from .data import SpeciesData, data

if TYPE_CHECKING:
    from random import Random


_damaging_moves = frozenset({
      1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  13,
     16,  17,  20,  21,  22,  23,  24,  25,  26,  27,  29,  30,
     31,  33,  34,  35,  36,  37,  38,  40,  41,  42,  44,  51,
     52,  53,  55,  56,  58,  59,  60,  61,  62,  63,  64,  65,
     66,  67,  69,  71,  72,  75,  76,  80,  82,  83,  84,  85,
     87,  88,  89,  91,  93,  94,  98,  99, 101, 121, 122, 123,
    124, 125, 126, 128, 129, 130, 131, 132, 136, 140, 141, 143,
    145, 146, 149, 152, 154, 155, 157, 158, 161, 162, 163, 167,
    168, 172, 175, 177, 179, 181, 183, 185, 188, 189, 190, 192,
    196, 198, 200, 202, 205, 209, 210, 211, 216, 217, 218, 221,
    222, 223, 224, 225, 228, 229, 231, 232, 233, 237, 238, 239,
    242, 245, 246, 247, 248, 250, 251, 253, 257, 263, 265, 267,
    276, 279, 280, 282, 284, 290, 292, 295, 296, 299, 301, 302,
    304, 305, 306, 307, 308, 309, 310, 311, 314, 315, 317, 318,
    323, 324, 325, 326, 327, 328, 330, 331, 332, 333, 337, 338,
    340, 341, 342, 343, 344, 345, 348, 350, 351, 352, 353, 354
})

_move_types = [
     0,  0,  1,  0,  0,  0,  0, 10, 15, 13,  0,  0,  0,  0,  0,
     0,  2,  2,  0,  2,  0,  0, 12,  0,  1,  0,  1,  1,  4,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  3,  6,  6,  0, 17,
     0,  0,  0,  0,  0,  0,  3, 10, 10, 15, 11, 11, 11, 15, 15,
    14, 11, 15,  0,  2,  2,  1,  1,  1,  1,  0, 12, 12, 12,  0,
    12, 12,  3, 12, 12, 12,  6, 16, 10, 13, 13, 13, 13,  5,  4,
     4,  4,  3, 14, 14, 14, 14, 14,  0,  0, 14,  7,  0,  0,  0,
     0,  0,  0,  0,  7, 11,  0, 14, 14, 15, 14,  0,  0,  0,  2,
     0,  0,  7,  3,  3,  4, 10, 11, 11,  0,  0,  0,  0, 14, 14,
     0,  1,  0, 14,  3,  0,  6,  0,  2,  0, 11,  0, 12,  0, 14,
     0,  3, 11,  0,  0,  4, 14,  5,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  1, 17,  6,  0,  7, 10,  0,  9,  0,  0,  2, 12,  1,
     7, 15,  0,  1,  0, 17,  0,  0,  3,  4, 11,  4, 13,  0,  7,
     0, 15,  1,  4,  0, 16,  5, 12,  0,  0,  5,  0,  0,  0, 13,
     6,  8,  0,  0,  0,  0,  0,  0,  0,  0,  0, 10,  4,  1,  6,
    16,  0,  0, 17,  0,  0,  8,  8,  1,  0, 12,  0,  0,  1, 16,
    11, 10, 17, 14,  0,  0,  5,  7, 14,  1, 11, 17,  0,  0,  0,
     0,  0, 10, 15, 17, 17, 10, 17,  0,  1,  0,  0,  0, 13, 17,
     0, 14, 14,  0,  0, 12,  1, 14,  0,  1,  1,  0, 17,  0, 10,
    14, 14,  0,  7, 17,  0, 11,  1,  0,  6, 14, 14,  2,  0, 10,
     4, 15, 12,  0,  0,  3,  0, 10, 11,  8,  7,  0, 12, 17,  2,
    10,  0,  5,  6,  8, 12,  0, 14, 11,  6,  7, 14,  1,  4, 15,
    11, 12,  2, 15,  8,  0,  0, 16, 12,  1,  2,  4,  3,  0, 13,
    12, 11, 14, 12, 16,  5, 13, 11,  8, 14
]

_moves_by_type: Dict[int, List[int]] = {}
for move, type in enumerate(_move_types):
    _moves_by_type.setdefault(type, []).append(move)

_move_blacklist = frozenset({
    0,    # MOVE_NONE
    165,  # Struggle
    15,   # Cut
    148,  # Flash
    249,  # Rock Smash
    70,   # Strength
    57,   # Surf
    19,   # Fly
    291,  # Dive
    127   # Waterfall
})

_legendary_pokemon = frozenset({
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
})


def get_random_species(
        random: "Random",
        candidates: List[Optional[SpeciesData]],
        nearby_bst: Optional[int] = None,
        species_type: Optional[int] = None,
        allow_legendaries: bool = True) -> SpeciesData:
    candidates: List[SpeciesData] = [species for species in candidates if species is not None]

    if species_type is not None:
        candidates = [species for species in candidates if species_type in species.types]

    if not allow_legendaries:
        candidates = [species for species in candidates if species.label not in _legendary_pokemon]

    if nearby_bst is not None:
        def has_nearby_bst(species: SpeciesData, max_percent_different: int) -> bool:
            return abs(sum(species.base_stats) - nearby_bst) < nearby_bst * (max_percent_different / 100)

        max_percent_different = 10
        bst_filtered_candidates = [species for species in candidates if has_nearby_bst(species, max_percent_different)]
        while len(bst_filtered_candidates) == 0:
            max_percent_different += 10
            bst_filtered_candidates = [
                species
                for species in candidates
                if has_nearby_bst(species, max_percent_different)
            ]

        candidates = bst_filtered_candidates

    return random.choice(candidates)


def get_random_type(random: "Random") -> int:
    picked_type = random.randrange(0, 18)
    while picked_type == 9:  # Don't pick the ??? type
        picked_type = random.randrange(0, 18)

    return picked_type


def get_random_move(
        random: "Random",
        blacklist: Optional[Set[int]] = None,
        type_bias: int = 0,
        normal_bias: int = 0,
        type_target: Optional[Tuple[int, int]] = None) -> int:
    expanded_blacklist = _move_blacklist | (blacklist if blacklist is not None else set())

    bias = random.random() * 100
    if bias < type_bias:
        pass  # Keep type_target unchanged
    elif bias < type_bias + ((100 - type_bias) * (normal_bias / 100)):
        type_target = (0, 0)
    else:
        type_target = None

    chosen_move = None

    # The blacklist is relatively small, so if we don't need to restrict
    # ourselves to any particular types, it's usually much faster to pick
    # a random number and hope it works. Limit this to 5 tries in case the
    # blacklist is actually significant enough to make this unlikely to work.
    if type_target is None:
        remaining_attempts = 5
        while remaining_attempts > 0:
            remaining_attempts -= 1
            chosen_move = random.randrange(0, data.constants["MOVES_COUNT"])
            if chosen_move not in expanded_blacklist:
                return chosen_move
        else:
            chosen_move = None

    # We're either matching types or failed to pick a move above
    if type_target is None:
        possible_moves = [i for i in range(data.constants["MOVES_COUNT"]) if i not in expanded_blacklist]
    else:
        possible_moves = [move for move in _moves_by_type[type_target[0]] if move not in expanded_blacklist] + \
                            [move for move in _moves_by_type[type_target[1]] if move not in expanded_blacklist]

    if len(possible_moves) == 0:
        return get_random_move(random, None, type_bias, normal_bias, type_target)

    return random.choice(possible_moves)


def get_random_damaging_move(random: "Random", blacklist: Optional[Set[int]] = None) -> int:
    expanded_blacklist = _move_blacklist | (blacklist if blacklist is not None else set())

    move_options = list(_damaging_moves)

    move = random.choice(move_options)
    while move in expanded_blacklist:
        move = random.choice(move_options)

    return move
