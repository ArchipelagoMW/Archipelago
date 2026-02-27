from BaseClasses import Item, ItemClassification
from .data import base_id, base_filler_id, filler_item_names
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import TrackmaniaWorld

class TrackmaniaItem(Item):
    game = "Trackmania"

trackmania_items: dict[str,int] = {
    "Bronze Medal"         : base_id,
    "Silver Medal"         : base_id + 1,
    "Gold Medal"           : base_id + 2,
    "Author Medal"         : base_id + 3,
    "Map Skip"             : base_id + 4,
    "PB Discount"          : base_id + 5,
}

trackmania_item_groups = {
    "Medals": {"Bronze Medal", "Silver Medal", "Gold Medal", "Author Medal"},
    "Useful Items": {"Map Skip", "PB Discount"},
    "Filler Items": set(filler_item_names)
}

#Item classification for most of our items is dependent on the target_time setting, so it cannot be hardcoded.
def determine_item_classification(world:"TrackmaniaWorld", name: str) -> ItemClassification:
    target_time = world.options.target_time
    match name:
        case "Bronze Medal":
            return ItemClassification.progression if target_time < 100 else ItemClassification.filler
        case "Silver Medal":
            return ItemClassification.progression if 100 <= target_time < 200 else ItemClassification.filler
        case "Gold Medal":
            return ItemClassification.progression if 200 <= target_time < 300 else ItemClassification.filler
        case "Author Medal":
            return ItemClassification.progression if 300 <= target_time else ItemClassification.filler
        case "Map Skip":
            return ItemClassification.useful
        case "PB Discount":
            return ItemClassification.useful
        case _:
            return ItemClassification.filler
        
def get_progression_medal(world: "TrackmaniaWorld") -> str:
    match world.options.target_time:
        case x if x < 100:
            return "Bronze Medal"
        case x if 100 <= x < 200:
            return "Silver Medal"
        case x if 200 <= x < 300:
            return "Gold Medal"
        case x if 300 <= x:
            return "Author Medal"
        case _:
            return ""


def create_itempool(world: "TrackmaniaWorld") -> list[Item]:
    itempool: list[Item] = []

    total_map_count: int = 0
    for series in world.series_data:
        total_map_count += series["MapCount"]

    total_item_slots: int = (total_map_count * get_locations_per_map(world))
    spots_remaining: int = total_item_slots

    #create medals for each map
    if spots_remaining >= total_map_count:
        itempool += create_medals(world, "Author Medal", 300, total_map_count)
    spots_remaining = total_item_slots - len(itempool)
    if spots_remaining >= total_map_count:
        itempool += create_medals(world, "Gold Medal", 200, total_map_count)
    spots_remaining = total_item_slots - len(itempool)
    if spots_remaining >= total_map_count:
        itempool += create_medals(world, "Silver Medal", 100, total_map_count)
    spots_remaining = total_item_slots - len(itempool)
    if spots_remaining >= total_map_count:
        itempool += create_medals(world, "Bronze Medal", 0, total_map_count)
    spots_remaining = total_item_slots - len(itempool)

    if spots_remaining < 0:
        spots_remaining = 0 # just in case

    skip_count = min(round(float(spots_remaining) * (world.options.skip_percentage / 100.0)),spots_remaining)
    itempool += create_items(world, "Map Skip", skip_count)

    discount_count = min(round(float(spots_remaining) * (world.options.discount_percentage / 100.0)),spots_remaining-skip_count)
    itempool += create_items(world, "PB Discount", discount_count)

    filler_count = spots_remaining - skip_count - discount_count
    for x in range(filler_count):
        filler_name = get_filler_item_name(world)
        itempool += create_items(world,filler_name, 1)

    return itempool

def create_medals(world: "TrackmaniaWorld", medal: str, minimum_target_time:int, map_count: int) -> list[Item]:
    if get_progression_medal(world) != medal and not get_medal_enabled(world, medal):
        return []
    if world.options.target_time >= minimum_target_time:
        return create_items(world, medal, map_count)
    return []

def create_item(world: "TrackmaniaWorld", name: str) -> Item:
    item_id = world.item_name_to_id[name]
    return TrackmaniaItem(name, determine_item_classification(world,name), item_id, world.player)

def create_items(world: "TrackmaniaWorld", name: str, count: int) -> list[Item]:

    item_id = world.item_name_to_id[name]
    itemlist: list[Item] = []

    for i in range(count):
        itemlist += [TrackmaniaItem(name, determine_item_classification(world,name), item_id, world.player)]

    return itemlist

def get_filler_item_name(world: "TrackmaniaWorld") -> str:
    return world.random.choice(filler_item_names)


def get_medal_enabled(world: "TrackmaniaWorld", medal: str) -> bool:
    match medal:
        case "Bronze Medal":
            return not world.options.disable_bronze_medals
        case "Silver Medal":
            return not world.options.disable_silver_medals
        case "Gold Medal":
            return not world.options.disable_gold_medals
        case "Author Medal":
            return True
        case _:
            return True


def get_locations_per_map(world: "TrackmaniaWorld") -> int:
    checks: int = 1
    if world.options.target_time < 100 or not world.options.disable_bronze_locations:
        checks += 1
    if world.options.target_time >= 100 and not world.options.disable_silver_locations:
        checks += 1
    if world.options.target_time >= 200 and not world.options.disable_gold_locations:
        checks += 1
    if world.options.target_time >= 300 and not world.options.disable_author_locations:
        checks += 1
    return checks
    

def build_items() -> dict[str,int]:
    # hardcoded items
    items: dict[str, int] = trackmania_items

    # filler items
    for x, name in enumerate(filler_item_names):
        items[name] = base_filler_id + x

    return items
