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
    "Victory",
]

post_wall_of_flesh_items = [
    "Hardmode",
    "Post-Pirate Invasion",
    "Post-Queen Slime",
    "Post-The Twins",
    "Post-The Destroyer",
    "Post-Skeletron Prime",
    "Post-Old One's Army Tier 2",
    "Post-Duke Fishron",
]

for item in post_wall_of_flesh_items:
    items.append(item)

post_plantera_items = [
    "Post-Frost Legion",
    "Post-Plantera",
    "Post-Golem",
    "Post-Old One's Army Tier 3",
    "Post-Martian Madness",
    "Post-Mourning Wood",
    "Post-Pumpking",
    "Post-Everscream",
    "Post-Santa-NK1",
    "Post-Ice Queen",
    "Post-Empress of Light",
    "Post-Lunatic Cultist",
    "Post-Lunar Events",
]

for item in post_plantera_items:
    items.append(item)

post_moon_lord_items = [
    "Post-Moon Lord"
]

for item in post_moon_lord_items:
    items.append(item)

item_items = [
    "Hermes Boots",
    "Magic Mirror",
    "Cloud in a Bottle",
    "Grappling Hook",
    "Climbing Claws",
    "Fledgling Wings",
    "Demon Conch",
    "Magic Conch",
    "Anklet of the Wind",
    "Aglet",
    "Ice Skates",
    "Lava Charm",
    "Obsidian Rose",
    "Nature's Gift",
    "Feral Claws",
    "Magma Stone",
    "Shark Tooth Necklace",
    "Cobalt Shield",
    "Band of Regeneration",
    "Philosopher's Stone",
    "Cross Necklace",
    "Magic Quiver",
    "Rifle Scope",
    "Celestial Magnet",
    "Rod of Discord",
    "Flying Carpet",
    "Lifeform Analyzer",
    "Ancient Chisel",
    "Moon Charm",
    "Neptune's Shell",
    "Shoe Spikes",
    "Tabi",
    "Black Belt",
    "Flesh Knuckles",
    "Putrid Scent",
    "Paladin's Shield",
    "Frozen Turtle Shell",
    "Star Cloak",
    "Discount Card",
    "Red Counterweight",
    "Yoyo Glove",
    "Depth Meter",
    "Compass",
    "Radar",
    "DPS Meter",
    "Metal Detector",
    "Sextant",
    "Stopwatch",
    "Tally Counter",
    "Fisherman's Pocket Guide",
    "High Test Fishing Line",
    "Angler Earring",
    "Tackle Box",
    "Lavaproof Fishing Hook",
    "Weather Radio",
    "Blindfold",
    "Pocket Mirror",
    "Vitamins",
    "Armor Polish",
    "Adhesive Bandage",
    "Bezoar",
    "Nazar",
    "Megaphone",
    "Trifold Map",
    "Fast Clock",
    "Brick Layer",
    "Extendo Grip",
    "Paint Sprayer",
    "Portable Cement Mixer",
    "Treasure Magnet",
    "Step Stool",
    "Gold Ring",
    "Lucky Coin",
]

# for item in item_items:
#     items.append(item)

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
]

post_wall_of_flesh_locations = [
    "Pirate Invasion",
    "Queen Slime",
    "The Twins",
    "The Destroyer",
    "Skeletron Prime",
    "Old One's Army Tier 2",
    "Plantera",
    "Duke Fishron",
]

for location in post_wall_of_flesh_locations:
    locations.append(location)

post_plantera_locations = [
    "Frost Legion",
    "Golem",
    "Old One's Army Tier 3",
    "Martian Madness",
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

for location in post_plantera_locations:
    locations.append(location)

post_moon_lord_locations = [
    "Zenith"
]

for location in post_moon_lord_locations:
    locations.append(location)

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
