import typing

from BaseClasses import Item, ItemClassification


class ItemData(typing.NamedTuple):
    code: int
    item_name: str
    progression: ItemClassification


class GLItem(Item):
    game: str = "Gauntlet Legends"


item_list: typing.List[ItemData] = [
    ItemData(77780000, "Key", ItemClassification.filler),
    ItemData(77780001, "Lightning Potion", ItemClassification.filler),
    ItemData(77780002, "Light Potion", ItemClassification.filler),
    ItemData(77780003, "Acid Potion", ItemClassification.filler),
    ItemData(77780004, "Fire Potion", ItemClassification.filler),
    ItemData(77780005, "Acid Breath", ItemClassification.filler),
    ItemData(77780006, "Lightning Breath", ItemClassification.filler),
    ItemData(77780007, "Fire Breath", ItemClassification.filler),
    ItemData(77780008, "Light Amulet", ItemClassification.filler),
    ItemData(77780009, "Acid Amulet", ItemClassification.filler),
    ItemData(77780010, "Lightning Amulet", ItemClassification.filler),
    ItemData(77780011, "Fire Amulet", ItemClassification.filler),
    ItemData(77780012, "Lightning Shield", ItemClassification.filler),
    ItemData(77780013, "Fire Shield", ItemClassification.filler),
    ItemData(77780014, "Invisibility", ItemClassification.filler),
    ItemData(77780015, "Levitate", ItemClassification.filler),
    ItemData(77780016, "Speed Boots", ItemClassification.filler),
    ItemData(77780017, "3-Way Shot", ItemClassification.filler),
    ItemData(77780018, "5-Way Shot", ItemClassification.filler),
    ItemData(77780019, "Rapid Fire", ItemClassification.filler),
    ItemData(77780020, "Reflective Shot", ItemClassification.filler),
    ItemData(77780021, "Reflective Shield", ItemClassification.filler),
    ItemData(77780022, "Super Shot", ItemClassification.filler),
    ItemData(77780023, "Timestop", ItemClassification.filler),
    ItemData(77780024, "Phoenix Familiar", ItemClassification.filler),
    ItemData(77780025, "Growth", ItemClassification.filler),
    ItemData(77780026, "Shrink", ItemClassification.filler),
    ItemData(77780027, "Thunder Hammer", ItemClassification.filler),
    ItemData(77780028, "Anti-Death Halo", ItemClassification.filler),
    ItemData(77780029, "Invulnerability", ItemClassification.filler),
    ItemData(77780030, "Fruit", ItemClassification.filler),
    ItemData(77780031, "Meat", ItemClassification.filler),
    ItemData(77780032, "Runestone 1", ItemClassification.progression),
    ItemData(77780033, "Runestone 2", ItemClassification.progression),
    ItemData(77780034, "Runestone 3", ItemClassification.progression),
    ItemData(77780035, "Runestone 4", ItemClassification.progression),
    ItemData(77780036, "Runestone 5", ItemClassification.progression),
    ItemData(77780037, "Runestone 6", ItemClassification.progression),
    ItemData(77780038, "Runestone 7", ItemClassification.progression),
    ItemData(77780039, "Runestone 8", ItemClassification.progression),
    ItemData(77780040, "Runestone 9", ItemClassification.progression),
    ItemData(77780041, "Runestone 10", ItemClassification.progression),
    ItemData(77780042, "Runestone 11", ItemClassification.progression),
    ItemData(77780043, "Runestone 12", ItemClassification.progression),
    ItemData(77780044, "Runestone 13", ItemClassification.progression),
    ItemData(77780045, "Dragon Mirror Shard", ItemClassification.progression),
    ItemData(77780046, "Yeti Mirror Shard", ItemClassification.progression),
    ItemData(77780047, "Chimera Mirror Shard", ItemClassification.progression),
    ItemData(77780048, "Plague Fiend Mirror Shard", ItemClassification.progression),
    ItemData(77780049, "Ice Axe of Untar", ItemClassification.useful),
    ItemData(77780050, "Flame of Tarkana", ItemClassification.useful),
    ItemData(77780051, "Scimitar of Decapitation", ItemClassification.useful),
    ItemData(77780052, "Marker's Javelin", ItemClassification.useful),
    ItemData(77780053, "Soul Savior", ItemClassification.useful),
    ItemData(77780054, "Gold", ItemClassification.filler),
    ItemData(77780055, "Mountain Obelisk 1", ItemClassification.progression),
    ItemData(77780056, "Mountain Obelisk 2", ItemClassification.progression),
    ItemData(77780057, "Mountain Obelisk 3", ItemClassification.progression),
    ItemData(77780058, "Town Obelisk 1", ItemClassification.progression),
    ItemData(77780059, "Town Obelisk 2", ItemClassification.progression),
    ItemData(77780060, "Castle Obelisk 1", ItemClassification.progression),
    ItemData(77780061, "Castle Obelisk 2", ItemClassification.progression),
    ItemData(77780062, "Death", ItemClassification.trap),
    ItemData(77780063, "Poison Fruit", ItemClassification.trap),
]

item_frequencies: typing.Dict[str, int] = {
    "Key": 1000,
    "Lightning Potion": 50,
    "Light Potion": 50,
    "Acid Potion": 50,
    "Fire Potion": 50,
    "Acid Breath": 50,
    "Lightning Breath": 50,
    "Fire Breath": 50,
    "Light Amulet": 50,
    "Acid Amulet": 50,
    "Lightning Amulet": 50,
    "Fire Amulet": 50,
    "Lightning Shield": 50,
    "Fire Shield": 50,
    "Invisibility": 50,
    "Levitate": 50,
    "Speed Boots": 50,
    "3-Way Shot": 50,
    "5-Way Shot": 50,
    "Rapid Fire": 50,
    "Reflective Shot": 50,
    "Reflective Shield": 50,
    "Super Shot": 50,
    "Timestop": 50,
    "Phoenix Familiar": 50,
    "Growth": 50,
    "Shrink": 50,
    "Thunder Hammer": 50,
    "Invulnerability": 25,
    "Fruit": 100,
    "Meat": 100,
    "Gold": 150,
    "Anti-Death Halo": 30,
    "Death": 50,
    "Poison Fruit": 50,
}

obelisks = [
    "Mountain Obelisk 1",
    "Mountain Obelisk 2",
    "Mountain Obelisk 3",
    "Town Obelisk 1",
    "Town Obelisk 2",
    "Castle Obelisk 1",
    "Castle Obelisk 2"
]

mirror_shards = [
    "Dragon Mirror Shard",
    "Chimera Mirror Shard",
    "Yeti Mirror Shard",
    "Plague Fiend Mirror Shard"
]

item_table: typing.Dict[str, ItemData] = {item.item_name: item for item in item_list}
items_by_id: typing.Dict[int, ItemData] = {item.code: item for item in item_list}
