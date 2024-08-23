from typing import List, Tuple

from . import items
from .locations import LocationData, free_character_locations, earned_character_locations
from ..AutoWorld import World


def create_itempool(locations: List[LocationData], multiworld: World) -> Tuple[List[str], str]:
    chosen_character = get_chosen_character(multiworld)
    character_pool = create_character_pool(multiworld, chosen_character)
    key_item_pool = create_key_item_pool(multiworld)
    location_count = len(locations) - len(character_pool) - len(key_item_pool)
    useful_percentage = multiworld.options.UsefulPercentage.value
    useful_count = location_count * useful_percentage // 100
    result_pool = []
    result_pool.extend(character_pool)
    result_pool.extend(key_item_pool)
    result_pool.extend(multiworld.random.choices([item.name for item in items.useful_items], k=useful_count))
    result_pool.extend(multiworld.random.choices([item.name for item in items.filler_items], k=location_count - useful_count))
    return (result_pool, chosen_character)


def create_character_pool(multiworld: World, chosen_character: str) -> List[str]:
    character_pool = []
    allowed_characters = [character for character in items.characters if character != "None"]
    if chosen_character != "None":
        allowed_characters.remove(chosen_character)
    #if multiworld.options.AllowDuplicateCharacters.value == False:
    #    allowed_characters.clear()
    character_slots = 18 # All slots
    filled_character_slots = 2  # Starting characters
    if multiworld.options.HeroChallenge.current_key != "none":
        character_pool.append(chosen_character)
        filled_character_slots -= 1
    if multiworld.options.NoFreeCharacters.current_key == "false":
        filled_character_slots += len(free_character_locations)
    if multiworld.options.NoEarnedCharacters.current_key == "false":
        filled_character_slots += len(earned_character_locations)
    if filled_character_slots > len(items.characters) - 1:
        character_pool.extend([character for character in allowed_characters if character != "None"])
        filled_character_slots -= len(allowed_characters)
        character_pool.extend(multiworld.random.choices(allowed_characters, k=filled_character_slots))
    else:
        character_pool.extend(multiworld.random.sample(allowed_characters, filled_character_slots))
    for x in range(len(character_pool), character_slots):
        character_pool.append("None")
    return character_pool


def get_chosen_character(multiworld):
    chosen_character = "None"
    if multiworld.options.HeroChallenge.current_key != "none":
        option_value = str(multiworld.options.HeroChallenge.current_key)
        if option_value == "random":
            chosen_character = multiworld.random.choice(items.characters)
        else:
            chosen_character = option_value.capitalize()
    return chosen_character


def create_key_item_pool(multiworld: World) -> List[str]:
    key_item_pool = [item.name for item in items.key_items]  # Start with every key item but Dark Matter
    if multiworld.options.PassEnabled.current_key == "false":
        key_item_pool.remove("Pass")
    if multiworld.options.DarkMatterHunt.current_key == "true":
        dark_matter_count = 75  # Placeholder until option for number of Dark Matters is made
        for i in range(dark_matter_count):
            key_item_pool.append("DkMatter")
    return key_item_pool


