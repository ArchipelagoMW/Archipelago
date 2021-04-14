from BaseClasses import Region, Entrance, Location, MultiWorld, Item
import typing

class ItemData(typing.NamedTuple):
    code: int
    progression: bool

class MinecraftItem(Item):
    game: str = "Minecraft"
    def __init__(self, name: str, progression: bool, code: int, player: int):
        super().__init__(name, progression, code, player)

item_table = {
    "Archery": ItemData(45000, True),
    "Ingot Crafting": ItemData(45001, True),
    "Resource Blocks": ItemData(45002, True),
    "Brewing": ItemData(45003, True),
    "Enchanting": ItemData(45004, True),
    "Bucket": ItemData(45005, True),
    "Flint and Steel": ItemData(45006, True),
    "Bed": ItemData(45007, True),
    "Bottles": ItemData(45008, True),
    "Shield": ItemData(45009, True),
    "Fishing Rod": ItemData(45010, True),
    "Campfire": ItemData(45011, True),
    "Progressive Weapons": ItemData(45012, True),
    "Progressive Tools": ItemData(45013, True),
    "Progressive Armor": ItemData(45014, True),
    "8 Netherite Scrap": ItemData(45015, True),
    "8 Emeralds": ItemData(45016, False),
    "4 Emeralds": ItemData(45017, False),
    "Channeling Book": ItemData(45018, True),
    "Silk Touch Book": ItemData(45019, True),
    "Sharpness III Book": ItemData(45020, False),
    "Piercing IV Book": ItemData(45021, True),
    "Looting III Book": ItemData(45022, False),
    "Infinity Book": ItemData(45023, False),
    "4 Diamond Ore": ItemData(45024, False),
    "16 Iron Ore": ItemData(45025, False),
    "500 XP": ItemData(45026, False),
    "100 XP": ItemData(45027, False),
    "50 XP": ItemData(45028, False)
}

# If not listed here then has frequency 1
item_frequencies = {
    "Progressive Weapons": 3,
    "Progressive Tools": 3, 
    "Progressive Armor": 2,
    "8 Netherite Scrap": 2, 
    "8 Emeralds": 4, 
    "4 Emeralds": 8, 
    "4 Diamond Ore": 4, 
    "16 Iron Ore": 4, 
    "500 XP": 6,
    "100 XP": 10,
    "50 XP": 16
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items()}
