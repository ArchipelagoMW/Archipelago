from typing import List, Tuple

from . import items
from .locations import LocationData, free_character_locations, earned_character_locations
from ..AutoWorld import World


def create_itempool(locations: List[LocationData], world: World) -> Tuple[List[str], str]:
    chosen_character = get_chosen_character(world)
    character_pool = create_character_pool(world, chosen_character)
    key_item_pool = create_key_item_pool(world)
    location_count = len(locations) - len(character_pool) - len(key_item_pool) - 33  # Objective Status locations hack
    if world.is_vanilla_game():
        key_item_pool.append("Crystal")
        location_count -= 2  # We're adding in the crystal manually, and we aren't using the Objective Reward location.
    if (world.options.HeroChallenge.current_key != "none"
            and not world.options.ForgeTheCrystal):
        location_count -= 1  # We're manually placing the Advance Weapon at Kokkol
    if world.options.ConquerTheGiant:
        location_count -= 1  # No Kain3 location in Giant%
    useful_percentage = world.options.UsefulPercentage.value
    useful_count = location_count * useful_percentage // 100
    result_pool = []
    result_pool.extend(character_pool)
    result_pool.extend(key_item_pool)
    result_pool.extend(world.random.choices([item.name for item in items.useful_items
                                             if item.tier <= world.options.MaxTier.value
                                             and not (item.name == "Adamant Armor" and world.options.NoAdamantArmors)],
                                            k=useful_count))
    result_pool.extend(world.random.choices([item.name for item in items.filler_items
                                             if item.tier >= world.options.MinTier.value],
                                            k=location_count - useful_count))
    return (result_pool, chosen_character)


def create_character_pool(world: World, chosen_character: str) -> List[str]:
    character_pool = []
    allowed_characters = sorted([character for character in world.options.AllowedCharacters.value if character != "None"])
    if chosen_character != "None" and world.options.HeroChallenge.current_key != "none":
        if chosen_character in allowed_characters and len(allowed_characters) > 1:
            allowed_characters.remove(chosen_character)
    character_slots = 18 # All slots
    filled_character_slots = 0
    character_pool.append(chosen_character)
    filled_character_slots += 1
    if world.options.NoFreeCharacters:
        filled_character_slots += len(free_character_locations)
    if world.options.NoEarnedCharacters:
        filled_character_slots += len(earned_character_locations)
    elif world.options.ConquerTheGiant:
        character_slots -= 1  # Kain3 slot goes unused in this objective
    if (character_slots - filled_character_slots) > len(allowed_characters):
        if world.options.EnsureAllCharacters:
            character_pool.extend([character for character in allowed_characters if character != "None"])
            filled_character_slots += len(allowed_characters)
        character_pool.extend(world.random.choices(allowed_characters, k=(character_slots - filled_character_slots)))
    else:
        character_pool.extend(world.random.sample(allowed_characters, character_slots - filled_character_slots))
    for x in range(len(character_pool), character_slots):
        character_pool.append("None")
    return character_pool[:18]


def get_chosen_character(world: World):
    chosen_character = "None"
    if world.options.HeroChallenge.current_key != "none":
        option_value = str(world.options.HeroChallenge.current_key)
        if option_value == "random_character":
            chosen_character = world.random.choice(items.characters)
        else:
            chosen_character = option_value.capitalize()
    else:
        allowed_characters = world.options.AllowedCharacters.value - world.options.RestrictedCharacters.value - {"None"}
        if len(allowed_characters) > 0:
            chosen_character = world.random.choice(sorted(allowed_characters))
        else:
            chosen_character = world.random.choice(sorted(world.options.AllowedCharacters.value))
    return chosen_character


def create_key_item_pool(world: World) -> List[str]:
    key_item_pool = [item.name for item in items.key_items]
    if not world.options.PassEnabled:
        key_item_pool.remove("Pass")
    if world.options.FindTheDarkMatter:
        dark_matter_count = 45  # Placeholder until option for number of Dark Matters is made
        for i in range(dark_matter_count):
            key_item_pool.append("DkMatter")
    return key_item_pool


