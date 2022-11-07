from BaseClasses import Item
import typing


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool
    consumable: bool


class MinecraftItem(Item):
    game: str = "Minecraft"


item_table = {
    "Archery": ItemData(45000, True, False),
    "Progressive Resource Crafting": ItemData(45001, True, False),
    # "Resource Blocks": ItemData(45002, True, False),
    "Brewing": ItemData(45003, True, False),
    "Enchanting": ItemData(45004, True, False),
    "Bucket": ItemData(45005, True, False),
    "Flint and Steel": ItemData(45006, True, False),
    "Bed": ItemData(45007, True, False),
    "Bottles": ItemData(45008, True, False),
    "Shield": ItemData(45009, True, False),
    "Fishing Rod": ItemData(45010, True, False),
    "Campfire": ItemData(45011, True, False),
    "Progressive Weapons": ItemData(45012, True, False),
    "Progressive Tools": ItemData(45013, True, False),
    "Progressive Armor": ItemData(45014, True, False),
    "8 Netherite Scrap": ItemData(45015, True, True),
    "8 Emeralds": ItemData(45016, False, True),
    "4 Emeralds": ItemData(45017, False, True),
    "Channeling Book": ItemData(45018, True, True),
    "Silk Touch Book": ItemData(45019, True, True),
    "Sharpness III Book": ItemData(45020, False, True),
    "Piercing IV Book": ItemData(45021, True, True),
    "Looting III Book": ItemData(45022, False, True),
    "Infinity Book": ItemData(45023, False, True),
    "4 Diamond Ore": ItemData(45024, False, True),
    "16 Iron Ore": ItemData(45025, False, True),
    "500 XP": ItemData(45026, False, True),
    "100 XP": ItemData(45027, False, True),
    "50 XP": ItemData(45028, False, True),
    "3 Ender Pearls": ItemData(45029, True, True),
    "4 Lapis Lazuli": ItemData(45030, False, True),
    "16 Porkchops": ItemData(45031, False, True),
    "8 Gold Ore": ItemData(45032, False, True),
    "Rotten Flesh": ItemData(45033, False, True),
    "Single Arrow": ItemData(45034, False, True),
    "32 Arrows": ItemData(45035, False, True),
    "Saddle": ItemData(45036, True, True),
    "Structure Compass (Village)": ItemData(45037, True, True),
    "Structure Compass (Pillager Outpost)": ItemData(45038, True, True),
    "Structure Compass (Nether Fortress)": ItemData(45039, True, True),
    "Structure Compass (Bastion Remnant)": ItemData(45040, True, True),
    "Structure Compass (End City)": ItemData(45041, True, True),
    "Shulker Box": ItemData(45042, False, True),
    "Dragon Egg Shard": ItemData(45043, True, False),
    "Spyglass": ItemData(45044, True, False),
    "Lead": ItemData(45045, True, False),

    "Bee Trap": ItemData(45100, False, True),
    "Blaze Rods": ItemData(None, True, False),
    "Defeat Ender Dragon": ItemData(None, True, False),
    "Defeat Wither": ItemData(None, True, False),
}

# 33 required items
required_items = {
    "Archery": 1,
    "Progressive Resource Crafting": 2,
    "Brewing": 1,
    "Enchanting": 1,
    "Bucket": 1,
    "Flint and Steel": 1,
    "Bed": 1,
    "Bottles": 1,
    "Shield": 1,
    "Fishing Rod": 1,
    "Campfire": 1,
    "Progressive Weapons": 3,
    "Progressive Tools": 3,
    "Progressive Armor": 2,
    "8 Netherite Scrap": 2,
    "Channeling Book": 1,
    "Silk Touch Book": 1,
    "Sharpness III Book": 1,
    "Piercing IV Book": 1,
    "Looting III Book": 1,
    "Infinity Book": 1,
    "3 Ender Pearls": 4,
    "Saddle": 1,
    "Spyglass": 1,
    "Lead": 1,
}

junk_weights = {
    "4 Emeralds": 2,
    "4 Diamond Ore": 1,
    "16 Iron Ore": 1,
    "50 XP": 4,
    "16 Porkchops": 2,
    "8 Gold Ore": 1,
    "Rotten Flesh": 1,
    "32 Arrows": 1,
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}
