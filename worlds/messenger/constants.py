from .shop import FIGURINES, SHOP_ITEMS

# items
# listing individual groups first for easy lookup
NOTES: list[str] = [
    "Key of Hope",
    "Key of Chaos",
    "Key of Courage",
    "Key of Love",
    "Key of Strength",
    "Key of Symbiosis",
]

PROG_ITEMS: list[str] = [
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
    "Candle",
    "Seashell",
]

PHOBEKINS: list[str] = [
    "Necro",
    "Pyro",
    "Claustro",
    "Acro",
]

USEFUL_ITEMS: list[str] = [
    "Windmill Shuriken",
]

FILLER: dict[str, int] = {
    "Time Shard": 5,
    "Time Shard (10)": 10,
    "Time Shard (50)": 20,
    "Time Shard (100)": 20,
    "Time Shard (300)": 10,
    "Time Shard (500)": 5,
}

TRAPS: dict[str, int] = {
    "Teleport Trap": 5,
    "Prophecy Trap": 10,
}

# item_name_to_id needs to be deterministic and match upstream
ALL_ITEMS: list[str] = [
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
    "Teleport Trap",
    "Prophecy Trap",
]

# locations
# the names of these don't actually matter, but using the upstream's names for now
# order must be exactly the same as upstream
ALWAYS_LOCATIONS: list[str] = [
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
    # seals
    "Ninja Village Seal - Tree House",
    "Autumn Hills Seal - Trip Saws",
    "Autumn Hills Seal - Double Swing Saws",
    "Autumn Hills Seal - Spike Ball Swing",
    "Autumn Hills Seal - Spike Ball Darts",
    "Catacombs Seal - Triple Spike Crushers",
    "Catacombs Seal - Crusher Gauntlet",
    "Catacombs Seal - Dirty Pond",
    "Bamboo Creek Seal - Spike Crushers and Doors",
    "Bamboo Creek Seal - Spike Ball Pits",
    "Bamboo Creek Seal - Spike Crushers and Doors v2",
    "Howling Grotto Seal - Windy Saws and Balls",
    "Howling Grotto Seal - Crushing Pits",
    "Howling Grotto Seal - Breezy Crushers",
    "Quillshroom Marsh Seal - Spikey Window",
    "Quillshroom Marsh Seal - Sand Trap",
    "Quillshroom Marsh Seal - Do the Spike Wave",
    "Searing Crags Seal - Triple Ball Spinner",
    "Searing Crags Seal - Raining Rocks",
    "Searing Crags Seal - Rhythm Rocks",
    "Glacial Peak Seal - Ice Climbers",
    "Glacial Peak Seal - Projectile Spike Pit",
    "Glacial Peak Seal - Glacial Air Swag",
    "Tower of Time Seal - Time Waster",
    "Tower of Time Seal - Lantern Climb",
    "Tower of Time Seal - Arcane Orbs",
    "Cloud Ruins Seal - Ghost Pit",
    "Cloud Ruins Seal - Toothbrush Alley",
    "Cloud Ruins Seal - Saw Pit",
    "Cloud Ruins Seal - Money Farm Room",
    "Underworld Seal - Sharp and Windy Climb",
    "Underworld Seal - Spike Wall",
    "Underworld Seal - Fireball Wave",
    "Underworld Seal - Rising Fanta",
    "Forlorn Temple Seal - Rocket Maze",
    "Forlorn Temple Seal - Rocket Sunset",
    "Sunken Shrine Seal - Ultra Lifeguard",
    "Sunken Shrine Seal - Waterfall Paradise",
    "Sunken Shrine Seal - Tabi Gauntlet",
    "Riviere Turquoise Seal - Bounces and Balls",
    "Riviere Turquoise Seal - Launch of Faith",
    "Riviere Turquoise Seal - Flower Power",
    "Elemental Skylands Seal - Air",
    "Elemental Skylands Seal - Water",
    "Elemental Skylands Seal - Fire",
]

BOSS_LOCATIONS: list[str] = [
    "Autumn Hills - Leaf Golem",
    "Catacombs - Ruxxtin",
    "Howling Grotto - Emerald Golem",
    "Quillshroom Marsh - Queen of Quills",
]
