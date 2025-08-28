from copy import deepcopy
from random import Random
from typing import Dict, List, Optional

from worlds.tits_the_3rd.crafts.models import Character
from worlds.tits_the_3rd.tables.craft_list import (
    base_craft_id_to_obj,
    default_characters,
    fixed_normal_craft_table,
    fixed_scraft_table,
    upgradable_normal_craft_table,
    upgradable_scraft_table,
)
from worlds.tits_the_3rd.options import TitsThe3rdOptions, CraftPlacement

def _get_character_to_craft_get_order() -> dict[str, List[Dict[int, int]]]:
    """
    Return a dictionary of:
    {
      character_name (str): [
        craft_id (int)
      ]
    }

    The order of the craft_id is the default order based on level acquired.
    This will return the character's default crafts.
    """
    character_to_craft_get_order = {}
    for character in default_characters:
        craft_id_to_level_acquired = {}
        crafts = character.crafts

        # Get a mapping of craft_id to level acquired
        for craft in crafts:
            craft_id_to_level_acquired[craft.base_craft_id] = craft.base_craft_level_acquired
            if craft.upgraded_craft_id is not None:
                craft_id_to_level_acquired[craft.upgraded_craft_id] = craft.upgraded_craft_level_acquired

        # Sort crafts by level acquired and extract just the craft IDs
        sorted_craft_ids = sorted(craft_id_to_level_acquired.items(), key=lambda x: x[1])

        character_to_craft_get_order[character.name.lower()] = [craft_id for craft_id, _ in sorted_craft_ids]
    return character_to_craft_get_order

def _shuffle_craft_get_order(character_to_craft_get_order: Dict[str, List[int]], rng: Random) -> Dict[str, List[int]]:
    """
    Shuffle the craft get order for each character.
    Upgraded crafts are always after the base craft.
    """
    for character_name, craft_ids in character_to_craft_get_order.items():
        rng.shuffle(craft_ids)
        for idx, craft_id in enumerate(craft_ids):
            if craft_id in base_craft_id_to_obj and base_craft_id_to_obj[craft_id].upgraded_craft_id is not None:
                # This craft has an upgrade. Assert that the upgrade is after the base craft.
                upgraded_craft_id = base_craft_id_to_obj[craft_id].upgraded_craft_id
                upgraded_craft_idx = craft_ids.index(upgraded_craft_id)
                if upgraded_craft_idx < idx:
                    craft_ids[idx], craft_ids[upgraded_craft_idx] = craft_ids[upgraded_craft_idx], craft_ids[idx]
        character_to_craft_get_order[character_name] = craft_ids
    return character_to_craft_get_order


def _progress_size_constraints(characters: List[Character], rng: Random):
    """
    If the character animation size is too large, swap crafts until the size for that character is valid.
    Crafts can only be swapped amongst those in the same craft category.

    Tested with 100000 runs without failure.
    """
    for character in characters:
        while character.remaining_buffer_size_bytes < 0:
            character_to_swap_with = rng.choice([c for c in characters if c != character])
            craft_1 = rng.choice(character.swappable_crafts)
            craft_category = craft_1.category
            character_2_category_craft_list = character_to_swap_with.get_craft_list_by_category(craft_category)
            if len(character_2_category_craft_list) == 0:
                continue
            craft_2 = rng.choice(character_2_category_craft_list)
            # Only swap if we end up in a better state.
            if (
                (abs(character.remaining_buffer_size_bytes) + abs(character_to_swap_with.remaining_buffer_size_bytes)) <
                (
                    abs(character.remaining_buffer_size_bytes - craft_1.animation_size_bytes + craft_2.animation_size_bytes) +
                    abs(character_to_swap_with.remaining_buffer_size_bytes - craft_2.animation_size_bytes + craft_1.animation_size_bytes)
                )
            ):
                character.get_craft_list_by_category(craft_category).remove(craft_1)
                character_to_swap_with.get_craft_list_by_category(craft_category).remove(craft_2)
                character.get_craft_list_by_category(craft_category).append(craft_2)
                character_to_swap_with.get_craft_list_by_category(craft_category).append(craft_1)


def _is_in_invalid_size_state(characters: List[Character]) -> bool:
    """
    Returns True if any character is in an invalid size state.
    """
    for character in characters:
        if character.remaining_buffer_size_bytes < 0:
            return True
    return False


def _fix_size_constraints(characters: List[Character], rng: Random):
    """
    Fix the size constraints for each character.
    """
    while _is_in_invalid_size_state(characters):
        _progress_size_constraints(characters, rng)


def _shuffle_crafts(characters: List[Character], rng: Random) -> List[Character]:
    """
    Shuffle the crafts for each character.
    Crafts can only be shuffled amongst those in the same craft category.

    Returns:
        List[Character]: The characters with their shuffled crafts.
    """
    fixed_normal_craft_table_copy = deepcopy(fixed_normal_craft_table)
    fixed_scraft_table_copy = deepcopy(fixed_scraft_table)
    upgradable_normal_craft_table_copy = deepcopy(upgradable_normal_craft_table)
    upgradable_scraft_table_copy = deepcopy(upgradable_scraft_table)

    rng.shuffle(fixed_normal_craft_table_copy)
    rng.shuffle(fixed_scraft_table_copy)
    rng.shuffle(upgradable_normal_craft_table_copy)
    rng.shuffle(upgradable_scraft_table_copy)

    for character in characters:
        character.fixed_normal_crafts = [fixed_normal_craft_table_copy.pop(0) for _ in range(len(character.fixed_normal_crafts))]
        character.fixed_scrafts = [fixed_scraft_table_copy.pop(0) for _ in range(len(character.fixed_scrafts))]
        character.upgradable_normal_crafts = [upgradable_normal_craft_table_copy.pop(0) for _ in range(len(character.upgradable_normal_crafts))]
        character.upgradable_scrafts = [upgradable_scraft_table_copy.pop(0) for _ in range(len(character.upgradable_scrafts))]

    _fix_size_constraints(characters, rng)
    return characters

def _get_old_craft_id_to_new_craft_id(characters: List[Character]) -> Dict[int, int]:
    """
    Get a mapping of old craft IDs to new craft IDs.

    Returns:
        Dict[int, int]: A mapping of old craft IDs to new craft IDs.
    """
    old_craft_id_to_new_craft_id = {}
    for idx, character in enumerate(characters):
        default_character = default_characters[idx]
        for idx, old_craft in enumerate(default_character.fixed_normal_crafts):
            old_craft_id_to_new_craft_id[old_craft.base_craft_id] = character.fixed_normal_crafts[idx].base_craft_id
        for idx, old_craft in enumerate(default_character.fixed_scrafts):
            old_craft_id_to_new_craft_id[old_craft.base_craft_id] = character.fixed_scrafts[idx].base_craft_id
        for idx, old_craft in enumerate(default_character.upgradable_normal_crafts):
            old_craft_id_to_new_craft_id[old_craft.base_craft_id] = character.upgradable_normal_crafts[idx].base_craft_id
        for idx, old_craft in enumerate(default_character.upgradable_scrafts):
            old_craft_id_to_new_craft_id[old_craft.base_craft_id] = character.upgradable_scrafts[idx].base_craft_id
    return old_craft_id_to_new_craft_id

def shuffle_crafts_main(options: TitsThe3rdOptions, rng: Random) -> tuple[Optional[Dict[str, List[int]]], Optional[Dict[int, int]]]:
    """
    Note that even if characters have their default crafts, if locations are shuffled, the craft get order will be randomized.
    (e.g. A character may get a late game craft for their first craft and vice versa).
    Note that progressive crafts are always given in order (e.g. Lanzenreiter will always be before Lanzenreiter 2)

    This returns a tuple of:
    - character_to_craft_get_order: A dictionary of character name to a list of craft IDs in the order they will be given.
    - old_craft_id_to_new_craft_id: The craft shuffle mapping.
    """
    if options.craft_placement == CraftPlacement.option_default and not options.craft_shuffle:
        return None, None
    characters = deepcopy(default_characters)

    old_craft_id_to_new_craft_id = None
    if options.craft_shuffle:
        # Get a mapping of shuffled crafts.
        characters = _shuffle_crafts(characters, rng)
        old_craft_id_to_new_craft_id = _get_old_craft_id_to_new_craft_id(characters)

    # Note the character_to_craft_get_order is the default craft ids.
    # This is because we tell the game to give the default craft ID, but it has the data of the new craft ID.
    character_to_craft_get_order = _get_character_to_craft_get_order()
    character_to_craft_get_order = _shuffle_craft_get_order(character_to_craft_get_order, rng)

    return character_to_craft_get_order, old_craft_id_to_new_craft_id
