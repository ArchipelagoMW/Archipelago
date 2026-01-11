import typing
from copy import copy

from . import items
from .items import ItemData
from .locations import LocationData, free_character_locations, earned_character_locations, \
    minor_locations, major_locations, areas_curves, get_location_data

if typing.TYPE_CHECKING:
    from . import FF4FEWorld

def create_itempool(locations: list[LocationData], world: "FF4FEWorld") -> tuple[list[str], str, str]:
    character_pool, chosen_character, second_starter = create_character_pool(world)
    key_item_pool = create_key_item_pool(world)
    location_count = len(locations) - len(character_pool) - len(key_item_pool) - 34  # Objective Status locations
    if world.is_vanilla_game():
        location_count -= 1  # We aren't using the Objective Reward location.
    result_pool = []
    result_pool.extend(character_pool)
    result_pool.extend(key_item_pool)
    result_pool.extend(create_general_pool(world, location_count, len(key_item_pool)))
    return (result_pool, chosen_character, second_starter)

def create_character_pool(world: "FF4FEWorld") -> tuple[list[str], str, str]:
    all_allowed_characters = world.options.AllowedCharacters.value
    if len(all_allowed_characters) == 0:
        all_allowed_characters = {"Cecil"}
    allowed_starter_characters = all_allowed_characters - world.options.RestrictedCharacters.value
    if world.options.HeroChallenge.current_key != "none":
        option_value = str(world.options.HeroChallenge.current_key)
        if option_value == "random_character":
            starter = world.random.choice([character_choice for character_choice in items.characters if character_choice != "None"])
        else:
            starter = option_value.capitalize()
        all_allowed_characters -= {starter}
    else:
        if len(allowed_starter_characters) > 0:
            starter = world.random.choice(sorted(allowed_starter_characters))
        else:
            starter = "Cecil" # If we restrict all allowable characters, default to Cecil
    if world.options.AllowDuplicateCharacters:
        if len(allowed_starter_characters) > 0:
            second = world.random.choice(sorted(allowed_starter_characters))
        else:
            second = "Cecil" # Same as above
    else:
        allowed_second_characters = allowed_starter_characters - {starter}
        if len(allowed_second_characters) > 0:
            second = world.random.choice(sorted(allowed_second_characters))
        else:
            second = "Kain" # Once again, a default if everyone's restricted.
    character_pool = list()
    character_pool.append(starter)
    character_pool.append(second)
    slots_to_fill = 18
    filled_slots = 2
    if world.options.NoFreeCharacters:
        filled_slots += len(free_character_locations)
    if world.options.NoEarnedCharacters:
        filled_slots += len(earned_character_locations)
    elif world.options.ConquerTheGiant:
        filled_slots += 1  # Kain3 slot goes unused in this objective
    if (slots_to_fill - filled_slots) > len(all_allowed_characters):
        if world.options.EnsureAllCharacters:
            character_pool.extend([character for character in all_allowed_characters])
            filled_slots += len(all_allowed_characters)
        if len(all_allowed_characters) == 0:
            all_allowed_characters = [starter]
        character_pool.extend(world.random.choices(sorted(all_allowed_characters), k=(slots_to_fill - filled_slots)))
    else:
        character_pool.extend(world.random.sample(sorted(all_allowed_characters), slots_to_fill - filled_slots))
    for x in range(len(character_pool), slots_to_fill):
        character_pool.append("None")
    return character_pool, starter, second



def create_key_item_pool(world: "FF4FEWorld") -> list[str]:
    key_item_pool = [item.name for item in items.key_items]
    if not world.options.PassEnabled:
        key_item_pool.remove("Pass")
    return key_item_pool


def create_general_pool(world: "FF4FEWorld", location_count: int, key_item_count: int):
    if world.options.WackyChallenge.current_key == "kleptomania":
        refined_filler = [item for item in items.filler_items if item.group not in ["weapon", "armor"]]
        refined_useful = [item for item in items.useful_items if item.group not in ["weapon", "armor"]]
    else:
        refined_filler = [*items.filler_items]
        refined_useful = [*items.useful_items]
    if world.options.NoAdamantArmors:
        try:
            refined_useful.remove(items.get_item_data("Adamant Armor"))
        except ValueError: # This will happen in Kleptomaniac seeds.
            pass
    refined_filler = [item for item in refined_filler if item.tier >= world.options.MinTier.value]
    refined_useful = [item for item in refined_useful if item.tier <= world.options.MaxTier.value]
    if world.options.JItems > 1: # If JItems is set to No Itempool or None
        refined_filler = [item for item in refined_filler if item not in items.j_items]
        refined_useful = [item for item in refined_useful if item not in items.j_items]
    refined_set = [*refined_useful, *refined_filler]
    if world.options.ItemRandomization.current_key == "standard":
        refined_set = [item for item in refined_set if item.tier < 6]
    required_useful_count = len(world.options.priority_locations.value)
    if world.options.HeroChallenge != "none" and not world.options.ForgeTheCrystal:
        required_useful_count -= 1
    extra_filler_locations = sorted(world.options.exclude_locations.value & {location.name for location in major_locations})
    if not world.is_vanilla_game():
        required_useful_count += 1
    item_pool = world.random.choices(refined_useful, k=required_useful_count - key_item_count)
    refined_minor_locations = copy(minor_locations)
    if len(item_pool) == 0:
        world.random.shuffle(refined_minor_locations)
        refined_minor_locations = refined_minor_locations[:(required_useful_count - key_item_count)]
    location_list = []
    for location in refined_minor_locations:
        if location.name not in world.options.priority_locations.value:
            location_list.append(location)
    for location in major_locations:
        if location.name not in world.options.priority_locations.value:
            location_list.append(location)
    world.random.shuffle(location_list)
    if world.options.FindTheDarkMatter:
        dark_matter_count = 45
        dark_matter_item = items.get_item_data("DkMatter")
        for i in range(dark_matter_count):
            location_list.pop()
            item_pool.append(dark_matter_item)
    for location in location_list:
        if world.options.ItemRandomization.current_key == "pro" or world.options.ItemRandomization.current_key == "wildish":
            item_pool.append(choose_item_by_weight(world, location, refined_set))
        else:
            item_pool.append(world.random.choice(refined_set))
    for location_name in extra_filler_locations:
        location_data = get_location_data(location_name)
        item_pool.append(choose_item_by_weight(world, location_data, refined_set))
    return [item.name for item in item_pool]


tiers = [0, 1, 2, 3, 4, 5, 6, 7]

def choose_item_by_weight(world: "FF4FEWorld", location: LocationData, item_set: list[ItemData]) -> ItemData:
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
    while chosen_item not in item_set:
        chosen_tier = world.random.choices(tiers, tier_weights, k=1)[0]
        chosen_item = world.random.choice(items.items_by_tier[chosen_tier])
    return chosen_item
