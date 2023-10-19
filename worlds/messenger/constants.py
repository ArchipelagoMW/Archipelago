from .shop import FIGURINES, SHOP_ITEMS

# items
# listing individual groups first for easy lookup
NOTES = [
    "Key of Hope",
    "Key of Chaos",
    "Key of Courage",
    "Key of Love",
    "Key of Strength",
    "Key of Symbiosis",
]

PROG_ITEMS = [
    "Wingsuit",
    "Rope Dart",
    "Lightfoot Tabi",
    "Power Thistle",
    "Demon King Crown",
    "Ruxxtin's Amulet",
    "Magic Firefly",
    "Sun Crest",
    "Moon Crest",
    # "Astral Seed",
    # "Astral Tea Leaves",
    "Money Wrench",
]

PHOBEKINS = [
    "Necro",
    "Pyro",
    "Claustro",
    "Acro",
]

USEFUL_ITEMS = [
    "Windmill Shuriken",
]

FILLER = {
    "Time Shard": 5,
    "Time Shard (10)": 10,
    "Time Shard (50)": 20,
    "Time Shard (100)": 20,
    "Time Shard (300)": 10,
    "Time Shard (500)": 5,
}

# item_name_to_id needs to be deterministic and match upstream
ALL_ITEMS = [
    *NOTES,
    "Windmill Shuriken",
    "Wingsuit",
    "Rope Dart",
    "Lightfoot Tabi",
    # "Astral Seed",
    # "Astral Tea Leaves",
    "Candle",
    "Seashell",
    "Power Thistle",
    "Demon King Crown",
    "Ruxxtin's Amulet",
    "Magic Firefly",
    "Sun Crest",
    "Moon Crest",
    *PHOBEKINS,
    "Power Seal",
    *FILLER,
    *SHOP_ITEMS,
    *FIGURINES,
    "Money Wrench",
]

# locations
# the names of these don't actually matter, but using the upstream's names for now
# order must be exactly the same as upstream
ALWAYS_LOCATIONS = [
    # notes
    "Sunken Shrine - Key of Love",
    "Corrupted Future - Key of Courage",
    "Underworld - Key of Chaos",
    "Elemental Skylands - Key of Symbiosis",
    "Searing Crags - Key of Strength",
    "Autumn Hills - Key of Hope",
    # upgrades
    "Howling Grotto - Wingsuit",
    "Searing Crags - Rope Dart",
    "Sunken Shrine - Lightfoot Tabi",
    "Autumn Hills - Climbing Claws",
    # quest items
    "Ninja Village - Astral Seed",
    "Searing Crags - Astral Tea Leaves",
    "Ninja Village - Candle",
    "Quillshroom Marsh - Seashell",
    "Searing Crags - Power Thistle",
    "Forlorn Temple - Demon King",
    "Catacombs - Ruxxtin's Amulet",
    "Riviere Turquoise - Butterfly Matriarch",
    "Sunken Shrine - Sun Crest",
    "Sunken Shrine - Moon Crest",
    # phobekins
    "Catacombs - Necro",
    "Searing Crags - Pyro",
    "Bamboo Creek - Claustro",
    "Cloud Ruins - Acro",
]

BOSS_LOCATIONS = [
    "Autumn Hills - Leaf Golem",
    "Catacombs - Ruxxtin",
    "Howling Grotto - Emerald Golem",
    "Quillshroom Marsh - Queen of Quills",
]
