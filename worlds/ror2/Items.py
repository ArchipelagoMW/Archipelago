from BaseClasses import Item
import typing


class RiskOfRainItem(Item):
    game: str = "Risk of Rain 2"

# 37000 - 38000
item_table = {
    "Dio's Best Friend": 37001,
    "Common Item": 37002,
    "Uncommon Item": 37003,
    "Legendary Item": 37004,
    "Boss Item": 37005,
    "Lunar Item": 37006,
    "Equipment": 37007,
    "Item Scrap, White": 37008,
    "Item Scrap, Green": 37009,
    "Item Scrap, Red": 37010,
    "Item Scrap, Yellow": 37011,
    "Victory": None,
    "Beat Level One": None,
    "Beat Level Two": None,
    "Beat Level Three": None,
    "Beat Level Four": None,
    "Beat Level Five": None,
}

junk_weights = {
    "Item Scrap, Green": 16,
    "Item Scrap, Red": 4,
    "Item Scrap, Yellow": 1,
    "Item Scrap, White": 32,
    "Common Item": 64,
    "Uncommon Item": 32,
    "Legendary Item": 8,
    "Boss Item": 4,
    "Lunar Item": 16,
    "Equipment": 32,
}

lookup_id_to_name: typing.Dict[int, str] = {id: name for name, id in item_table.items() if id}
