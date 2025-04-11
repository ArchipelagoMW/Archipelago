from BaseClasses import Item, ItemClassification

class TrackmaniaItem(Item):
    game = "Trackmania"

class ItemData:
    id:int
    classification: ItemClassification

trackmania_items: dict[str,int] = {
    "Bronze Medal" : 24001,
    "Silver Medal" : 24002,
    "Gold Medal"   : 24003,
    "Author Medal" : 24004,
    "Map Skip"     : 24005,
    "Filler Item"  : 24006,
}

trackmania_item_groups = {
        "Medals": {"Bronze Medal", "Silver Medal", "Gold Medal", "Author Medal"},
        "Filler": {"Filler Item"},
}