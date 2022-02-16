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

default_weights = {
    "Item Scrap, Green": 16,
    "Item Scrap, Red": 4,
    "Item Scrap, Yellow": 1,
    "Item Scrap, White": 32,
    "Common Item": 64,
    "Uncommon Item": 32,
    "Legendary Item": 8,
    "Boss Item": 4,
    "Lunar Item": 16,
    "Equipment": 32
}

new_weights = {
    "Item Scrap, Green": 15,
    "Item Scrap, Red": 5,
    "Item Scrap, Yellow": 1,
    "Item Scrap, White": 30,
    "Common Item": 75,
    "Uncommon Item": 40,
    "Legendary Item": 10,
    "Boss Item": 5,
    "Lunar Item": 10,
    "Equipment": 20
}

uncommon_weights = {
    "Item Scrap, Green": 45,
    "Item Scrap, Red": 5,
    "Item Scrap, Yellow": 1,
    "Item Scrap, White": 30,
    "Common Item": 45,
    "Uncommon Item": 100,
    "Legendary Item": 10,
    "Boss Item": 5,
    "Lunar Item": 15,
    "Equipment": 20
}

legendary_weights = {
    "Item Scrap, Green": 15,
    "Item Scrap, Red": 5,
    "Item Scrap, Yellow": 1,
    "Item Scrap, White": 30,
    "Common Item": 50,
    "Uncommon Item": 25,
    "Legendary Item": 100,
    "Boss Item": 5,
    "Lunar Item": 15,
    "Equipment": 20
}

lunartic_weights = {
    "Item Scrap, Green": 0,
    "Item Scrap, Red": 0,
    "Item Scrap, Yellow": 0,
    "Item Scrap, White": 0,
    "Common Item": 0,
    "Uncommon Item": 0,
    "Legendary Item": 0,
    "Boss Item": 0,
    "Lunar Item": 100,
    "Equipment": 0
}

no_scraps_weights = {
    "Item Scrap, Green": 0,
    "Item Scrap, Red": 0,
    "Item Scrap, Yellow": 0,
    "Item Scrap, White": 0,
    "Common Item": 100,
    "Uncommon Item": 40,
    "Legendary Item": 15,
    "Boss Item": 5,
    "Lunar Item": 10,
    "Equipment": 25
}

even_weights = {
    "Item Scrap, Green": 1,
    "Item Scrap, Red": 1,
    "Item Scrap, Yellow": 1,
    "Item Scrap, White": 1,
    "Common Item": 1,
    "Uncommon Item": 1,
    "Legendary Item": 1,
    "Boss Item": 1,
    "Lunar Item": 1,
    "Equipment": 1
}

scraps_only = {
    "Item Scrap, Green": 70,
    "Item Scrap, White": 100,
    "Item Scrap, Red": 30,
    "Item Scrap, Yellow": 5,
    "Common Item": 0,
    "Uncommon Item": 0,
    "Legendary Item": 0,
    "Boss Item": 0,
    "Lunar Item": 0,
    "Equipment": 0
}

item_pool_weights: typing.Dict[int, typing.Dict[str, int]] = {
    0: default_weights,
    1: new_weights,
    2: uncommon_weights,
    3: legendary_weights,
    4: lunartic_weights,
    6: no_scraps_weights,
    7: even_weights,
    8: scraps_only
}

lookup_id_to_name: typing.Dict[int, str] = {id: name for name, id in item_table.items() if id}
