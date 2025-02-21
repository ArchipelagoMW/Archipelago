import pkgutil
from typing import List, Tuple

from . import items, csvdb
from .locations import LocationData, free_character_locations, earned_character_locations, all_locations, \
    minor_locations, major_locations, areas_curves
from ..AutoWorld import World
from ..oot import generate_itempool


def create_itempool(locations: List[LocationData], world: World) -> Tuple[List[str], str, str]:
    chosen_character = get_chosen_character(world)
    character_pool = create_character_pool(world, chosen_character)
    second_starter = get_second_character(world, chosen_character, character_pool)
    key_item_pool = create_key_item_pool(world)
    location_count = len(locations) - len(character_pool) - len(key_item_pool) - 33  # Objective Status locations hack
    if world.is_vanilla_game():
        location_count -= 1  # We aren't using the Objective Reward location.
    if (world.options.HeroChallenge.current_key != "none"
            and not world.options.ForgeTheCrystal):
        location_count -= 1  # We're manually placing the Advance Weapon at Kokkol
    result_pool = []
    result_pool.extend(character_pool)
    result_pool.extend(key_item_pool)
    result_pool.extend(create_general_pool(world, location_count, len(key_item_pool)))
    return (result_pool, chosen_character, second_starter)


def create_character_pool(world: World, chosen_character: str) -> List[str]:
    # Create the pool of characters to place.
    character_pool = []
    allowed_characters = sorted([character for character in world.options.AllowedCharacters.value if character != "None"])
    # If we have a Hero, we only get the one unless there's no other choice.
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
        filled_character_slots += 1  # Kain3 slot goes unused in this objective
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
    # Get a starting character. A Hero if applicable, otherwise random from the list of unrestricted characters.
    if world.options.HeroChallenge.current_key != "none":
        option_value = str(world.options.HeroChallenge.current_key)
        if option_value == "random_character":
            chosen_character = world.random.choice([character_choice for character_choice in items.characters if character_choice != "None"])
        else:
            chosen_character = option_value.capitalize()
    else:
        allowed_characters = world.options.AllowedCharacters.value - world.options.RestrictedCharacters.value - {"None"}
        if len(allowed_characters) > 0:
            chosen_character = world.random.choice(sorted(allowed_characters))
        else:
            chosen_character = world.random.choice(sorted(world.options.AllowedCharacters.value))
    return chosen_character

def get_second_character(world: World, chosen_character: str, character_pool: List[str]):
    pruned_pool = [character for character in character_pool if character != "None"
                   and character not in world.options.RestrictedCharacters.value]
    if world.options.AllowDuplicateCharacters.value == True:
        pruned_pool = [character for character in pruned_pool if character != chosen_character]
    pruned_pool.remove(chosen_character)
    if len(pruned_pool) > 0:
        return world.random.choice(sorted(pruned_pool))
    else:
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


def create_general_pool(world: World, location_count: int, key_item_count: int):
    #Tstandard is items from tiers 1-5
    #TWild is items from tiers 1-8
    if world.options.WackyChallenge.current_key == "kleptomania":
        refined_filler = [item for item in items.filler_items if item.group not in ["weapon", "armor"]]
        refined_useful = [item for item in items.useful_items if item.group not in ["weapon", "armor"]]
    else:
        refined_filler = [*items.filler_items]
        refined_useful = [*items.useful_items]
    refined_filler = [item for item in refined_filler if item.tier >= world.options.MinTier.value]
    refined_useful = [item for item in refined_useful if item.tier <= world.options.MaxTier.value]
    refined_set = [*refined_useful, *refined_filler]
    priority_locations = world.options.priority_locations.value
    required_useful_count = len(priority_locations | set(major_locations))
    item_pool = world.random.choices(refined_useful, k=required_useful_count - key_item_count)
    if world.options.ItemRandomization.current_key == "standard":
        refined_set = [item for item in refined_set if item.tier < 6]
        item_pool.extend(world.random.choices(refined_set, k=location_count))
    if world.options.ItemRandomization.current_key == "wild":
        item_pool = world.random.choices(refined_set, k=location_count)
    if world.options.ItemRandomization.current_key == "pro" or world.options.ItemRandomization.current_key == "wildish":
        tiers = [0, 1, 2, 3, 4, 5, 6, 7]
        for location in minor_locations:
            if location.name in world.options.priority_locations.value:
                continue
            area_curve = areas_curves[location.area]
            if world.options.ItemRandomization.current_key == "pro":
                tier_weights = [
                    int(area_curve.tier1),
                    int(area_curve.tier2),
                    int(area_curve.tier3),
                    int(area_curve.tier4),
                    int(area_curve.tier5),
                    int(area_curve.tier6),
                    int(area_curve.tier7),
                    int(area_curve.tier8),
                ]
            else:
                tier_weights = [
                    int(area_curve.tier1) * 7 // 8,
                    (int(area_curve.tier1) * 1 // 8) + (int(area_curve.tier2) * 6 // 8),
                    (int(area_curve.tier2) * 2 // 8) + (int(area_curve.tier3) * 5 // 8),
                    (int(area_curve.tier3) * 3 // 8) + (int(area_curve.tier4) * 4 // 8),
                    (int(area_curve.tier4) * 4 // 8) + (int(area_curve.tier5) * 3 // 8),
                    (int(area_curve.tier5) * 5 // 8) + (int(area_curve.tier6) * 2 // 8),
                    (int(area_curve.tier6) * 6 // 8) + (int(area_curve.tier7) * 1 // 8),
                    (int(area_curve.tier7) * 7 // 8) + int(area_curve.tier8),
                ]
            chosen_tier = world.random.choices(tiers, tier_weights, k=1)[0]
            chosen_item = world.random.choice(items.items_by_tier[chosen_tier])
            while chosen_item not in refined_set:
                chosen_tier = world.random.choices(tiers, tier_weights, k=1)[0]
                chosen_item = world.random.choice(items.items_by_tier[chosen_tier])
            item_pool.append(chosen_item)
    return [item.name for item in item_pool]