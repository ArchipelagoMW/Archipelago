from BaseClasses import Item
import typing


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool


class MinecraftItem(Item):
    game: str = "Minecraft"


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
    "50 XP": ItemData(45028, False), 
    "3 Ender Pearls": ItemData(45029, True),
    "4 Lapis Lazuli": ItemData(45030, False), 
    "16 Porkchops": ItemData(45031, False), 
    "8 Gold Ore": ItemData(45032, False), 
    "Rotten Flesh": ItemData(45033, False), 
    "Single Arrow": ItemData(45034, False), 
    "32 Arrows": ItemData(45035, False),
    "Saddle": ItemData(45036, False),
    "Structure Compass (Village)": ItemData(45037, True),
    "Structure Compass (Pillager Outpost)": ItemData(45038, True),
    "Structure Compass (Nether Fortress)": ItemData(45039, True),
    "Structure Compass (Bastion Remnant)": ItemData(45040, True),
    "Structure Compass (End City)": ItemData(45041, True),
    "Bee Trap (Minecraft)": ItemData(45100, False),

    "Victory": ItemData(None, True)
}

# If not listed here then has frequency 1
item_frequencies = {
    "Progressive Weapons": 3,
    "Progressive Tools": 3, 
    "Progressive Armor": 2,
    "8 Netherite Scrap": 2, 
    "8 Emeralds": 0,
    "4 Emeralds": 8, 
    "4 Diamond Ore": 4, 
    "16 Iron Ore": 4, 
    "500 XP": 0,
    "100 XP": 0,
    "50 XP": 21,
    "3 Ender Pearls": 4, 
    "4 Lapis Lazuli": 2, 
    "16 Porkchops": 8, 
    "8 Gold Ore": 4, 
    "Rotten Flesh": 4, 
    "Single Arrow": 0, 
    "32 Arrows": 4,
    "Structure Compass (Village)": 0,
    "Structure Compass (Pillager Outpost)": 0,
    "Structure Compass (Nether Fortress)": 0,
    "Structure Compass (Bastion Remnant)": 0,
    "Structure Compass (End City)": 0,
    "Bee Trap (Minecraft)": 0,
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}
