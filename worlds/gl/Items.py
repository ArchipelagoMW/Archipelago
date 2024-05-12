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
    "Key": 2280,
    "Lightning Potion": 15,
    "Light Potion": 10,
    "Acid Potion": 10,
    "Fire Potion": 12,
    "Acid Breath": 3,
    "Electric Breath": 3,
    "Fire Breath": 3,
    "Light Amulet": 2,
    "Acid Amulet": 2,
    "Lightning Amulet": 2,
    "Fire Amulet": 5,
    "Lightning Shield": 3,
    "Fire Shield": 3,
    "Invisibility": 4,
    "Levitate": 2,
    "Speed Boots": 13,
    "3-Way Shot": 7,
    "5-Way Shot": 3,
    "Rapid Fire": 6,
    "Reflective Shot": 7,
    "Reflective Shield": 3,
    "Super Shot": 3,
    "Timestop": 3,
    "Phoenix Familiar": 7,
    "Growth": 6,
    "Shrink": 5,
    "Thunder Hammer": 5,
    "Invulnerability": 5,
    "Fruit": 50,
    "Meat": 35,
    "Gold": 95
}

item_table: typing.Dict[str, ItemData] = {item.itemName: item for item in itemList}
items_by_id: typing.Dict[int, ItemData] = {item.code: item for item in itemList}
