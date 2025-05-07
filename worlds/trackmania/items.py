import random
from BaseClasses import Item, ItemClassification
from .data import base_id, base_filler_id, filler_item_names
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import TrackmaniaWorld

class TrackmaniaItem(Item):
    game = "Trackmania"

trackmania_items: dict[str,int] = {
    "Bronze Medal" : base_id,
    "Silver Medal" : base_id + 1,
    "Gold Medal"   : base_id + 2,
    "Author Medal" : base_id + 3,
    "Map Skip"     : base_id + 4,
}

trackmania_item_groups = {
    "Medals": {"Bronze Medal", "Silver Medal", "Gold Medal", "Author Medal"},
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

    total_map_count: int = 0#world.options.series_number * world.options.series_map_number
    for x in range(0, world.options.series_number):
        total_map_count += world.slot_data["SeriesData"][x]["MapCount"]

    #create medals for each map
    itempool += create_medals(world, "Author Medal", 300, total_map_count)
    itempool += create_medals(world, "Gold Medal", 200, total_map_count)
    itempool += create_medals(world, "Silver Medal", 100, total_map_count)
    itempool += create_medals(world, "Bronze Medal", 0, total_map_count)

    #each map has one additional check for reaching the target time we can fill with skips and filler
    skip_count = round(float(total_map_count) * (world.options.skip_percentage / 100.0))
    itempool += create_items(world, "Map Skip", skip_count)

    filler_count = total_map_count - skip_count
    for x in range(filler_count):
        filler_name = get_filler_item_name()
        itempool += create_items(world,filler_name, 1)

    return itempool

def create_medals(world: "TrackmaniaWorld", medal: str, minimum_target_time:int, map_count: int) -> list[Item]:
    if world.options.target_time >= minimum_target_time:
        return create_items(world, medal, map_count)
    else:
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

def get_filler_item_name() -> str:
    return filler_item_names[random.randint(0, len(filler_item_names)-1)]

def build_items() -> dict[str,int]:
    # hardcoded items
    items: dict[str, int] = trackmania_items

    # filler items
    filler_id:int = base_filler_id
    for x in range(len(filler_item_names)):
        items[filler_item_names[x]] = filler_id
        filler_id += 1

    return items

