from BaseClasses import Item, ItemClassification
from .data import base_id
from typing import List, Dict, TYPE_CHECKING

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
    "Filler Item"  : base_id + 5,
}

trackmania_item_groups = {
        "Medals": {"Bronze Medal", "Silver Medal", "Gold Medal", "Author Medal"}
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
        case "Filler Item":
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


def create_itempool(world: "TrackmaniaWorld") -> List[Item]:
    itempool: List[Item] = []
    #create medals for each map
    total_map_count : int = world.options.series_number * world.options.series_map_number
    itempool += create_medals(world, "Bronze Medal", 0, total_map_count)
    itempool += create_medals(world, "Silver Medal", 100, total_map_count)
    itempool += create_medals(world, "Gold Medal", 200, total_map_count)
    itempool += create_medals(world, "Author Medal", 300, total_map_count)

    #each map has one additional check for reaching the target time we can fill with skips and filler
    skip_count = round(float(total_map_count) * (world.options.skip_percentage / 100.0))
    itempool += create_items(world, "Map Skip", skip_count)
    itempool += create_items(world,"Filler Item", total_map_count - skip_count)

    return itempool

def create_medals(world: "TrackmaniaWorld", medal: str, minimumTargetTime:int, mapCount: int) -> List[Item]:
    if (world.options.target_time >= minimumTargetTime):
        return create_items(world, medal, mapCount)
    else:
        return []

def create_item(world: "TrackmaniaWorld", name: str) -> Item:
    id = trackmania_items[name]
    return TrackmaniaItem(name, determine_item_classification(world,name), id, world.player)

def create_items(world: "TrackmaniaWorld", name: str, count: int) -> List[Item]:

    id = trackmania_items[name]
    itemlist: List[Item] = []

    for i in range(count):
        itemlist += [TrackmaniaItem(name, determine_item_classification(world,name), id, world.player)]

    return itemlist

