from typing import List, Tuple

from . import items
from .locations import LocationData, free_character_locations, earned_character_locations
from ..AutoWorld import World


def create_itempool(locations: List[LocationData], multiworld: World) -> Tuple[List[str], str]:
    chosen_character = get_chosen_character(multiworld)
    character_pool = create_character_pool(multiworld, chosen_character)
    key_item_pool = create_key_item_pool(multiworld)
    location_count = len(locations) - len(character_pool) - len(key_item_pool) - 1  # Objective Status location hack
    if (multiworld.options.HeroChallenge.current_key != "none"
            and multiworld.options.ForgeTheCrystal.current_key == "false"):
        location_count -= 1  # We're manyally placing the Advance Weapon at Kokkol
    if multiworld.options.ConquerTheGiant.current_key == "true":
        location_count -= 1  # No Kain3 location in Giant%
    useful_percentage = multiworld.options.UsefulPercentage.value
    useful_count = location_count * useful_percentage // 100
    result_pool = []
    result_pool.extend(character_pool)
    result_pool.extend(key_item_pool)
    result_pool.extend(multiworld.random.choices([item.name for item in items.useful_items
                                                  if item.tier <= multiworld.options.MaxTier.value],
                                                 k=useful_count))
    result_pool.extend(multiworld.random.choices([item.name for item in items.filler_items
                                                  if item.tier >= multiworld.options.MinTier.value],
                                                 k=location_count - useful_count))
    return (result_pool, chosen_character)


def create_character_pool(multiworld: World, chosen_character: str) -> List[str]:
    character_pool = []
    allowed_characters = [character for character in multiworld.options.AllowedCharacters.value if character != "None"]
    if chosen_character != "None":
        if chosen_character in allowed_characters and len(allowed_characters) > 1:
            allowed_characters.remove(chosen_character)
    if "None" in allowed_characters and len(allowed_characters) == 1:
        allowed_characters = [character for character in items.characters if character != "None"]
    character_slots = 18 # All slots
    filled_character_slots = 0
    if multiworld.options.HeroChallenge.current_key != "none":
        character_pool.append(chosen_character)
        filled_character_slots += 1
    if multiworld.options.NoFreeCharacters.current_key == "true":
        filled_character_slots += len(free_character_locations)
    if multiworld.options.NoEarnedCharacters.current_key == "true":
        filled_character_slots += len(earned_character_locations)
    elif multiworld.options.ConquerTheGiant.current_key == "true":
        character_slots -= 1  # Kain3 slot goes unused in this objective
    if (character_slots - filled_character_slots) > len(allowed_characters):
        if multiworld.options.EnsureAllCharacters.current_key == "true":
            character_pool.extend([character for character in allowed_characters if character != "None"])
            filled_character_slots += len(allowed_characters)
        character_pool.extend(multiworld.random.choices(allowed_characters, k=(character_slots - filled_character_slots)))
    else:
        character_pool.extend(multiworld.random.sample(allowed_characters, character_slots - filled_character_slots))
    for x in range(len(character_pool), character_slots):
        character_pool.append("None")
    return character_pool[:18]


def get_chosen_character(multiworld):
    chosen_character = "None"
    if multiworld.options.HeroChallenge.current_key != "none":
        option_value = str(multiworld.options.HeroChallenge.current_key)
        if option_value == "random_character":
            chosen_character = multiworld.random.choice(items.characters)
        else:
            chosen_character = option_value.capitalize()
    else:
        chosen_character = multiworld.random.choice(list(multiworld.options.AllowedCharacters.value))
    return chosen_character


def create_key_item_pool(multiworld: World) -> List[str]:
    key_item_pool = [item.name for item in items.key_items]
    if multiworld.options.PassEnabled.current_key == "false":
        key_item_pool.remove("Pass")
    if multiworld.options.FindTheDarkMatter.current_key == "true":
        dark_matter_count = 45  # Placeholder until option for number of Dark Matters is made
        for i in range(dark_matter_count):
            key_item_pool.append("DkMatter")
    return key_item_pool


