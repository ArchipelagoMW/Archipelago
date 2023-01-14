from BaseClasses import Location, Item

next_id = 0x7E0000

items = [
    "Nothing",
    "Torch God's Favor",
    "Post-Goblin Army",
    "Post-King Slime",
    "Post-Eye of Cthulhu",
    "Post-Eater of Worlds or Brain of Cthulhu",
    "Post-Old One's Army Tier 1",
    "Post-Queen Been",
    "Post-Skeletron",
    "Post-Deerclops",
    "Hardmode",
    "Post-Pirate Invasion",
    "Post-Frost Legion",
    "Post-Queen Slime",
    "Post-The Twins",
    "Post-The Destroyer",
    "Post-Skeletron Prime",
    "Post-Old One's Army Tier 2",
    "Post-Plantera",
    "Post-Golem",
    "Post-Old One's Army Tier 3",
    "Post-Martian Madness",
    "Post-Duke Fishron",
    "Post-Mourning Wood",
    "Post-Pumpking",
    "Post-Everscream",
    "Post-Santa-NK1",
    "Post-Ice Queen",
    "Post-Empress of Light",
    "Post-Lunatic Cultist",
    "Post-Lunar Events",
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
    "Mourning Wood",
    "Pumpking",
    "Everscream",
    "Santa-NK1",
    "Ice Queen",
    "Empress of Light",
    "Lunatic Cultist",
    "Lunar Events",
    "Moon Lord",
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
