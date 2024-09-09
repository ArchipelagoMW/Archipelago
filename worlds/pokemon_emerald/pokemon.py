"""
Functions related to pokemon species and moves
"""
import functools
from typing import TYPE_CHECKING, Dict, List, Set, Optional, Tuple

from .data import (NUM_REAL_SPECIES, OUT_OF_LOGIC_MAPS, EncounterType, EncounterTableData, LearnsetMove, SpeciesData,
                   MapData, data)
from .options import (Goal, HmCompatibility, LevelUpMoves, RandomizeAbilities, RandomizeLegendaryEncounters,
                      RandomizeMiscPokemon, RandomizeStarters, RandomizeTypes, RandomizeWildPokemon,
                      TmTutorCompatibility)
from .util import bool_array_to_int, get_easter_egg, int_to_bool_array

if TYPE_CHECKING:
    from random import Random
    from . import PokemonEmeraldWorld


_DAMAGING_MOVES = frozenset({
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
    340, 341, 342, 343, 344, 345, 348, 350, 351, 352, 353, 354,
})
"""IDs for moves that safely deal direct damage, for avoiding putting the
player in a situation where they can only use status moves, or are forced
to faint themselves, or something of that nature."""

_MOVE_TYPES = [
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
    12, 11, 14, 12, 16,  5, 13, 11,  8, 14,
]
"""Maps move ids to the type of that move"""

_MOVES_BY_TYPE: Dict[int, List[int]] = {}
"""Categorizes move ids by their type"""
for move, type in enumerate(_MOVE_TYPES):
    _MOVES_BY_TYPE.setdefault(type, []).append(move)

HM_MOVES = frozenset({
    data.constants["MOVE_CUT"],
    data.constants["MOVE_FLY"],
    data.constants["MOVE_SURF"],
    data.constants["MOVE_STRENGTH"],
    data.constants["MOVE_FLASH"],
    data.constants["MOVE_ROCK_SMASH"],
    data.constants["MOVE_WATERFALL"],
    data.constants["MOVE_DIVE"],
})

_MOVE_BLACKLIST = frozenset({
    0,    # MOVE_NONE
    165,  # Struggle
} | HM_MOVES)


@functools.lru_cache(maxsize=386)
def get_species_id_by_label(label: str) -> int:
    return next(species.species_id for species in data.species.values() if species.label == label)


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
    expanded_blacklist = _MOVE_BLACKLIST | (blacklist if blacklist is not None else set())

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
        possible_moves = [move for move in _MOVES_BY_TYPE[type_target[0]] if move not in expanded_blacklist] + \
                         [move for move in _MOVES_BY_TYPE[type_target[1]] if move not in expanded_blacklist]

    if len(possible_moves) == 0:
        return get_random_move(random, None, type_bias, normal_bias, type_target)

    return random.choice(possible_moves)


def get_random_damaging_move(random: "Random", blacklist: Optional[Set[int]] = None) -> int:
    expanded_blacklist = _MOVE_BLACKLIST | (blacklist if blacklist is not None else set())
    move_options = list(_DAMAGING_MOVES)

    move = random.choice(move_options)
    while move in expanded_blacklist:
        move = random.choice(move_options)

    return move


def filter_species_by_nearby_bst(species: List[SpeciesData], target_bst: int) -> List[SpeciesData]:
    # Sort by difference in bst, then chop off the tail of the list that's more than
    # 10% different. If that leaves the list empty, increase threshold to 20%, then 30%, etc.
    species = sorted(species, key=lambda species: abs(sum(species.base_stats) - target_bst))
    cutoff_index = 0
    max_percent_different = 10
    while cutoff_index == 0 and max_percent_different < 10000:
        while cutoff_index < len(species) and abs(sum(species[cutoff_index].base_stats) - target_bst) < target_bst * (max_percent_different / 100):
            cutoff_index += 1
        max_percent_different += 10

    return species[:cutoff_index + 1]


def randomize_types(world: "PokemonEmeraldWorld") -> None:
    if world.options.types == RandomizeTypes.option_shuffle:
        type_map = list(range(18))
        world.random.shuffle(type_map)

        # We never want to map to the ??? type, so swap whatever index maps to ??? with ???
        # which forces ??? to always map to itself. There are no pokemon which have the ??? type
        mystery_type_index = type_map.index(9)
        type_map[mystery_type_index], type_map[9] = type_map[9], type_map[mystery_type_index]

        for species in world.modified_species.values():
            species.types = (type_map[species.types[0]], type_map[species.types[1]])
    elif world.options.types == RandomizeTypes.option_completely_random:
        for species in world.modified_species.values():
            new_type_1 = get_random_type(world.random)
            new_type_2 = new_type_1
            if species.types[0] != species.types[1]:
                while new_type_1 == new_type_2:
                    new_type_2 = get_random_type(world.random)

            species.types = (new_type_1, new_type_2)
    elif world.options.types == RandomizeTypes.option_follow_evolutions:
        already_modified: Set[int] = set()

        # Similar to follow evolutions for abilities, but only needs to loop through once.
        # For every pokemon without a pre-evolution, generates a random mapping from old types to new types
        # and then walks through the evolution tree applying that map. This means that evolutions that share
        # types will have those types mapped to the same new types, and evolutions with new or diverging types
        # will still have new or diverging types.
        # Consider:
        # - Charmeleon (Fire/Fire) -> Charizard (Fire/Flying)
        # - Onyx (Rock/Ground) -> Steelix (Steel/Ground)
        # - Nincada (Bug/Ground) -> Ninjask (Bug/Flying) && Shedinja (Bug/Ghost)
        # - Azurill (Normal/Normal) -> Marill (Water/Water)
        for species in world.modified_species.values():
            if species.species_id in already_modified:
                continue
            if species.pre_evolution is not None and species.pre_evolution not in already_modified:
                continue

            type_map = list(range(18))
            world.random.shuffle(type_map)

            # We never want to map to the ??? type, so swap whatever index maps to ??? with ???
            # which forces ??? to always map to itself. There are no pokemon which have the ??? type
            mystery_type_index = type_map.index(9)
            type_map[mystery_type_index], type_map[9] = type_map[9], type_map[mystery_type_index]

            evolutions = [species]
            while len(evolutions) > 0:
                evolution = evolutions.pop()
                evolution.types = (type_map[evolution.types[0]], type_map[evolution.types[1]])
                already_modified.add(evolution.species_id)
                evolutions += [world.modified_species[evo.species_id] for evo in evolution.evolutions]


_encounter_subcategory_ranges: Dict[EncounterType, Dict[range, Optional[str]]] = {
    EncounterType.LAND: {range(0, 12): None},
    EncounterType.WATER: {range(0, 5): None},
    EncounterType.FISHING: {range(0, 2): "OLD_ROD", range(2, 5): "GOOD_ROD", range(5, 10): "SUPER_ROD"},
}


def _rename_wild_events(world: "PokemonEmeraldWorld", map_data: MapData, new_slots: List[int], encounter_type: EncounterType):
    """
    Renames the events that correspond to wild encounters to reflect the new species there after randomization
    """
    for i, new_species_id in enumerate(new_slots):
        # Get the subcategory for rods
        subcategory_range, subcategory_name = next(
            (r, sc)
            for r, sc in _encounter_subcategory_ranges[encounter_type].items()
            if i in r
        )
        subcategory_species = []
        for k in subcategory_range:
            if new_slots[k] not in subcategory_species:
                subcategory_species.append(new_slots[k])

        # Create the name of the location that corresponds to this encounter slot
        # Fishing locations include the rod name
        subcategory_str = "" if subcategory_name is None else "_" + subcategory_name
        encounter_location_index = subcategory_species.index(new_species_id) + 1
        encounter_location_name = f"{map_data.name}_{encounter_type.value}_ENCOUNTERS{subcategory_str}_{encounter_location_index}"
        try:
            # Get the corresponding location and change the event name to reflect the new species
            slot_location = world.multiworld.get_location(encounter_location_name, world.player)
            slot_location.item.name = f"CATCH_{data.species[new_species_id].name}"
        except KeyError:
            pass  # Map probably isn't included; should be careful here about bad encounter location names


def randomize_wild_encounters(world: "PokemonEmeraldWorld") -> None:
    if world.options.wild_pokemon == RandomizeWildPokemon.option_vanilla:
        return

    from collections import defaultdict

    should_match_bst = world.options.wild_pokemon in {
        RandomizeWildPokemon.option_match_base_stats,
        RandomizeWildPokemon.option_match_base_stats_and_type,
    }
    should_match_type = world.options.wild_pokemon in {
        RandomizeWildPokemon.option_match_type,
        RandomizeWildPokemon.option_match_base_stats_and_type,
    }

    already_placed = set()
    num_placeable_species = NUM_REAL_SPECIES - len(world.blacklisted_wilds)

    priority_species = [data.constants["SPECIES_WAILORD"], data.constants["SPECIES_RELICANTH"]]

    # Loop over map data to modify their encounter slots
    map_names = list(world.modified_maps.keys())
    world.random.shuffle(map_names)
    for map_name in map_names:
        placed_priority_species = False
        map_data = world.modified_maps[map_name]

        new_encounters: Dict[EncounterType, EncounterTableData] = {}

        for encounter_type, table in map_data.encounters.items():
            # Create a map from the original species to new species
            # instead of just randomizing every slot.
            # Force area 1-to-1 mapping, in other words.
            species_old_to_new_map: Dict[int, int] = {}
            for species_id in table.slots:
                if species_id not in species_old_to_new_map:
                    if not placed_priority_species and len(priority_species) > 0 \
                            and encounter_type != EncounterType.ROCK_SMASH and map_name not in OUT_OF_LOGIC_MAPS:
                        new_species_id = priority_species.pop()
                        placed_priority_species = True
                    else:
                        original_species = data.species[species_id]

                        # Construct progressive tiers of blacklists that can be peeled back if they
                        # collectively cover too much of the pokedex. A lower index in `blacklists`
                        # indicates a more important set of species to avoid. Entries at `0` will
                        # always be blacklisted.
                        blacklists: Dict[int, List[Set[int]]] = defaultdict(list)

                        # Blacklist pokemon already on this table
                        blacklists[0].append(set(species_old_to_new_map.values()))

                        # If doing legendary hunt, blacklist Latios from wild encounters so
                        # it can be tracked as the roamer. Otherwise it may be impossible
                        # to tell whether a highlighted route is the roamer or a wild
                        # encounter.
                        if world.options.goal == Goal.option_legendary_hunt:
                            blacklists[0].append({data.constants["SPECIES_LATIOS"]})

                        # If dexsanity/catch 'em all mode, blacklist already placed species
                        # until every species has been placed once
                        if world.options.dexsanity and len(already_placed) < num_placeable_species:
                            blacklists[1].append(already_placed)

                        # Blacklist from player options
                        blacklists[2].append(world.blacklisted_wilds)

                        # Type matching blacklist
                        if should_match_type:
                            blacklists[3].append({
                                species.species_id
                                for species in world.modified_species.values()
                                if not bool(set(species.types) & set(original_species.types))
                            })

                        merged_blacklist: Set[int] = set()
                        for max_priority in reversed(sorted(blacklists.keys())):
                            merged_blacklist = set()
                            for priority in blacklists.keys():
                                if priority <= max_priority:
                                    for blacklist in blacklists[priority]:
                                        merged_blacklist |= blacklist

                            if len(merged_blacklist) < NUM_REAL_SPECIES:
                                break
                        else:
                            raise RuntimeError("This should never happen")

                        candidates = [
                            species
                            for species in world.modified_species.values()
                            if species.species_id not in merged_blacklist
                        ]

                        if should_match_bst:
                            candidates = filter_species_by_nearby_bst(candidates, sum(original_species.base_stats))

                        new_species_id = world.random.choice(candidates).species_id

                    species_old_to_new_map[species_id] = new_species_id

                    if world.options.dexsanity and encounter_type != EncounterType.ROCK_SMASH \
                            and map_name not in OUT_OF_LOGIC_MAPS:
                        already_placed.add(new_species_id)

            # Actually create the new list of slots and encounter table
            new_slots: List[int] = []
            for species_id in table.slots:
                new_slots.append(species_old_to_new_map[species_id])

            new_encounters[encounter_type] = EncounterTableData(new_slots, table.address)

            # Rock smash encounters not used in logic, so they have no events
            if encounter_type != EncounterType.ROCK_SMASH:
                _rename_wild_events(world, map_data, new_slots, encounter_type)

        map_data.encounters = new_encounters


def randomize_abilities(world: "PokemonEmeraldWorld") -> None:
    if world.options.abilities == RandomizeAbilities.option_vanilla:
        return

    # Creating list of potential abilities
    ability_label_to_value = {ability.label.lower(): ability.ability_id for ability in data.abilities}

    ability_blacklist_labels = {"cacophony"}  # Cacophony is defined and has a description, but no effect
    option_ability_blacklist = world.options.ability_blacklist.value
    if option_ability_blacklist is not None:
        ability_blacklist_labels |= {ability_label.lower() for ability_label in option_ability_blacklist}

    ability_blacklist = {ability_label_to_value[label] for label in ability_blacklist_labels}
    ability_whitelist = [a.ability_id for a in data.abilities if a.ability_id not in ability_blacklist]

    if world.options.abilities == RandomizeAbilities.option_follow_evolutions:
        already_modified: Set[int] = set()

        # Loops through species and only tries to modify abilities if the pokemon has no pre-evolution
        # or if the pre-evolution has already been modified. Then tries to modify all species that evolve
        # from this one which have the same abilities.
        #
        # The outer while loop only runs three times for vanilla ordering: Once for a first pass, once for
        # Hitmonlee/Hitmonchan, and once to verify that there's nothing left to do.
        while True:
            had_clean_pass = True
            for species in world.modified_species.values():
                if species.species_id in already_modified:
                    continue
                if species.pre_evolution is not None and species.pre_evolution not in already_modified:
                    continue

                had_clean_pass = False

                old_abilities = species.abilities
                # 0 is the value for "no ability"; species with only 1 ability have the other set to 0
                new_abilities = (
                    0 if old_abilities[0] == 0 else world.random.choice(ability_whitelist),
                    0 if old_abilities[1] == 0 else world.random.choice(ability_whitelist)
                )

                # Recursively modify the abilities of anything that evolves from this pokemon
                # until the evolution doesn't have a matching set of abilities
                evolutions = [species]
                while len(evolutions) > 0:
                    evolution = evolutions.pop()
                    if evolution.abilities == old_abilities:
                        evolution.abilities = new_abilities
                        already_modified.add(evolution.species_id)
                        evolutions += [
                            world.modified_species[evolution.species_id]
                            for evolution in evolution.evolutions
                            if evolution.species_id not in already_modified
                        ]

            if had_clean_pass:
                break
    else:  # Not following evolutions
        for species in world.modified_species.values():
            old_abilities = species.abilities
            # 0 is the value for "no ability"; species with only 1 ability have the other set to 0
            new_abilities = (
                0 if old_abilities[0] == 0 else world.random.choice(ability_whitelist),
                0 if old_abilities[1] == 0 else world.random.choice(ability_whitelist)
            )

            species.abilities = new_abilities


def randomize_learnsets(world: "PokemonEmeraldWorld") -> None:
    if world.options.level_up_moves == LevelUpMoves.option_vanilla:
        return

    type_bias = world.options.move_match_type_bias.value
    normal_bias = world.options.move_normal_type_bias.value

    for species in world.modified_species.values():
        old_learnset = species.learnset
        new_learnset: List[LearnsetMove] = []

        # All species have 4 moves at level 0. Up to 3 of them are blank spaces reserved for the
        # start with four moves option. This either replaces those moves or leaves it blank
        # and moves the cursor.
        cursor = 0
        while old_learnset[cursor].move_id == 0:
            if world.options.level_up_moves == LevelUpMoves.option_start_with_four_moves:
                new_move = get_random_move(world.random,
                                           {move.move_id for move in new_learnset} | world.blacklisted_moves,
                                           type_bias, normal_bias, species.types)
            else:
                new_move = 0
            new_learnset.append(old_learnset[cursor]._replace(move_id=new_move))
            cursor += 1

        # All moves from here onward are actual moves.
        while cursor < len(old_learnset):
            # Guarantees the starter has a good damaging move; i will always be <=3 when entering this loop
            if cursor == 3:
                new_move = get_random_damaging_move(world.random, {move.move_id for move in new_learnset})
            else:
                new_move = get_random_move(world.random,
                                           {move.move_id for move in new_learnset} | world.blacklisted_moves,
                                           type_bias, normal_bias, species.types)
            new_learnset.append(old_learnset[cursor]._replace(move_id=new_move))
            cursor += 1

        species.learnset = new_learnset

        
def randomize_starters(world: "PokemonEmeraldWorld") -> None:
    if world.options.starters == RandomizeStarters.option_vanilla:
        return

    should_match_bst = world.options.starters in {
        RandomizeStarters.option_match_base_stats,
        RandomizeStarters.option_match_base_stats_and_type,
    }
    should_match_type = world.options.starters in {
        RandomizeStarters.option_match_type,
        RandomizeStarters.option_match_base_stats_and_type,
    }

    new_starters: List[SpeciesData] = []

    easter_egg_type, easter_egg_value = get_easter_egg(world.options.easter_egg.value)
    if easter_egg_type == 1:
        new_starters = [
            world.modified_species[easter_egg_value],
            world.modified_species[easter_egg_value],
            world.modified_species[easter_egg_value]
        ]
    else:
        for i, starter_id in enumerate(data.starters):
            original_starter = data.species[starter_id]
            type_blacklist = {
                species.species_id
                for species in world.modified_species.values()
                if not bool(set(species.types) & set(original_starter.types))
            } if should_match_type else set()

            merged_blacklist = set(s.species_id for s in new_starters) | world.blacklisted_starters | type_blacklist
            if len(merged_blacklist) == NUM_REAL_SPECIES:
                merged_blacklist = set(s.species_id for s in new_starters) | world.blacklisted_starters
            if len(merged_blacklist) == NUM_REAL_SPECIES:
                merged_blacklist = set(s.species_id for s in new_starters)

            candidates = [
                species
                for species in world.modified_species.values()
                if species.species_id not in merged_blacklist
            ]

            if should_match_bst:
                candidates = filter_species_by_nearby_bst(candidates, sum(original_starter.base_stats))

            new_starters.append(world.random.choice(candidates))

    world.modified_starters = (
        new_starters[0].species_id,
        new_starters[1].species_id,
        new_starters[2].species_id
    )

    # Putting the unchosen starter onto the rival's team
    # (trainer name, index of starter in team, whether the starter is evolved)
    rival_teams: List[List[Tuple[str, int, bool]]] = [
        [
            ("TRAINER_BRENDAN_ROUTE_103_TREECKO", 0, False),
            ("TRAINER_BRENDAN_RUSTBORO_TREECKO",  1, False),
            ("TRAINER_BRENDAN_ROUTE_110_TREECKO", 2, True ),
            ("TRAINER_BRENDAN_ROUTE_119_TREECKO", 2, True ),
            ("TRAINER_BRENDAN_LILYCOVE_TREECKO",  3, True ),
            ("TRAINER_MAY_ROUTE_103_TREECKO",     0, False),
            ("TRAINER_MAY_RUSTBORO_TREECKO",      1, False),
            ("TRAINER_MAY_ROUTE_110_TREECKO",     2, True ),
            ("TRAINER_MAY_ROUTE_119_TREECKO",     2, True ),
            ("TRAINER_MAY_LILYCOVE_TREECKO",      3, True ),
        ],
        [
            ("TRAINER_BRENDAN_ROUTE_103_TORCHIC", 0, False),
            ("TRAINER_BRENDAN_RUSTBORO_TORCHIC",  1, False),
            ("TRAINER_BRENDAN_ROUTE_110_TORCHIC", 2, True ),
            ("TRAINER_BRENDAN_ROUTE_119_TORCHIC", 2, True ),
            ("TRAINER_BRENDAN_LILYCOVE_TORCHIC",  3, True ),
            ("TRAINER_MAY_ROUTE_103_TORCHIC",     0, False),
            ("TRAINER_MAY_RUSTBORO_TORCHIC",      1, False),
            ("TRAINER_MAY_ROUTE_110_TORCHIC",     2, True ),
            ("TRAINER_MAY_ROUTE_119_TORCHIC",     2, True ),
            ("TRAINER_MAY_LILYCOVE_TORCHIC",      3, True ),
        ],
        [
            ("TRAINER_BRENDAN_ROUTE_103_MUDKIP", 0, False),
            ("TRAINER_BRENDAN_RUSTBORO_MUDKIP",  1, False),
            ("TRAINER_BRENDAN_ROUTE_110_MUDKIP", 2, True ),
            ("TRAINER_BRENDAN_ROUTE_119_MUDKIP", 2, True ),
            ("TRAINER_BRENDAN_LILYCOVE_MUDKIP",  3, True ),
            ("TRAINER_MAY_ROUTE_103_MUDKIP",     0, False),
            ("TRAINER_MAY_RUSTBORO_MUDKIP",      1, False),
            ("TRAINER_MAY_ROUTE_110_MUDKIP",     2, True ),
            ("TRAINER_MAY_ROUTE_119_MUDKIP",     2, True ),
            ("TRAINER_MAY_LILYCOVE_MUDKIP",      3, True ),
        ],
    ]

    for i, starter in enumerate([new_starters[1], new_starters[2], new_starters[0]]):
        potential_evolutions = [evolution.species_id for evolution in starter.evolutions]
        picked_evolution = starter.species_id
        if len(potential_evolutions) > 0:
            picked_evolution = world.random.choice(potential_evolutions)

        for trainer_name, starter_position, is_evolved in rival_teams[i]:
            new_species_id = picked_evolution if is_evolved else starter.species_id
            trainer_data = world.modified_trainers[data.constants[trainer_name]]
            trainer_data.party.pokemon[starter_position] = \
                trainer_data.party.pokemon[starter_position]._replace(species_id=new_species_id)


def randomize_legendary_encounters(world: "PokemonEmeraldWorld") -> None:
    if world.options.legendary_encounters == RandomizeLegendaryEncounters.option_vanilla:
        return
    elif world.options.legendary_encounters == RandomizeLegendaryEncounters.option_shuffle:
        # Just take the existing species and shuffle them
        shuffled_species = [encounter.species_id for encounter in data.legendary_encounters]
        world.random.shuffle(shuffled_species)

        for i, encounter in enumerate(data.legendary_encounters):
            world.modified_legendary_encounters.append(encounter._replace(species_id=shuffled_species[i]))
    else:
        should_match_bst = world.options.legendary_encounters in {
            RandomizeLegendaryEncounters.option_match_base_stats,
            RandomizeLegendaryEncounters.option_match_base_stats_and_type
        }
        should_match_type = world.options.legendary_encounters in {
            RandomizeLegendaryEncounters.option_match_type,
            RandomizeLegendaryEncounters.option_match_base_stats_and_type
        }

        for encounter in data.legendary_encounters:
            original_species = world.modified_species[encounter.species_id]

            candidates = list(world.modified_species.values())
            if should_match_type:
                candidates = [
                    species
                    for species in candidates
                    if bool(set(species.types) & set(original_species.types))
                ]
            if should_match_bst:
                candidates = filter_species_by_nearby_bst(candidates, sum(original_species.base_stats))

            world.modified_legendary_encounters.append(encounter._replace(
                species_id=world.random.choice(candidates).species_id
            ))


def randomize_misc_pokemon(world: "PokemonEmeraldWorld") -> None:
    if world.options.misc_pokemon == RandomizeMiscPokemon.option_vanilla:
        return
    elif world.options.misc_pokemon == RandomizeMiscPokemon.option_shuffle:
        # Just take the existing species and shuffle them
        shuffled_species = [encounter.species_id for encounter in data.misc_pokemon]
        world.random.shuffle(shuffled_species)

        world.modified_misc_pokemon = []
        for i, encounter in enumerate(data.misc_pokemon):
            world.modified_misc_pokemon.append(encounter._replace(species_id=shuffled_species[i]))
    else:
        should_match_bst = world.options.misc_pokemon in {
            RandomizeMiscPokemon.option_match_base_stats,
            RandomizeMiscPokemon.option_match_base_stats_and_type,
        }
        should_match_type = world.options.misc_pokemon in {
            RandomizeMiscPokemon.option_match_type,
            RandomizeMiscPokemon.option_match_base_stats_and_type,
        }

        for encounter in data.misc_pokemon:
            original_species = world.modified_species[encounter.species_id]

            candidates = list(world.modified_species.values())
            if should_match_type:
                candidates = [
                    species
                    for species in candidates
                    if bool(set(species.types) & set(original_species.types))
                ]
            if should_match_bst:
                candidates = filter_species_by_nearby_bst(candidates, sum(original_species.base_stats))
            
            player_filtered_candidates = [
                species
                for species in candidates
                if species.species_id not in world.blacklisted_wilds
            ]
            if len(player_filtered_candidates) > 0:
                candidates = player_filtered_candidates

            world.modified_misc_pokemon.append(encounter._replace(
                species_id=world.random.choice(candidates).species_id
            ))


def randomize_tm_hm_compatibility(world: "PokemonEmeraldWorld") -> None:
    for species in world.modified_species.values():
        # TM and HM compatibility is stored as a 64-bit bitfield
        combatibility_array = int_to_bool_array(species.tm_hm_compatibility)

        # TMs
        if world.options.tm_tutor_compatibility != TmTutorCompatibility.special_range_names["vanilla"]:
            for i in range(0, 50):
                combatibility_array[i] = world.random.random() < world.options.tm_tutor_compatibility / 100

        # HMs
        if world.options.hm_compatibility != HmCompatibility.special_range_names["vanilla"]:
            for i in range(50, 58):
                combatibility_array[i] = world.random.random() < world.options.hm_compatibility / 100

        species.tm_hm_compatibility = bool_array_to_int(combatibility_array)
