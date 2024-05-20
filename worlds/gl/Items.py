import typing

from BaseClasses import Item, ItemClassification


class ItemData(typing.NamedTuple):
    code: int
    itemName: str
    progression: ItemClassification


class GLItem(Item):
    game: str = "Gauntlet Legends"


itemList: typing.List[ItemData] = [
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
    ItemData(77780012, "Electric Shield", ItemClassification.filler),
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
    # ItemData(77780028, "Anti-Death Halo", ItemClassification.filler),
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
    ItemData(77780055, "Valley of Fire Obelisk", ItemClassification.progression),
    ItemData(77780056, "Dagger Peak Obelisk", ItemClassification.progression),
    ItemData(77780057, "Cliffs of Desolation Obelisk", ItemClassification.progression),
    ItemData(77780058, "Poisoned Fields Obelisk", ItemClassification.progression),
    ItemData(77780059, "Haunted Cemetery Obelisk", ItemClassification.progression),
    ItemData(77780060, "Castle Courtyard Obelisk", ItemClassification.progression),
    ItemData(77780061, "Dungeon of Torment Obelisk", ItemClassification.progression),
]

item_frequencies: typing.Dict[str, int] = {
    "Key": 1000,
    "Lightning Potion": 45,
    "Light Potion": 40,
    "Acid Potion": 40,
    "Fire Potion": 42,
    "Acid Breath": 33,
    "Electric Breath": 33,
    "Fire Breath": 33,
    "Light Amulet": 32,
    "Acid Amulet": 32,
    "Lightning Amulet": 32,
    "Fire Amulet": 35,
    "Lightning Shield": 33,
    "Fire Shield": 33,
    "Invisibility": 34,
    "Levitate": 32,
    "Speed Boots": 33,
    "3-Way Shot": 37,
    "5-Way Shot": 33,
    "Rapid Fire": 36,
    "Reflective Shot": 37,
    "Reflective Shield": 33,
    "Super Shot": 33,
    "Timestop": 33,
    "Phoenix Familiar": 37,
    "Growth": 36,
    "Shrink": 35,
    "Thunder Hammer": 35,
    "Invulnerability": 35,
    "Fruit": 100,
    "Meat": 100,
    "Gold": 150
}

item_table: typing.Dict[str, ItemData] = {item.itemName: item for item in itemList}
items_by_id: typing.Dict[int, ItemData] = {item.code: item for item in itemList}
