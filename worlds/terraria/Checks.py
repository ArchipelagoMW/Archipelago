from BaseClasses import Location, Item

next_id = 0x7E0000

items = [
    "Nothing",
    "Bound Goblin",
    "Dryad",
    "Progressive Old One's Army",
    "Witch Doctor",
    "Progressive Dungeon",
    "Hardmode",
    "Underground Evil",
    "Hallow",
    "Wizard",
    "Truffle",
    "Hardmode Fishing",
    "Truffle Worm",
    "Steampunker",
    "Life Fruit",
    "Solar Eclipse",
    "Plantera's Bulb",
    "Cyborg",
    "Autohammer",
    "Biome Chests",
    "Post-Plantera Eclipse",
    "Lihzahrd Altar",
    "Prismatic Lacewing",
    "Martian Probe",
    "Cultists",
    "Victory",
]

locations = [
    "Torch God",
    "Goblin Army",
    "King Slime",
    "Eye of Cthulhu",
    "Eater of Worlds or Brain of Cthulhu",
    "Old One's Army Tier 1",
    "Queen Bee",
    "Skeletron",
    "Deerclops",
    "Wall of Flesh",
    "Pirate Invasion",
    "Frost Legion",
    "Queen Slime",
    "The Twins",
    "The Destroyer",
    "Skeletron Prime",
    "Old One's Army Tier 2",
    "Plantera",
    "Golem",
    "Old One's Army Tier 3",
    "Martian Madness",
    "Duke Fishron",
    "Pumpkin Moon",
    "Frost Moon",
    "Empress of Light",
    "Lunatic Cultist",
    "Lunar Events",
    "Moon Lord",
    # "Zenith",
]

# Debugging utility
precollected = []

item_name_to_id: dict[str, int] = {}
location_name_to_id: dict[str, int] = {}

for item in items:
    item_name_to_id[item] = next_id
    next_id += 1

for location in locations:
    location_name_to_id[location] = next_id
    next_id += 1

class TerrariaItem(Item):
    game = "Terraria"

class TerrariaLocation(Location):
    game = "Terraria"
