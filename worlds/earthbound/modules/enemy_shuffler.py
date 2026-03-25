import struct
from ..game_data.text_data import text_encoder
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import EarthBoundWorld
    from ..Rom import LocalRom

enemy_ids = {
    "Insane Cultist": 0x01,
    "Armored Frog": 0x03,
    "Bad Buffalo": 0x04,
    "Black Antoid": 0x05,
    "Red Antoid": 0x06,
    "Ramblin' Evil Mushroom": 0x07,
    "Struttin' Evil Mushroom": 0x08,
    "Mobile Sprout": 0x09,
    "Tough Mobile Sprout": 0x0a,
    "Enraged Fire Plug": 0x0b,
    "Mystical Record": 0x0c,
    "Atomic Power Robot": 0x0d,
    "Nuclear Reactor Robot": 0x0e,
    "Guardian Hieroglyph": 0x0f,
    "Lethal Asp Hieroglyph": 0x10,
    "Electro Swoosh": 0x11,
    "Conducting Menace": 0x12,
    "Conducting Spirit": 0x13,
    "Evil Elemental": 0x14,
    "Annoying Old Party Man": 0x16,
    "Annoying Reveler": 0x17,
    "Unassuming Local Guy": 0x18,
    "New Age Retro Hippie": 0x19,
    "Mighty Bear": 0x1c,
    "Mighty Bear Seven": 0x1d,
    "Putrid Moldyman": 0x1e,
    "Thunder Mite": 0x1f,
    "Cranky Lady": 0x20,
    "Extra Cranky Lady": 0x21,
    "Wetnosaur": 0x23,
    "Chomposaur": 0x24,
    "Gigantic Ant": 0x26,
    "Scalding Coffee Cup": 0x2b,
    "Loaded Dice": 0x2c,
    "Slimy Little Pile": 0x2d,
    "Even Slimier Little Pile": 0x2e,
    "Arachnid!": 0x2f,
    "Arachnid!!!": 0x30,
    "Kraken": 0x31,
    "Bionic Kraken": 0x32,
    "Spinning Robo": 0x33,
    "Whirling Robo": 0x34,
    "Hyper Spinning Robo": 0x35,
    "Cop": 0x36,
    "Coil Snake": 0x37,
    "Thirsty Coil Snake": 0x38,
    "Mr. Batty": 0x39,
    "Elder Batty": 0x3a,
    "Violent Roach": 0x3b,
    "Filthy Attack Roach": 0x3c,
    "Crazed Sign": 0x3d,
    "Wooly Shambler": 0x3e,
    "Wild 'n Wooly Shambler": 0x3f,
    "Skate Punk": 0x40,
    "Skelpion": 0x41,
    "Dread Skelpion": 0x42,
    "Starman": 0x43,
    "Starman Super": 0x44,
    "Ghost of Starman": 0x45,
    "Smilin' Sphere": 0x46,
    "Uncontrollable Sphere": 0x47,
    "Petrified Royal Guard": 0x48,
    "Final Starman": 0x4b,
    "Urban Zombie": 0x4c,
    "Zombie Possessor": 0x4d,
    "Zombie Dog": 0x4e,
    "Over Zealous Cop": 0x50,
    "Territorial Oak": 0x51,
    "Hostile Elder Oak": 0x52,
    "Marauder Octobot": 0x54,
    "Military Octobot": 0x55,
    "Mechanical Octobot": 0x56,
    "Ultimate Octobot": 0x57,
    "Mad Duck": 0x58,
    "Dali's Clock": 0x59,
    "Musica": 0x5b,
    "Desert Wolf": 0x5c,
    "Big Pile of Puke": 0x5e,
    "Kiss of Death": 0x60,
    "French Kiss of Death": 0x61,
    "Foppy": 0x62,
    "Fobby": 0x63,
    "Zap Eel": 0x64,
    "Tangoo": 0x65,
    "Squatter Demon": 0x67,
    "Crested Booka": 0x68,
    "Great Crested Booka": 0x69,
    "Lesser Mook": 0x6a,
    "Mook Senior": 0x6b,
    "Smelly Ghost": 0x6c,
    "Stinky Ghost": 0x6d,
    "Everdred": 0x6e,
    "Attack Slug": 0x6f,
    "Pit Bull Slug": 0x70,
    "Rowdy Mouse": 0x71,
    "Deadly Mouse": 0x72,
    "Care Free Bomb": 0x73,
    "Handsome Tom": 0x75,
    "Smilin' Sam": 0x76,
    "Manly Fish": 0x77,
    "Manly Fish's Brother": 0x78,
    "Runaway Dog": 0x79,
    "Trick or Trick Kid": 0x7a,
    "Abstract Art": 0x7c,
    "Shattered Man": 0x7d,
    "Fierce Shattered Man": 0x7e,
    "Ego Orb": 0x7f,
    "Yes Man Junior": 0x81,
    "Frank": 0x83,
    "Cute Li'l UFO": 0x84,
    "Beautiful UFO": 0x85,
    "Pogo Punk": 0x86,
    "Tough Guy": 0x87,
    "Mad Taxi": 0x88,
    "Mr. Molecule": 0x8a,
    "Worthless Protoplasm": 0x8b,
    "Sentry Robot": 0x8c,
    "Psychic Psycho": 0x8e,
    "Major Psychic Psycho": 0x8f,
    "Mole Playing Rough": 0x90,
    "Gruff Goat": 0x91,
    "Clumsy Robot": 0x92,
    "Soul Consuming Flame": 0x93,
    "Demonic Petunia": 0x94,
    "Ranboob": 0x95,
    "Li'l UFO": 0x96,
    "High-class UFO": 0x97,
    "Noose Man": 0x98,
    "Robo-pump": 0x99,
    "Plain Crocodile": 0x9a,
    "Strong Crocodile": 0x9b,
    "Hard Crocodile": 0x9c,
    "No Good Fly": 0x9d,
    "Mostly Bad Fly": 0x9e,
    "Spiteful Crow": 0x9f,
    "Loaded Dice 2": 0xC3,
    "Black Antoid (2)": 0xD1,
    "Cave Boy": 0x7B,
    "Farm Zombie": 0xde,
    "Criminal Caterpillar": 0xdf,
    "Evil Eye": 0xe0,
    "Master Criminal Worm": 0xe3
}

base_enemy_table = [
    "Insane Cultist",
    "Armored Frog",
    "Bad Buffalo",
    "Black Antoid",
    "Red Antoid",
    "Ramblin' Evil Mushroom",
    "Struttin' Evil Mushroom",
    "Mobile Sprout",
    "Tough Mobile Sprout",
    "Enraged Fire Plug",
    "Mystical Record",
    "Atomic Power Robot",
    "Nuclear Reactor Robot",
    "Guardian Hieroglyph",
    "Lethal Asp Hieroglyph",
    "Electro Swoosh",
    "Conducting Menace",
    "Conducting Spirit",
    "Evil Elemental",
    "Annoying Old Party Man",
    "Annoying Reveler",
    "Unassuming Local Guy",
    "New Age Retro Hippie",
    "Mighty Bear",
    "Mighty Bear Seven",
    "Putrid Moldyman",
    "Thunder Mite",
    "Cranky Lady",
    "Extra Cranky Lady",
    "Wetnosaur",
    "Chomposaur",
    "Gigantic Ant",
    "Scalding Coffee Cup",
    "Loaded Dice",
    "Slimy Little Pile",
    "Even Slimier Little Pile",
    "Arachnid!",
    "Arachnid!!!",
    "Bionic Kraken",
    "Spinning Robo",
    "Whirling Robo",
    "Hyper Spinning Robo",
    "Cop",
    "Coil Snake",
    "Thirsty Coil Snake",
    "Mr. Batty",
    "Elder Batty",
    "Violent Roach",
    "Filthy Attack Roach",
    "Crazed Sign",
    "Wooly Shambler",
    "Wild 'n Wooly Shambler",
    "Skate Punk",
    "Skelpion",
    "Dread Skelpion",
    "Starman",
    "Starman Super",
    "Ghost of Starman",
    "Smilin' Sphere",
    "Uncontrollable Sphere",
    "Petrified Royal Guard",
    "Final Starman",
    "Urban Zombie",
    "Zombie Possessor",
    "Zombie Dog",
    "Over Zealous Cop",
    "Territorial Oak",
    "Hostile Elder Oak",
    "Marauder Octobot",
    "Military Octobot",
    "Mechanical Octobot",
    "Ultimate Octobot",
    "Mad Duck",
    "Dali's Clock",
    "Musica",
    "Desert Wolf",
    "Big Pile of Puke",
    "Kiss of Death",
    "French Kiss of Death",
    "Foppy",
    "Fobby",
    "Zap Eel",
    "Tangoo",
    "Squatter Demon",
    "Crested Booka",
    "Great Crested Booka",
    "Lesser Mook",
    "Mook Senior",
    "Smelly Ghost",
    "Stinky Ghost",
    "Attack Slug",
    "Pit Bull Slug",
    "Rowdy Mouse",
    "Deadly Mouse",
    "Care Free Bomb",
    "Handsome Tom",
    "Smilin' Sam",
    "Manly Fish",
    "Manly Fish's Brother",
    "Runaway Dog",
    "Trick or Trick Kid",
    "Abstract Art",
    "Shattered Man",
    "Fierce Shattered Man",
    "Ego Orb",
    "Yes Man Junior",
    "Cute Li'l UFO",
    "Beautiful UFO",
    "Pogo Punk",
    "Tough Guy",
    "Mad Taxi",
    "Mr. Molecule",
    "Worthless Protoplasm",
    "Sentry Robot",
    "Psychic Psycho",
    "Major Psychic Psycho",
    "Mole Playing Rough",
    "Gruff Goat",
    "Soul Consuming Flame",
    "Demonic Petunia",
    "Ranboob",
    "Li'l UFO",
    "High-class UFO",
    "Noose Man",
    "Robo-pump",
    "Plain Crocodile",
    "Strong Crocodile",
    "Hard Crocodile",
    "No Good Fly",
    "Mostly Bad Fly",
    "Spiteful Crow",
    "Black Antoid (2)",
    "Struttin' Evil Mushroom",
    "Cave Boy",
    "Farm Zombie",
    "Criminal Caterpillar",
    "Evil Eye",
    "Master Criminal Worm",
    "Loaded Dice 2"
]

enemy_descriptions = {
    "Insane Cultist": "@They are friendly if you give them blue gifts.",
    "Armored Frog": "@Their hard shell makes them very resistant.",
    "Bad Buffalo": "@It really is a bad kind of buffalo.",
    "Black Antoid": "@Be careful not to step on him.",
    "Black Antoid (2)": "@Be careful not to step on him.",
    "Red Antoid": "@Collectors dig that bright red hue.",
    "Ramblin' Evil Mushroom": "@He is a really fun guy.",
    "Struttin' Evil Mushroom": "@Watch the spores!",
    "Mobile Sprout": "@The next evolution of plant.",
    "Tough Mobile Sprout": "@This plant is actually made of stainless steel.",
    "Enraged Fire Plug": "@A little hot-tempered.",
    "Mystical Record": "@It has all your least favorite songs.",
    "Atomic Power Robot": "@Handle with care!",
    "Nuclear Reactor Robot": "@Handle with care!",
    "Guardian Hieroglyph": "@I found him at the Pyramid north of here.",
    "Lethal Asp Hieroglyph": "@I found him at the Pyramid north of here.",
    "Electro Swoosh": "@Don't stare directly at it.",
    "Conducting Menace": "@Shield your eyes from his light.",
    "Conducting Spirit": "@Shield your eyes from his light.",
    "Evil Elemental": "@What is the element of evil?",
    "Annoying Old Party Man": "@He really knows how to throw a good party.",
    "Annoying Reveler": "@This is my friend, Dave.",
    "Unassuming Local Guy": "@What is he so unassuming about?",
    "New Age Retro Hippie": "@I like him better than the Old Age Modern Urbanite.",
    "Mighty Bear": "@He's stronger than the average bear.",
    "Mighty Bear Seven": "@I wonder what happened to two through six?",
    "Putrid Moldyman": "@I think this one's kinda cute.",
    "Thunder Mite": "@He mite rain on your parade.",
    "Cranky Lady": "@There aren't enough stores in the desert.",
    "Extra Cranky Lady": "@There aren't enough stores in the desert.",
    "Wetnosaur": "@Reminds me of a fossil I saw once.",
    "Chomposaur": "@Reminds me of a fossil I saw once.",
    "Gigantic Ant": "@No relation to the Titanic Ant.",
    "Scalding Coffee Cup": "@It's a little too hot for me.",
    "Loaded Dice": "@Always fun at parties.",
    "Even Slimier Little Pile": "@Smells worse than the Slimy Little Pile.",
    "Arachnid!": "@I think he just lives here.",
    "Arachnid!!!": "@How did it get the extra exclamation points?",
    "Bionic Kraken": "@The bionics make better soup.",
    "Spinning Robo": "@Look at it go!",
    "Whirling Robo": "@Look at it go!",
    "Hyper Spinning Robo": "@Look at it go!",
    "Cop": "@He said I wasn't paying taxes.",
    "Coil Snake": "@Not a tool for modding.",
    "Thirsty Coil Snake": "@What could he be thirsting for?",
    "Mr. Batty": "@They make for good pets if you're careful.",
    "Elder Batty": "@They make for good pets if you're careful.",
    "Violent Roach": "@They make for good pets.",
    "Filthy Attack Roach": "@They make for good pets.",
    "Crazed Sign": "@That actually seems like a pretty reasonable speed limit.",
    "Wooly Shambler": "@These are not actually Earth sheep.",
    "Wild 'n Wooly Shambler": "@These are not actually Earth sheep.",
    "Skate Punk": "@I saw him do a sick flip once.",
    "Skelpion": "@How can scorpions shoot lightning?",
    "Dread Skelpion": "@How can scorpions shoot lightning?",
    "Starman": "@Famous for their fan-made websites.",
    "Starman Super": "@My own personal sword farm.",
    "Ghost of Starman": "@Are Starmen aliens or robots, anyways?",
    "Smilin' Sphere": "@I don't like how it smiles at me.",
    "Uncontrollable Sphere": "@Fortunately, these ones are controlled",
    "Petrified Royal Guard": "@He isn't guarding this place.",
    "Final Starman": "@Watch yourself around this one.",
    "Urban Zombie": "@An import from the big city.",
    "Zombie Possessor": "@Did you hear something just now?",
    "Zombie Dog": "@He's more dog than zombie.",
    "Over Zealous Cop": "@He is overstaying his welcome.",
    "Territorial Oak": "@Don't worry, this one is just a model.",
    "Hostile Elder Oak": "@Don't worry, this one is just a model.",
    "Marauder Octobot": "@Watch out for your valuables!",
    "Military Octobot": "@Watch out for your valuables!",
    "Mechanical Octobot": "@Watch out for your valuables!",
    "Ultimate Octobot": "@Watch out for your valuables!",
    "Dali's Clock": "@I can never tell what time he's showing.",
    "Musica": "@His soothing music puts me to sleep.",
    "Desert Wolf": "@He is a surprisingly good pet.",
    "Big Pile of Puke": "@How did this one get in here?",
    "Kiss of Death": "@Despite the name, I wouldn't recommend kissing it.",
    "French Kiss of Death": "@Despite the name, I wouldn't recommend kissing it.",
    "Foppy": "@I can't even tell what this thing is.",
    "Fobby": "@I wonder what color they are?",
    "Zap Eel": "@How can eels live on land, anyway?",
    "Tangoo": "@Watch out for his poisonous breath.",
    "Squatter Demon": "@I don't know what to say about this one.",
    "Crested Booka": "@The classic desert animal.",
    "Great Crested Booka": "@The classic desert animal.",
    "Lesser Mook": "@These aliens live here.",
    "Mook Senior": "@These aliens live here.",
    "Smelly Ghost": "@This exhibit needs some air freshener.",
    "Stinky Ghost": "@This exhibit needs some air freshener.",
    "Attack Slug": "@Cute when alone.",
    "Pit Bull Slug": "@It is neither pit bull nor slug.",
    "Rowdy Mouse": "@They're good pets if you don't let them SMAAAASH you.",
    "Deadly Mouse": "@They're good pets if you don't let them SMAAAASH you.",
    "Care Free Bomb": "@Don't get too close!",
    "Handsome Tom": "@Not really all that handsome.",
    "Smilin' Sam": "@He usually doesn't smile.",
    "Manly Fish": "@Not related to Manly Fish's Brother.",
    "Manly Fish's Brother": "@They are not actually related.",
    "Runaway Dog": "@Don't worry, this one is adopted.",
    "Trick or Trick Kid": "@He likes to play Clique.",
    "Cave Boy": "@Not quite a Cave Man.",
    "Abstract Art": "@Looks good in any gallery.",
    "Shattered Man": "@He doesn't look so shattered to me.",
    "Fierce Shattered Man": "@He doesn't look so shattered to me.",
    "Ego Orb": "@I'll get back to you on that one.",
    "Yes Man Junior": "@Not that bad of a guy.",
    "Cute Li'l UFO": "@The ribbon is actually biological.",
    "Beautiful UFO": "@Personally, I'm a bigger fan of the Li'l UFO.",
    "Pogo Punk": "@He knows some sick tricks.",
    "Tough Guy": "@Likes to chew gum and kick butt.",
    "Mad Taxi": "@It has surprisingly good mental health.",
    "Mr. Molecule": "@His whole family is here.",
    "Worthless Protoplasm": "@He's actually kind of worthwhile.",
    "Sentry Robot": "@Built by a crafty engineer.",
    "Psychic Psycho": "@Watch out for Fire attacks!",
    "Major Psychic Psycho": "@Watch out for Fire attacks!",
    "Mole Playing Rough": "@They like to show up in the most random places.",
    "Soul Consuming Flame": "@This one can't affect me.",
    "Demonic Petunia": "@Looks beautiful from a distance.",
    "Ranboob": "@Yeah I've got nothing to say on this one.",
    "Li'l UFO": "@Personally, I'm a bigger fan of the High-class UFO.",
    "High-class UFO": "@Personally, I'm a bigger fan of the Beautiful UFO.",
    "Noose Man": "@How was this approved for a family game?",
    "Robo-pump": "@It causes fires more than it puts them out.",
    "Plain Crocodile": "@Also known as the vanilla crocodile.",
    "Strong Crocodile": "@Stronger than the weak crocodile",
    "Hard Crocodile": "@Slightly harder than the soft crocodile.",
    "No Good Fly": "@They are often mistaken for bees.",
    "Mostly Bad Fly": "@He's not all bad.",
    "Spiteful Crow": "@Keep your valuables in your pocket!",
    "Farm Zombie": "@Easily subdued by plants.",
    "Criminal Caterpillar": "@He is wanted in seventeen countries for his crimes.",
    "Evil Eye": "@Third-year staring contest champion.",
    "Master Criminal Worm": "@He is wanted in seventeen countries for his crimes.",
    "Loaded Dice 2": "@Always dangerous at parties.",
}

can_walkthrough = [
    0x0045,
    0x004A,
    0x0065,
    0x00C3,
    0x0112,
    0x0114,
    0x0115,
    0x0116,
    0x0117,
    0x0118,
    0x011A,
    0x011B,
    0x011C,
    0x011D,
    0x011E,
    0x011F,
    0x0120,
    0x0123,
    0x0124,
    0x012D,
    0x012E,
    0x012F,
    0x0130,
    0x0131,
    0x0132,
    0x0133,
    0x0134,
    0x0135,
    0x0136,
    0x0139,
    0x013A,
    0x013B,
    0x013C,
    0x013D,
    0x013E,
    0x013F,
    0x0140,
    0x0142,
    0x0143,
    0x0144,
    0x0145,
    0x0146,
    0x0169,
    0x0182,
    0x0185,
    0x0186,
    0x0187,
    0x0188,
    0x019F,
    0x01A0,
    0x01A1,
    0x01BC,
    0x01CD
]


def shuffle_enemies(world: "EarthBoundWorld") -> None:
    """Shuffles the global enemy table."""
    world.acting_enemy_list = {}
    shuffled_enemies = base_enemy_table.copy()
    if world.options.enemy_shuffle:
        world.random.shuffle(shuffled_enemies)
    for index, enemy in enumerate(shuffled_enemies):
        world.acting_enemy_list[base_enemy_table[index]] = enemy


def apply_enemy_shuffle(world: "EarthBoundWorld", rom: "LocalRom") -> None:
    """Writes the shuffled enemy table into ROM."""
    rom.write_bytes(0x10d54d, bytearray([enemy_ids[world.acting_enemy_list["Spiteful Crow"]]]))
    rom.write_bytes(0x10d551, bytearray([enemy_ids[world.acting_enemy_list["Runaway Dog"]]]))
    rom.write_bytes(0x10d555, bytearray([enemy_ids[world.acting_enemy_list["Coil Snake"]]]))
    rom.write_bytes(0x10d559, bytearray([enemy_ids[world.acting_enemy_list["Ghost of Starman"]]]))
    rom.write_bytes(0x10d55c, bytearray([enemy_ids[world.acting_enemy_list["Evil Eye"]]]))
    rom.write_bytes(0x10d567, bytearray([enemy_ids[world.acting_enemy_list["Evil Eye"]]]))
    rom.write_bytes(0x10d56a, bytearray([enemy_ids[world.acting_enemy_list["Mechanical Octobot"]]]))
    rom.write_bytes(0x10d56e, bytearray([enemy_ids[world.acting_enemy_list["Ghost of Starman"]]]))
    rom.write_bytes(0x10d571, bytearray([enemy_ids[world.acting_enemy_list["Mechanical Octobot"]]]))
    rom.write_bytes(0x10d574, bytearray([enemy_ids[world.acting_enemy_list["Evil Eye"]]]))
    rom.write_bytes(0x10d578, bytearray([enemy_ids[world.acting_enemy_list["Skate Punk"]]]))
    rom.write_bytes(0x10d57b, bytearray([enemy_ids[world.acting_enemy_list["Yes Man Junior"]]]))
    rom.write_bytes(0x10d57e, bytearray([enemy_ids[world.acting_enemy_list["Pogo Punk"]]]))
    rom.write_bytes(0x10d582, bytearray([enemy_ids[world.acting_enemy_list["Skate Punk"]]]))
    rom.write_bytes(0x10d585, bytearray([enemy_ids[world.acting_enemy_list["Pogo Punk"]]]))
    rom.write_bytes(0x10d588, bytearray([enemy_ids[world.acting_enemy_list["Yes Man Junior"]]]))
    rom.write_bytes(0x10d58c, bytearray([enemy_ids[world.acting_enemy_list["Pogo Punk"]]]))
    rom.write_bytes(0x10d58f, bytearray([enemy_ids[world.acting_enemy_list["Yes Man Junior"]]]))
    rom.write_bytes(0x10d593, bytearray([enemy_ids[world.acting_enemy_list["Skate Punk"]]]))
    rom.write_bytes(0x10d596, bytearray([enemy_ids[world.acting_enemy_list["Yes Man Junior"]]]))
    rom.write_bytes(0x10d599, bytearray([enemy_ids[world.acting_enemy_list["Pogo Punk"]]]))
    rom.write_bytes(0x10d5a1, bytearray([enemy_ids[world.acting_enemy_list["Spiteful Crow"]]]))
    rom.write_bytes(0x10d5a9, bytearray([enemy_ids[world.acting_enemy_list["Lesser Mook"]]]))
    rom.write_bytes(0x10d5ac, bytearray([enemy_ids[world.acting_enemy_list["Whirling Robo"]]]))
    rom.write_bytes(0x10d5b0, bytearray([enemy_ids[world.acting_enemy_list["Lesser Mook"]]]))
    rom.write_bytes(0x10d5b3, bytearray([enemy_ids[world.acting_enemy_list["Wooly Shambler"]]]))
    rom.write_bytes(0x10d5b7, bytearray([enemy_ids[world.acting_enemy_list["Wooly Shambler"]]]))
    rom.write_bytes(0x10d5ba, bytearray([enemy_ids[world.acting_enemy_list["Whirling Robo"]]]))
    rom.write_bytes(0x10d5be, bytearray([enemy_ids[world.acting_enemy_list["Lesser Mook"]]]))
    rom.write_bytes(0x10d5c1, bytearray([enemy_ids[world.acting_enemy_list["Whirling Robo"]]]))
    rom.write_bytes(0x10d5c4, bytearray([enemy_ids[world.acting_enemy_list["Wooly Shambler"]]]))
    rom.write_bytes(0x10d5c8, bytearray([enemy_ids[world.acting_enemy_list["Spiteful Crow"]]]))
    rom.write_bytes(0x10d5cc, bytearray([enemy_ids[world.acting_enemy_list["Gruff Goat"]]]))
    rom.write_bytes(0x10d5d4, bytearray([enemy_ids[world.acting_enemy_list["Lesser Mook"]]]))
    rom.write_bytes(0x10d5d7, bytearray([enemy_ids[world.acting_enemy_list["Whirling Robo"]]]))
    rom.write_bytes(0x10d5db, bytearray([enemy_ids[world.acting_enemy_list["Lesser Mook"]]]))
    rom.write_bytes(0x10d5de, bytearray([enemy_ids[world.acting_enemy_list["Wooly Shambler"]]]))
    rom.write_bytes(0x10d5e2, bytearray([enemy_ids[world.acting_enemy_list["Wooly Shambler"]]]))
    rom.write_bytes(0x10d5e5, bytearray([enemy_ids[world.acting_enemy_list["Whirling Robo"]]]))
    rom.write_bytes(0x10d5e9, bytearray([enemy_ids[world.acting_enemy_list["Lesser Mook"]]]))
    rom.write_bytes(0x10d5ec, bytearray([enemy_ids[world.acting_enemy_list["Wooly Shambler"]]]))
    rom.write_bytes(0x10d5ef, bytearray([enemy_ids[world.acting_enemy_list["Whirling Robo"]]]))
    rom.write_bytes(0x10d5f7, bytearray([enemy_ids[world.acting_enemy_list["Cave Boy"]]]))
    rom.write_bytes(0x10d5fa, bytearray([enemy_ids[world.acting_enemy_list["Mighty Bear Seven"]]]))
    rom.write_bytes(0x10d5fe, bytearray([enemy_ids[world.acting_enemy_list["Cave Boy"]]]))
    rom.write_bytes(0x10d601, bytearray([enemy_ids[world.acting_enemy_list["Mighty Bear Seven"]]]))
    rom.write_bytes(0x10d605, bytearray([enemy_ids[world.acting_enemy_list["Cave Boy"]]]))
    rom.write_bytes(0x10d608, bytearray([enemy_ids[world.acting_enemy_list["Mighty Bear Seven"]]]))
    rom.write_bytes(0x10d60c, bytearray([enemy_ids[world.acting_enemy_list["Black Antoid"]]]))
    rom.write_bytes(0x10d610, bytearray([enemy_ids[world.acting_enemy_list["Ramblin' Evil Mushroom"]]]))
    rom.write_bytes(0x10d614, bytearray([enemy_ids[world.acting_enemy_list["Ramblin' Evil Mushroom"]]]))
    rom.write_bytes(0x10d618, bytearray([enemy_ids[world.acting_enemy_list["Black Antoid"]]]))
    rom.write_bytes(0x10d61b, bytearray([enemy_ids[world.acting_enemy_list["Ramblin' Evil Mushroom"]]]))
    rom.write_bytes(0x10d61f, bytearray([enemy_ids[world.acting_enemy_list["Ramblin' Evil Mushroom"]]]))
    rom.write_bytes(0x10d623, bytearray([enemy_ids[world.acting_enemy_list["Ramblin' Evil Mushroom"]]]))
    rom.write_bytes(0x10d627, bytearray([enemy_ids[world.acting_enemy_list["Runaway Dog"]]]))
    rom.write_bytes(0x10d62a, bytearray([enemy_ids[world.acting_enemy_list["Cop"]]]))
    rom.write_bytes(0x10d62e, bytearray([enemy_ids[world.acting_enemy_list["Cranky Lady"]]]))
    rom.write_bytes(0x10d632, bytearray([enemy_ids[world.acting_enemy_list["Annoying Old Party Man"]]]))
    rom.write_bytes(0x10d636, bytearray([enemy_ids[world.acting_enemy_list["Unassuming Local Guy"]]]))
    rom.write_bytes(0x10d63a, bytearray([enemy_ids[world.acting_enemy_list["New Age Retro Hippie"]]]))
    rom.write_bytes(0x10d63e, bytearray([enemy_ids[world.acting_enemy_list["Ramblin' Evil Mushroom"]]]))
    rom.write_bytes(0x10d641, bytearray([enemy_ids[world.acting_enemy_list["Mobile Sprout"]]]))
    rom.write_bytes(0x10d645, bytearray([enemy_ids[world.acting_enemy_list["Ramblin' Evil Mushroom"]]]))
    rom.write_bytes(0x10d649, bytearray([enemy_ids[world.acting_enemy_list["Mobile Sprout"]]]))
    rom.write_bytes(0x10d64c, bytearray([enemy_ids[world.acting_enemy_list["Territorial Oak"]]]))
    rom.write_bytes(0x10d650, bytearray([enemy_ids[world.acting_enemy_list["Mobile Sprout"]]]))
    rom.write_bytes(0x10d653, bytearray([enemy_ids[world.acting_enemy_list["Territorial Oak"]]]))
    rom.write_bytes(0x10d657, bytearray([enemy_ids[world.acting_enemy_list["Mobile Sprout"]]]))
    rom.write_bytes(0x10d65a, bytearray([enemy_ids[world.acting_enemy_list["Li'l UFO"]]]))
    rom.write_bytes(0x10d65e, bytearray([enemy_ids[world.acting_enemy_list["Mobile Sprout"]]]))
    rom.write_bytes(0x10d662, bytearray([enemy_ids[world.acting_enemy_list["Mobile Sprout"]]]))
    rom.write_bytes(0x10d666, bytearray([enemy_ids[world.acting_enemy_list["Territorial Oak"]]]))
    rom.write_bytes(0x10d66a, bytearray([enemy_ids[world.acting_enemy_list["Spinning Robo"]]]))
    rom.write_bytes(0x10d66e, bytearray([enemy_ids[world.acting_enemy_list["Li'l UFO"]]]))
    rom.write_bytes(0x10d672, bytearray([enemy_ids[world.acting_enemy_list["Li'l UFO"]]]))
    rom.write_bytes(0x10d675, bytearray([enemy_ids[world.acting_enemy_list["Mobile Sprout"]]]))
    rom.write_bytes(0x10d679, bytearray([enemy_ids[world.acting_enemy_list["Li'l UFO"]]]))
    rom.write_bytes(0x10d67c, bytearray([enemy_ids[world.acting_enemy_list["Spinning Robo"]]]))
    rom.write_bytes(0x10d680, bytearray([enemy_ids[world.acting_enemy_list["Li'l UFO"]]]))
    rom.write_bytes(0x10d684, bytearray([enemy_ids[world.acting_enemy_list["Insane Cultist"]]]))
    rom.write_bytes(0x10d688, bytearray([enemy_ids[world.acting_enemy_list["Insane Cultist"]]]))
    rom.write_bytes(0x10d68c, bytearray([enemy_ids[world.acting_enemy_list["Spiteful Crow"]]]))
    rom.write_bytes(0x10d690, bytearray([enemy_ids[world.acting_enemy_list["Spiteful Crow"]]]))
    rom.write_bytes(0x10d694, bytearray([enemy_ids[world.acting_enemy_list["Cranky Lady"]]]))
    rom.write_bytes(0x10d698, bytearray([enemy_ids[world.acting_enemy_list["Annoying Old Party Man"]]]))
    rom.write_bytes(0x10d69c, bytearray([enemy_ids[world.acting_enemy_list["New Age Retro Hippie"]]]))
    rom.write_bytes(0x10d6a0, bytearray([enemy_ids[world.acting_enemy_list["Trick or Trick Kid"]]]))
    rom.write_bytes(0x10d6a3, bytearray([enemy_ids[world.acting_enemy_list["Handsome Tom"]]]))
    rom.write_bytes(0x10d6a7, bytearray([enemy_ids[world.acting_enemy_list["Trick or Trick Kid"]]]))
    rom.write_bytes(0x10d6ab, bytearray([enemy_ids[world.acting_enemy_list["Handsome Tom"]]]))
    rom.write_bytes(0x10d6ae, bytearray([enemy_ids[world.acting_enemy_list["Smilin' Sam"]]]))
    rom.write_bytes(0x10d6b2, bytearray([enemy_ids[world.acting_enemy_list["Handsome Tom"]]]))
    rom.write_bytes(0x10d6b6, bytearray([enemy_ids[world.acting_enemy_list["Smilin' Sam"]]]))
    rom.write_bytes(0x10d6ba, bytearray([enemy_ids[world.acting_enemy_list["Urban Zombie"]]]))
    rom.write_bytes(0x10d6be, bytearray([enemy_ids[world.acting_enemy_list["Zombie Possessor"]]]))
    rom.write_bytes(0x10d6c1, bytearray([enemy_ids[world.acting_enemy_list["Urban Zombie"]]]))
    rom.write_bytes(0x10d6c5, bytearray([enemy_ids[world.acting_enemy_list["No Good Fly"]]]))
    rom.write_bytes(0x10d6c8, bytearray([enemy_ids[world.acting_enemy_list["Putrid Moldyman"]]]))
    rom.write_bytes(0x10d6cc, bytearray([enemy_ids[world.acting_enemy_list["Putrid Moldyman"]]]))
    rom.write_bytes(0x10d6cf, bytearray([enemy_ids[world.acting_enemy_list["Smelly Ghost"]]]))
    rom.write_bytes(0x10d6d3, bytearray([enemy_ids[world.acting_enemy_list["Zombie Possessor"]]]))
    rom.write_bytes(0x10d6d6, bytearray([enemy_ids[world.acting_enemy_list["Putrid Moldyman"]]]))
    rom.write_bytes(0x10d6da, bytearray([enemy_ids[world.acting_enemy_list["Zombie Possessor"]]]))
    rom.write_bytes(0x10d6dd, bytearray([enemy_ids[world.acting_enemy_list["Smelly Ghost"]]]))
    rom.write_bytes(0x10d6e1, bytearray([enemy_ids[world.acting_enemy_list["Putrid Moldyman"]]]))
    rom.write_bytes(0x10d6e4, bytearray([enemy_ids[world.acting_enemy_list["Smelly Ghost"]]]))
    rom.write_bytes(0x10d6e8, bytearray([enemy_ids[world.acting_enemy_list["No Good Fly"]]]))
    rom.write_bytes(0x10d6eb, bytearray([enemy_ids[world.acting_enemy_list["Putrid Moldyman"]]]))
    rom.write_bytes(0x10d6ef, bytearray([enemy_ids[world.acting_enemy_list["No Good Fly"]]]))
    rom.write_bytes(0x10d6f2, bytearray([enemy_ids[world.acting_enemy_list["Smelly Ghost"]]]))
    rom.write_bytes(0x10d6f6, bytearray([enemy_ids[world.acting_enemy_list["No Good Fly"]]]))
    rom.write_bytes(0x10d6fa, bytearray([enemy_ids[world.acting_enemy_list["Zombie Dog"]]]))
    rom.write_bytes(0x10d6fe, bytearray([enemy_ids[world.acting_enemy_list["Zombie Dog"]]]))
    rom.write_bytes(0x10d701, bytearray([enemy_ids[world.acting_enemy_list["No Good Fly"]]]))
    rom.write_bytes(0x10d705, bytearray([enemy_ids[world.acting_enemy_list["Red Antoid"]]]))
    rom.write_bytes(0x10d70c, bytearray([enemy_ids[world.acting_enemy_list["Red Antoid"]]]))
    rom.write_bytes(0x10d713, bytearray([enemy_ids[world.acting_enemy_list["Red Antoid"]]]))
    rom.write_bytes(0x10d716, bytearray([enemy_ids[world.acting_enemy_list["Armored Frog"]]]))
    rom.write_bytes(0x10d719, bytearray([enemy_ids[world.acting_enemy_list["Farm Zombie"]]]))
    rom.write_bytes(0x10d71d, bytearray([enemy_ids[world.acting_enemy_list["Red Antoid"]]]))
    rom.write_bytes(0x10d720, bytearray([enemy_ids[world.acting_enemy_list["Armored Frog"]]]))
    rom.write_bytes(0x10d724, bytearray([enemy_ids[world.acting_enemy_list["Red Antoid"]]]))
    rom.write_bytes(0x10d727, bytearray([enemy_ids[world.acting_enemy_list["Armored Frog"]]]))
    rom.write_bytes(0x10d72b, bytearray([enemy_ids[world.acting_enemy_list["Red Antoid"]]]))
    rom.write_bytes(0x10d72e, bytearray([enemy_ids[world.acting_enemy_list["Farm Zombie"]]]))
    rom.write_bytes(0x10d732, bytearray([enemy_ids[world.acting_enemy_list["Armored Frog"]]]))
    rom.write_bytes(0x10d735, bytearray([enemy_ids[world.acting_enemy_list["Farm Zombie"]]]))
    rom.write_bytes(0x10d739, bytearray([enemy_ids[world.acting_enemy_list["Armored Frog"]]]))
    rom.write_bytes(0x10d73d, bytearray([enemy_ids[world.acting_enemy_list["Armored Frog"]]]))
    rom.write_bytes(0x10d740, bytearray([enemy_ids[world.acting_enemy_list["Farm Zombie"]]]))
    rom.write_bytes(0x10d744, bytearray([enemy_ids[world.acting_enemy_list["Plain Crocodile"]]]))
    rom.write_bytes(0x10d747, bytearray([enemy_ids[world.acting_enemy_list["Red Antoid"]]]))
    rom.write_bytes(0x10d74b, bytearray([enemy_ids[world.acting_enemy_list["Plain Crocodile"]]]))
    rom.write_bytes(0x10d74e, bytearray([enemy_ids[world.acting_enemy_list["Armored Frog"]]]))
    rom.write_bytes(0x10d751, bytearray([enemy_ids[world.acting_enemy_list["Farm Zombie"]]]))
    rom.write_bytes(0x10d755, bytearray([enemy_ids[world.acting_enemy_list["Plain Crocodile"]]]))
    rom.write_bytes(0x10d758, bytearray([enemy_ids[world.acting_enemy_list["Farm Zombie"]]]))
    rom.write_bytes(0x10d75c, bytearray([enemy_ids[world.acting_enemy_list["Plain Crocodile"]]]))
    rom.write_bytes(0x10d75f, bytearray([enemy_ids[world.acting_enemy_list["Farm Zombie"]]]))
    rom.write_bytes(0x10d763, bytearray([enemy_ids[world.acting_enemy_list["Red Antoid"]]]))
    rom.write_bytes(0x10d769, bytearray([enemy_ids[world.acting_enemy_list["Armored Frog"]]]))
    rom.write_bytes(0x10d76d, bytearray([enemy_ids[world.acting_enemy_list["Red Antoid"]]]))
    rom.write_bytes(0x10d770, bytearray([enemy_ids[world.acting_enemy_list["Black Antoid (2)"]]]))
    rom.write_bytes(0x10d766, bytearray([enemy_ids[world.acting_enemy_list["Black Antoid (2)"]]]))
    rom.write_bytes(0x10d774, bytearray([enemy_ids[world.acting_enemy_list["Red Antoid"]]]))
    rom.write_bytes(0x10d777, bytearray([enemy_ids[world.acting_enemy_list["Black Antoid (2)"]]]))
    rom.write_bytes(0x10d77b, bytearray([enemy_ids[world.acting_enemy_list["Red Antoid"]]]))
    rom.write_bytes(0x10d77e, bytearray([enemy_ids[world.acting_enemy_list["Armored Frog"]]]))
    rom.write_bytes(0x10d781, bytearray([enemy_ids[world.acting_enemy_list["Plain Crocodile"]]]))
    rom.write_bytes(0x10d785, bytearray([enemy_ids[world.acting_enemy_list["Red Antoid"]]]))
    rom.write_bytes(0x10d788, bytearray([enemy_ids[world.acting_enemy_list["Armored Frog"]]]))
    rom.write_bytes(0x10d78c, bytearray([enemy_ids[world.acting_enemy_list["Red Antoid"]]]))
    rom.write_bytes(0x10d78f, bytearray([enemy_ids[world.acting_enemy_list["Plain Crocodile"]]]))
    rom.write_bytes(0x10d793, bytearray([enemy_ids[world.acting_enemy_list["Red Antoid"]]]))
    rom.write_bytes(0x10d796, bytearray([enemy_ids[world.acting_enemy_list["Plain Crocodile"]]]))
    rom.write_bytes(0x10d79a, bytearray([enemy_ids[world.acting_enemy_list["Red Antoid"]]]))
    rom.write_bytes(0x10d79d, bytearray([enemy_ids[world.acting_enemy_list["Armored Frog"]]]))
    rom.write_bytes(0x10d7a1, bytearray([enemy_ids[world.acting_enemy_list["Armored Frog"]]]))
    rom.write_bytes(0x10d7a5, bytearray([enemy_ids[world.acting_enemy_list["Armored Frog"]]]))
    rom.write_bytes(0x10d7a9, bytearray([enemy_ids[world.acting_enemy_list["Plain Crocodile"]]]))
    rom.write_bytes(0x10d7ac, bytearray([enemy_ids[world.acting_enemy_list["Armored Frog"]]]))
    rom.write_bytes(0x10d7b0, bytearray([enemy_ids[world.acting_enemy_list["Plain Crocodile"]]]))
    rom.write_bytes(0x10d7b4, bytearray([enemy_ids[world.acting_enemy_list["Mad Duck"]]]))
    rom.write_bytes(0x10d7b8, bytearray([enemy_ids[world.acting_enemy_list["Violent Roach"]]]))
    rom.write_bytes(0x10d7bc, bytearray([enemy_ids[world.acting_enemy_list["Ranboob"]]]))
    rom.write_bytes(0x10d7c0, bytearray([enemy_ids[world.acting_enemy_list["Tough Mobile Sprout"]]]))
    rom.write_bytes(0x10d7c3, bytearray([enemy_ids[world.acting_enemy_list["Ranboob"]]]))
    rom.write_bytes(0x10d7c7, bytearray([enemy_ids[world.acting_enemy_list["Tough Mobile Sprout"]]]))
    rom.write_bytes(0x10d7cb, bytearray([enemy_ids[world.acting_enemy_list["Tough Mobile Sprout"]]]))
    rom.write_bytes(0x10d7ce, bytearray([enemy_ids[world.acting_enemy_list["Struttin' Evil Mushroom"]]]))
    rom.write_bytes(0x10d7d1, bytearray([enemy_ids[world.acting_enemy_list["Ranboob"]]]))
    rom.write_bytes(0x10d7d5, bytearray([enemy_ids[world.acting_enemy_list["Bad Buffalo"]]]))
    rom.write_bytes(0x10d7d8, bytearray([enemy_ids[world.acting_enemy_list["Desert Wolf"]]]))
    rom.write_bytes(0x10d7dc, bytearray([enemy_ids[world.acting_enemy_list["Bad Buffalo"]]]))
    rom.write_bytes(0x10d7df, bytearray([enemy_ids[world.acting_enemy_list["Smilin' Sphere"]]]))
    rom.write_bytes(0x10d7e3, bytearray([enemy_ids[world.acting_enemy_list["Bad Buffalo"]]]))
    rom.write_bytes(0x10d7e7, bytearray([enemy_ids[world.acting_enemy_list["Desert Wolf"]]]))
    rom.write_bytes(0x10d7eb, bytearray([enemy_ids[world.acting_enemy_list["Skelpion"]]]))
    rom.write_bytes(0x10d7ee, bytearray([enemy_ids[world.acting_enemy_list["Cute Li'l UFO"]]]))
    rom.write_bytes(0x10d7f2, bytearray([enemy_ids[world.acting_enemy_list["Skelpion"]]]))
    rom.write_bytes(0x10d7f5, bytearray([enemy_ids[world.acting_enemy_list["Smilin' Sphere"]]]))
    rom.write_bytes(0x10d7f9, bytearray([enemy_ids[world.acting_enemy_list["Skelpion"]]]))
    rom.write_bytes(0x10d7fc, bytearray([enemy_ids[world.acting_enemy_list["Smilin' Sphere"]]]))
    rom.write_bytes(0x10d7ff, bytearray([enemy_ids[world.acting_enemy_list["Cute Li'l UFO"]]]))
    rom.write_bytes(0x10d803, bytearray([enemy_ids[world.acting_enemy_list["Skelpion"]]]))
    rom.write_bytes(0x10d806, bytearray([enemy_ids[world.acting_enemy_list["Crested Booka"]]]))
    rom.write_bytes(0x10d80a, bytearray([enemy_ids[world.acting_enemy_list["Skelpion"]]]))
    rom.write_bytes(0x10d80e, bytearray([enemy_ids[world.acting_enemy_list["Skelpion"]]]))
    rom.write_bytes(0x10d812, bytearray([enemy_ids[world.acting_enemy_list["Crested Booka"]]]))
    rom.write_bytes(0x10d815, bytearray([enemy_ids[world.acting_enemy_list["Bad Buffalo"]]]))
    rom.write_bytes(0x10d819, bytearray([enemy_ids[world.acting_enemy_list["Crested Booka"]]]))
    rom.write_bytes(0x10d81c, bytearray([enemy_ids[world.acting_enemy_list["Desert Wolf"]]]))
    rom.write_bytes(0x10d820, bytearray([enemy_ids[world.acting_enemy_list["Crested Booka"]]]))
    rom.write_bytes(0x10d823, bytearray([enemy_ids[world.acting_enemy_list["Cute Li'l UFO"]]]))
    rom.write_bytes(0x10d826, bytearray([enemy_ids[world.acting_enemy_list["Smilin' Sphere"]]]))
    rom.write_bytes(0x10d82a, bytearray([enemy_ids[world.acting_enemy_list["Crested Booka"]]]))
    rom.write_bytes(0x10d82d, bytearray([enemy_ids[world.acting_enemy_list["Cute Li'l UFO"]]]))
    rom.write_bytes(0x10d831, bytearray([enemy_ids[world.acting_enemy_list["Crested Booka"]]]))
    rom.write_bytes(0x10d834, bytearray([enemy_ids[world.acting_enemy_list["Smilin' Sphere"]]]))
    rom.write_bytes(0x10d838, bytearray([enemy_ids[world.acting_enemy_list["Mad Taxi"]]]))
    rom.write_bytes(0x10d83c, bytearray([enemy_ids[world.acting_enemy_list["Extra Cranky Lady"]]]))
    rom.write_bytes(0x10d840, bytearray([enemy_ids[world.acting_enemy_list["Annoying Reveler"]]]))
    rom.write_bytes(0x10d844, bytearray([enemy_ids[world.acting_enemy_list["Crazed Sign"]]]))
    rom.write_bytes(0x10d848, bytearray([enemy_ids[world.acting_enemy_list["Dali's Clock"]]]))
    rom.write_bytes(0x10d84c, bytearray([enemy_ids[world.acting_enemy_list["Enraged Fire Plug"]]]))
    rom.write_bytes(0x10d850, bytearray([enemy_ids[world.acting_enemy_list["Enraged Fire Plug"]]]))
    rom.write_bytes(0x10d854, bytearray([enemy_ids[world.acting_enemy_list["Abstract Art"]]]))
    rom.write_bytes(0x10d858, bytearray([enemy_ids[world.acting_enemy_list["Robo-pump"]]]))
    rom.write_bytes(0x10d85c, bytearray([enemy_ids[world.acting_enemy_list["Robo-pump"]]]))
    rom.write_bytes(0x10d85f, bytearray([enemy_ids[world.acting_enemy_list["Enraged Fire Plug"]]]))
    rom.write_bytes(0x10d863, bytearray([enemy_ids[world.acting_enemy_list["Mad Taxi"]]]))
    rom.write_bytes(0x10d867, bytearray([enemy_ids[world.acting_enemy_list["Mad Taxi"]]]))
    rom.write_bytes(0x10d86a, bytearray([enemy_ids[world.acting_enemy_list["Crazed Sign"]]]))
    rom.write_bytes(0x10d86e, bytearray([enemy_ids[world.acting_enemy_list["Crazed Sign"]]]))
    rom.write_bytes(0x10d872, bytearray([enemy_ids[world.acting_enemy_list["Tough Guy"]]]))
    rom.write_bytes(0x10d876, bytearray([enemy_ids[world.acting_enemy_list["Over Zealous Cop"]]]))
    rom.write_bytes(0x10d879, bytearray([enemy_ids[world.acting_enemy_list["Tough Guy"]]]))
    rom.write_bytes(0x10d87d, bytearray([enemy_ids[world.acting_enemy_list["Over Zealous Cop"]]]))
    rom.write_bytes(0x10d881, bytearray([enemy_ids[world.acting_enemy_list["High-class UFO"]]]))
    rom.write_bytes(0x10d884, bytearray([enemy_ids[world.acting_enemy_list["Beautiful UFO"]]]))
    rom.write_bytes(0x10d888, bytearray([enemy_ids[world.acting_enemy_list["High-class UFO"]]]))
    rom.write_bytes(0x10d88c, bytearray([enemy_ids[world.acting_enemy_list["High-class UFO"]]]))
    rom.write_bytes(0x10d890, bytearray([enemy_ids[world.acting_enemy_list["Beautiful UFO"]]]))
    rom.write_bytes(0x10d894, bytearray([enemy_ids[world.acting_enemy_list["Dread Skelpion"]]]))
    rom.write_bytes(0x10d897, bytearray([enemy_ids[world.acting_enemy_list["Great Crested Booka"]]]))
    rom.write_bytes(0x10d89b, bytearray([enemy_ids[world.acting_enemy_list["Dread Skelpion"]]]))
    rom.write_bytes(0x10d89f, bytearray([enemy_ids[world.acting_enemy_list["Great Crested Booka"]]]))
    rom.write_bytes(0x10d8a3, bytearray([enemy_ids[world.acting_enemy_list["Great Crested Booka"]]]))
    rom.write_bytes(0x10d8a6, bytearray([enemy_ids[world.acting_enemy_list["Dread Skelpion"]]]))
    rom.write_bytes(0x10d8aa, bytearray([enemy_ids[world.acting_enemy_list["Great Crested Booka"]]]))
    rom.write_bytes(0x10d8ae, bytearray([enemy_ids[world.acting_enemy_list["High-class UFO"]]]))
    rom.write_bytes(0x10d8b1, bytearray([enemy_ids[world.acting_enemy_list["Beautiful UFO"]]]))
    rom.write_bytes(0x10d8b5, bytearray([enemy_ids[world.acting_enemy_list["High-class UFO"]]]))
    rom.write_bytes(0x10d8b8, bytearray([enemy_ids[world.acting_enemy_list["Marauder Octobot"]]]))
    rom.write_bytes(0x10d8bb, bytearray([enemy_ids[world.acting_enemy_list["Beautiful UFO"]]]))
    rom.write_bytes(0x10d8bf, bytearray([enemy_ids[world.acting_enemy_list["High-class UFO"]]]))
    rom.write_bytes(0x10d8c2, bytearray([enemy_ids[world.acting_enemy_list["Marauder Octobot"]]]))
    rom.write_bytes(0x10d8c6, bytearray([enemy_ids[world.acting_enemy_list["Beautiful UFO"]]]))
    rom.write_bytes(0x10d8ca, bytearray([enemy_ids[world.acting_enemy_list["Marauder Octobot"]]]))
    rom.write_bytes(0x10d8ce, bytearray([enemy_ids[world.acting_enemy_list["Hostile Elder Oak"]]]))
    rom.write_bytes(0x10d8d2, bytearray([enemy_ids[world.acting_enemy_list["Pit Bull Slug"]]]))
    rom.write_bytes(0x10d8d6, bytearray([enemy_ids[world.acting_enemy_list["Demonic Petunia"]]]))
    rom.write_bytes(0x10d8da, bytearray([enemy_ids[world.acting_enemy_list["Big Pile of Puke"]]]))
    rom.write_bytes(0x10d8dd, bytearray([enemy_ids[world.acting_enemy_list["Even Slimier Little Pile"]]]))
    rom.write_bytes(0x10d8e1, bytearray([enemy_ids[world.acting_enemy_list["Big Pile of Puke"]]]))
    rom.write_bytes(0x10d8e4, bytearray([enemy_ids[world.acting_enemy_list["Even Slimier Little Pile"]]]))
    rom.write_bytes(0x10d8e8, bytearray([enemy_ids[world.acting_enemy_list["Hostile Elder Oak"]]]))
    rom.write_bytes(0x10d8ec, bytearray([enemy_ids[world.acting_enemy_list["Zap Eel"]]]))
    rom.write_bytes(0x10d8ef, bytearray([enemy_ids[world.acting_enemy_list["Hard Crocodile"]]]))
    rom.write_bytes(0x10d8f3, bytearray([enemy_ids[world.acting_enemy_list["Zap Eel"]]]))
    rom.write_bytes(0x10d8f7, bytearray([enemy_ids[world.acting_enemy_list["Even Slimier Little Pile"]]]))
    rom.write_bytes(0x10d8fa, bytearray([enemy_ids[world.acting_enemy_list["Zap Eel"]]]))
    rom.write_bytes(0x10d8fe, bytearray([enemy_ids[world.acting_enemy_list["Even Slimier Little Pile"]]]))
    rom.write_bytes(0x10d901, bytearray([enemy_ids[world.acting_enemy_list["Hard Crocodile"]]]))
    rom.write_bytes(0x10d905, bytearray([enemy_ids[world.acting_enemy_list["Even Slimier Little Pile"]]]))
    rom.write_bytes(0x10d908, bytearray([enemy_ids[world.acting_enemy_list["Manly Fish"]]]))
    rom.write_bytes(0x10d90c, bytearray([enemy_ids[world.acting_enemy_list["Manly Fish"]]]))
    rom.write_bytes(0x10d90f, bytearray([enemy_ids[world.acting_enemy_list["Hard Crocodile"]]]))
    rom.write_bytes(0x10d913, bytearray([enemy_ids[world.acting_enemy_list["Manly Fish"]]]))
    rom.write_bytes(0x10d916, bytearray([enemy_ids[world.acting_enemy_list["Manly Fish's Brother"]]]))
    rom.write_bytes(0x10d91a, bytearray([enemy_ids[world.acting_enemy_list["Pit Bull Slug"]]]))
    rom.write_bytes(0x10d91e, bytearray([enemy_ids[world.acting_enemy_list["Demonic Petunia"]]]))
    rom.write_bytes(0x10d922, bytearray([enemy_ids[world.acting_enemy_list["Demonic Petunia"]]]))
    rom.write_bytes(0x10d925, bytearray([enemy_ids[world.acting_enemy_list["Hostile Elder Oak"]]]))
    rom.write_bytes(0x10d929, bytearray([enemy_ids[world.acting_enemy_list["Wetnosaur"]]]))
    rom.write_bytes(0x10d92d, bytearray([enemy_ids[world.acting_enemy_list["Chomposaur"]]]))
    rom.write_bytes(0x10d931, bytearray([enemy_ids[world.acting_enemy_list["Ego Orb"]]]))
    rom.write_bytes(0x10d935, bytearray([enemy_ids[world.acting_enemy_list["Care Free Bomb"]]]))
    rom.write_bytes(0x10d938, bytearray([enemy_ids[world.acting_enemy_list["Mr. Molecule"]]]))
    rom.write_bytes(0x10d93c, bytearray([enemy_ids[world.acting_enemy_list["Care Free Bomb"]]]))
    rom.write_bytes(0x10d940, bytearray([enemy_ids[world.acting_enemy_list["French Kiss of Death"]]]))
    rom.write_bytes(0x10d944, bytearray([enemy_ids[world.acting_enemy_list["Loaded Dice"]]]))
    rom.write_bytes(0x10d947, bytearray([enemy_ids[world.acting_enemy_list["Care Free Bomb"]]]))
    rom.write_bytes(0x10d94a, bytearray([enemy_ids[world.acting_enemy_list["Beautiful UFO"]]]))
    rom.write_bytes(0x10d94d, bytearray([enemy_ids[world.acting_enemy_list["High-class UFO"]]]))

    rom.write_bytes(0x10d951, bytearray([enemy_ids[world.acting_enemy_list["Loaded Dice 2"]]]))
    rom.write_bytes(0x10d954, bytearray([enemy_ids[world.acting_enemy_list["Electro Swoosh"]]]))
    rom.write_bytes(0x10d957, bytearray([enemy_ids[world.acting_enemy_list["Fobby"]]]))
    rom.write_bytes(0x10d95a, bytearray([enemy_ids[world.acting_enemy_list["Uncontrollable Sphere"]]]))
    rom.write_bytes(0x10d95e, bytearray([enemy_ids[world.acting_enemy_list["Electro Swoosh"]]]))
    rom.write_bytes(0x10d962, bytearray([enemy_ids[world.acting_enemy_list["Electro Swoosh"]]]))
    rom.write_bytes(0x10d965, bytearray([enemy_ids[world.acting_enemy_list["French Kiss of Death"]]]))
    rom.write_bytes(0x10d969, bytearray([enemy_ids[world.acting_enemy_list["Mr. Molecule"]]]))
    rom.write_bytes(0x10d96d, bytearray([enemy_ids[world.acting_enemy_list["Mr. Molecule"]]]))
    rom.write_bytes(0x10d971, bytearray([enemy_ids[world.acting_enemy_list["Rowdy Mouse"]]]))
    rom.write_bytes(0x10d974, bytearray([enemy_ids[world.acting_enemy_list["Attack Slug"]]]))
    rom.write_bytes(0x10d978, bytearray([enemy_ids[world.acting_enemy_list["Rowdy Mouse"]]]))
    rom.write_bytes(0x10d97f, bytearray([enemy_ids[world.acting_enemy_list["Rowdy Mouse"]]]))
    rom.write_bytes(0x10d98b, bytearray([enemy_ids[world.acting_enemy_list["Attack Slug"]]]))
    rom.write_bytes(0x10d98f, bytearray([enemy_ids[world.acting_enemy_list["Attack Slug"]]]))
    rom.write_bytes(0x10d993, bytearray([enemy_ids[world.acting_enemy_list["Elder Batty"]]]))
    rom.write_bytes(0x10d996, bytearray([enemy_ids[world.acting_enemy_list["Arachnid!"]]]))
    rom.write_bytes(0x10d99a, bytearray([enemy_ids[world.acting_enemy_list["Elder Batty"]]]))
    rom.write_bytes(0x10d99e, bytearray([enemy_ids[world.acting_enemy_list["Elder Batty"]]]))
    rom.write_bytes(0x10d9a1, bytearray([enemy_ids[world.acting_enemy_list["Arachnid!"]]]))
    rom.write_bytes(0x10d9a5, bytearray([enemy_ids[world.acting_enemy_list["Elder Batty"]]]))
    rom.write_bytes(0x10d9a8, bytearray([enemy_ids[world.acting_enemy_list["Strong Crocodile"]]]))
    rom.write_bytes(0x10d9ac, bytearray([enemy_ids[world.acting_enemy_list["Strong Crocodile"]]]))
    rom.write_bytes(0x10d9af, bytearray([enemy_ids[world.acting_enemy_list["Arachnid!"]]]))
    rom.write_bytes(0x10d9b3, bytearray([enemy_ids[world.acting_enemy_list["Strong Crocodile"]]]))
    rom.write_bytes(0x10d9b7, bytearray([enemy_ids[world.acting_enemy_list["Strong Crocodile"]]]))
    rom.write_bytes(0x10d9bb, bytearray([enemy_ids[world.acting_enemy_list["Arachnid!"]]]))
    rom.write_bytes(0x10d9bf, bytearray([enemy_ids[world.acting_enemy_list["Black Antoid"]]]))
    rom.write_bytes(0x10d9c2, bytearray([enemy_ids[world.acting_enemy_list["Rowdy Mouse"]]]))
    rom.write_bytes(0x10d9c6, bytearray([enemy_ids[world.acting_enemy_list["Black Antoid"]]]))
    rom.write_bytes(0x10d9c9, bytearray([enemy_ids[world.acting_enemy_list["Attack Slug"]]]))
    rom.write_bytes(0x10d9cd, bytearray([enemy_ids[world.acting_enemy_list["Black Antoid"]]]))
    rom.write_bytes(0x10d9d1, bytearray([enemy_ids[world.acting_enemy_list["Black Antoid"]]]))
    rom.write_bytes(0x10d9d4, bytearray([enemy_ids[world.acting_enemy_list["Rowdy Mouse"]]]))
    rom.write_bytes(0x10d9d8, bytearray([enemy_ids[world.acting_enemy_list["Black Antoid"]]]))
    rom.write_bytes(0x10d9dc, bytearray([enemy_ids[world.acting_enemy_list["Rowdy Mouse"]]]))
    rom.write_bytes(0x10d9e0, bytearray([enemy_ids[world.acting_enemy_list["Rowdy Mouse"]]]))
    rom.write_bytes(0x10d9e4, bytearray([enemy_ids[world.acting_enemy_list["Attack Slug"]]]))
    rom.write_bytes(0x10d9e8, bytearray([enemy_ids[world.acting_enemy_list["Attack Slug"]]]))
    rom.write_bytes(0x10d9ec, bytearray([enemy_ids[world.acting_enemy_list["Mole Playing Rough"]]]))
    rom.write_bytes(0x10d9f0, bytearray([enemy_ids[world.acting_enemy_list["Mr. Batty"]]]))
    rom.write_bytes(0x10d9f4, bytearray([enemy_ids[world.acting_enemy_list["Mr. Batty"]]]))
    rom.write_bytes(0x10d9f7, bytearray([enemy_ids[world.acting_enemy_list["Mole Playing Rough"]]]))
    rom.write_bytes(0x10d9fb, bytearray([enemy_ids[world.acting_enemy_list["Mr. Batty"]]]))
    rom.write_bytes(0x10d9fe, bytearray([enemy_ids[world.acting_enemy_list["Mighty Bear"]]]))
    rom.write_bytes(0x10da02, bytearray([enemy_ids[world.acting_enemy_list["Mr. Batty"]]]))
    rom.write_bytes(0x10da06, bytearray([enemy_ids[world.acting_enemy_list["Mole Playing Rough"]]]))
    rom.write_bytes(0x10da0a, bytearray([enemy_ids[world.acting_enemy_list["Mole Playing Rough"]]]))
    rom.write_bytes(0x10da0d, bytearray([enemy_ids[world.acting_enemy_list["Mighty Bear"]]]))
    rom.write_bytes(0x10da11, bytearray([enemy_ids[world.acting_enemy_list["Mighty Bear"]]]))
    rom.write_bytes(0x10da15, bytearray([enemy_ids[world.acting_enemy_list["Mighty Bear"]]]))
    rom.write_bytes(0x10da18, bytearray([enemy_ids[world.acting_enemy_list["Mr. Batty"]]]))
    rom.write_bytes(0x10da1c, bytearray([enemy_ids[world.acting_enemy_list["Urban Zombie"]]]))
    rom.write_bytes(0x10da1f, bytearray([enemy_ids[world.acting_enemy_list["Zombie Dog"]]]))
    rom.write_bytes(0x10da23, bytearray([enemy_ids[world.acting_enemy_list["Urban Zombie"]]]))
    rom.write_bytes(0x10da27, bytearray([enemy_ids[world.acting_enemy_list["Zombie Dog"]]]))
    rom.write_bytes(0x10da2a, bytearray([enemy_ids[world.acting_enemy_list["No Good Fly"]]]))
    rom.write_bytes(0x10da2e, bytearray([enemy_ids[world.acting_enemy_list["Zombie Possessor"]]]))
    rom.write_bytes(0x10da32, bytearray([enemy_ids[world.acting_enemy_list["Zombie Possessor"]]]))
    rom.write_bytes(0x10da35, bytearray([enemy_ids[world.acting_enemy_list["Urban Zombie"]]]))
    rom.write_bytes(0x10da39, bytearray([enemy_ids[world.acting_enemy_list["Zombie Possessor"]]]))
    rom.write_bytes(0x10da3c, bytearray([enemy_ids[world.acting_enemy_list["Urban Zombie"]]]))
    rom.write_bytes(0x10da40, bytearray([enemy_ids[world.acting_enemy_list["Zombie Possessor"]]]))
    rom.write_bytes(0x10da44, bytearray([enemy_ids[world.acting_enemy_list["Violent Roach"]]]))
    rom.write_bytes(0x10da48, bytearray([enemy_ids[world.acting_enemy_list["Foppy"]]]))
    rom.write_bytes(0x10da4c, bytearray([enemy_ids[world.acting_enemy_list["Foppy"]]]))
    rom.write_bytes(0x10da50, bytearray([enemy_ids[world.acting_enemy_list["Foppy"]]]))
    rom.write_bytes(0x10da54, bytearray([enemy_ids[world.acting_enemy_list["Foppy"]]]))
    rom.write_bytes(0x10da58, bytearray([enemy_ids[world.acting_enemy_list["Foppy"]]]))
    rom.write_bytes(0x10da5c, bytearray([enemy_ids[world.acting_enemy_list["Mostly Bad Fly"]]]))
    rom.write_bytes(0x10da60, bytearray([enemy_ids[world.acting_enemy_list["Slimy Little Pile"]]]))
    rom.write_bytes(0x10da63, bytearray([enemy_ids[world.acting_enemy_list["Mostly Bad Fly"]]]))
    rom.write_bytes(0x10da67, bytearray([enemy_ids[world.acting_enemy_list["Slimy Little Pile"]]]))
    rom.write_bytes(0x10da6a, bytearray([enemy_ids[world.acting_enemy_list["Mostly Bad Fly"]]]))
    rom.write_bytes(0x10da6e, bytearray([enemy_ids[world.acting_enemy_list["Slimy Little Pile"]]]))
    rom.write_bytes(0x10da72, bytearray([enemy_ids[world.acting_enemy_list["Slimy Little Pile"]]]))
    rom.write_bytes(0x10da76, bytearray([enemy_ids[world.acting_enemy_list["Slimy Little Pile"]]]))
    rom.write_bytes(0x10da7a, bytearray([enemy_ids[world.acting_enemy_list["Farm Zombie"]]]))
    rom.write_bytes(0x10da7e, bytearray([enemy_ids[world.acting_enemy_list["Farm Zombie"]]]))
    rom.write_bytes(0x10da82, bytearray([enemy_ids[world.acting_enemy_list["Struttin' Evil Mushroom"]]]))
    rom.write_bytes(0x10da85, bytearray([enemy_ids[world.acting_enemy_list["Tough Mobile Sprout"]]]))
    rom.write_bytes(0x10da89, bytearray([enemy_ids[world.acting_enemy_list["Struttin' Evil Mushroom"]]]))
    rom.write_bytes(0x10da8c, bytearray([enemy_ids[world.acting_enemy_list["Tough Mobile Sprout"]]]))
    rom.write_bytes(0x10da8f, bytearray([enemy_ids[world.acting_enemy_list["Ranboob"]]]))
    rom.write_bytes(0x10da93, bytearray([enemy_ids[world.acting_enemy_list["Ranboob"]]]))
    rom.write_bytes(0x10da97, bytearray([enemy_ids[world.acting_enemy_list["Tough Mobile Sprout"]]]))
    rom.write_bytes(0x10da9a, bytearray([enemy_ids[world.acting_enemy_list["Ranboob"]]]))
    rom.write_bytes(0x10da9e, bytearray([enemy_ids[world.acting_enemy_list["Tough Mobile Sprout"]]]))
    rom.write_bytes(0x10daa1, bytearray([enemy_ids[world.acting_enemy_list["Ranboob"]]]))
    rom.write_bytes(0x10daa5, bytearray([enemy_ids[world.acting_enemy_list["Tough Mobile Sprout"]]]))
    rom.write_bytes(0x10daa8, bytearray([enemy_ids[world.acting_enemy_list["Struttin' Evil Mushroom"]]]))
    rom.write_bytes(0x10daac, bytearray([enemy_ids[world.acting_enemy_list["Struttin' Evil Mushroom"]]]))
    rom.write_bytes(0x10daaf, bytearray([enemy_ids[world.acting_enemy_list["Tough Mobile Sprout"]]]))
    rom.write_bytes(0x10dab2, bytearray([enemy_ids[world.acting_enemy_list["Ranboob"]]]))
    rom.write_bytes(0x10dab6, bytearray([enemy_ids[world.acting_enemy_list["Struttin' Evil Mushroom"]]]))
    rom.write_bytes(0x10dab9, bytearray([enemy_ids[world.acting_enemy_list["Tough Mobile Sprout"]]]))
    rom.write_bytes(0x10dabc, bytearray([enemy_ids[world.acting_enemy_list["Ranboob"]]]))
    rom.write_bytes(0x10dac0, bytearray([enemy_ids[world.acting_enemy_list["Ranboob"]]]))
    rom.write_bytes(0x10dac4, bytearray([enemy_ids[world.acting_enemy_list["Tough Mobile Sprout"]]]))
    rom.write_bytes(0x10dac7, bytearray([enemy_ids[world.acting_enemy_list["Struttin' Evil Mushroom"]]]))
    rom.write_bytes(0x10dacb, bytearray([enemy_ids[world.acting_enemy_list["Tough Mobile Sprout"]]]))
    rom.write_bytes(0x10dace, bytearray([enemy_ids[world.acting_enemy_list["Struttin' Evil Mushroom"]]]))
    rom.write_bytes(0x10dad2, bytearray([enemy_ids[world.acting_enemy_list["Tough Mobile Sprout"]]]))
    rom.write_bytes(0x10dad6, bytearray([enemy_ids[world.acting_enemy_list["Struttin' Evil Mushroom"]]]))
    rom.write_bytes(0x10dada, bytearray([enemy_ids[world.acting_enemy_list["Gigantic Ant"]]]))
    rom.write_bytes(0x10dade, bytearray([enemy_ids[world.acting_enemy_list["Gigantic Ant"]]]))
    rom.write_bytes(0x10dae2, bytearray([enemy_ids[world.acting_enemy_list["Thirsty Coil Snake"]]]))
    rom.write_bytes(0x10dae5, bytearray([enemy_ids[world.acting_enemy_list["Gigantic Ant"]]]))
    rom.write_bytes(0x10dae9, bytearray([enemy_ids[world.acting_enemy_list["Thirsty Coil Snake"]]]))
    rom.write_bytes(0x10daed, bytearray([enemy_ids[world.acting_enemy_list["Thirsty Coil Snake"]]]))
    rom.write_bytes(0x10daf1, bytearray([enemy_ids[world.acting_enemy_list["Mad Duck"]]]))
    rom.write_bytes(0x10daf4, bytearray([enemy_ids[world.acting_enemy_list["Thirsty Coil Snake"]]]))
    rom.write_bytes(0x10daf8, bytearray([enemy_ids[world.acting_enemy_list["Mad Duck"]]]))
    rom.write_bytes(0x10dafc, bytearray([enemy_ids[world.acting_enemy_list["Noose Man"]]]))
    rom.write_bytes(0x10daff, bytearray([enemy_ids[world.acting_enemy_list["Mad Duck"]]]))
    rom.write_bytes(0x10db03, bytearray([enemy_ids[world.acting_enemy_list["Noose Man"]]]))
    rom.write_bytes(0x10db06, bytearray([enemy_ids[world.acting_enemy_list["Mad Duck"]]]))
    rom.write_bytes(0x10db0a, bytearray([enemy_ids[world.acting_enemy_list["Noose Man"]]]))
    rom.write_bytes(0x10db0d, bytearray([enemy_ids[world.acting_enemy_list["Mad Duck"]]]))
    rom.write_bytes(0x10db11, bytearray([enemy_ids[world.acting_enemy_list["Noose Man"]]]))
    rom.write_bytes(0x10db14, bytearray([enemy_ids[world.acting_enemy_list["Mad Duck"]]]))
    rom.write_bytes(0x10db18, bytearray([enemy_ids[world.acting_enemy_list["Noose Man"]]]))
    rom.write_bytes(0x10db1b, bytearray([enemy_ids[world.acting_enemy_list["Mad Duck"]]]))
    rom.write_bytes(0x10db1f, bytearray([enemy_ids[world.acting_enemy_list["Noose Man"]]]))
    rom.write_bytes(0x10db22, bytearray([enemy_ids[world.acting_enemy_list["Gigantic Ant"]]]))
    rom.write_bytes(0x10db26, bytearray([enemy_ids[world.acting_enemy_list["Noose Man"]]]))
    rom.write_bytes(0x10db29, bytearray([enemy_ids[world.acting_enemy_list["Mad Duck"]]]))
    rom.write_bytes(0x10db2d, bytearray([enemy_ids[world.acting_enemy_list["Noose Man"]]]))
    rom.write_bytes(0x10db30, bytearray([enemy_ids[world.acting_enemy_list["Mad Duck"]]]))
    rom.write_bytes(0x10db34, bytearray([enemy_ids[world.acting_enemy_list["Noose Man"]]]))
    rom.write_bytes(0x10db38, bytearray([enemy_ids[world.acting_enemy_list["Noose Man"]]]))
    rom.write_bytes(0x10db3b, bytearray([enemy_ids[world.acting_enemy_list["Gigantic Ant"]]]))
    rom.write_bytes(0x10db3f, bytearray([enemy_ids[world.acting_enemy_list["Musica"]]]))
    rom.write_bytes(0x10db42, bytearray([enemy_ids[world.acting_enemy_list["Mystical Record"]]]))
    rom.write_bytes(0x10db46, bytearray([enemy_ids[world.acting_enemy_list["Musica"]]]))
    rom.write_bytes(0x10db49, bytearray([enemy_ids[world.acting_enemy_list["Mystical Record"]]]))
    rom.write_bytes(0x10db4d, bytearray([enemy_ids[world.acting_enemy_list["Musica"]]]))
    rom.write_bytes(0x10db51, bytearray([enemy_ids[world.acting_enemy_list["Scalding Coffee Cup"]]]))
    rom.write_bytes(0x10db54, bytearray([enemy_ids[world.acting_enemy_list["Mystical Record"]]]))
    rom.write_bytes(0x10db58, bytearray([enemy_ids[world.acting_enemy_list["Scalding Coffee Cup"]]]))
    rom.write_bytes(0x10db5b, bytearray([enemy_ids[world.acting_enemy_list["Mystical Record"]]]))
    rom.write_bytes(0x10db5f, bytearray([enemy_ids[world.acting_enemy_list["Scalding Coffee Cup"]]]))
    rom.write_bytes(0x10db63, bytearray([enemy_ids[world.acting_enemy_list["Mystical Record"]]]))
    rom.write_bytes(0x10db67, bytearray([enemy_ids[world.acting_enemy_list["Stinky Ghost"]]]))
    rom.write_bytes(0x10db6b, bytearray([enemy_ids[world.acting_enemy_list["Deadly Mouse"]]]))
    rom.write_bytes(0x10db6e, bytearray([enemy_ids[world.acting_enemy_list["Stinky Ghost"]]]))
    rom.write_bytes(0x10db72, bytearray([enemy_ids[world.acting_enemy_list["Filthy Attack Roach"]]]))
    rom.write_bytes(0x10db76, bytearray([enemy_ids[world.acting_enemy_list["Filthy Attack Roach"]]]))
    rom.write_bytes(0x10db7a, bytearray([enemy_ids[world.acting_enemy_list["Deadly Mouse"]]]))
    rom.write_bytes(0x10db7e, bytearray([enemy_ids[world.acting_enemy_list["Deadly Mouse"]]]))
    rom.write_bytes(0x10db81, bytearray([enemy_ids[world.acting_enemy_list["Stinky Ghost"]]]))
    rom.write_bytes(0x10db85, bytearray([enemy_ids[world.acting_enemy_list["Stinky Ghost"]]]))
    rom.write_bytes(0x10db89, bytearray([enemy_ids[world.acting_enemy_list["Deadly Mouse"]]]))
    rom.write_bytes(0x10db8c, bytearray([enemy_ids[world.acting_enemy_list["Stinky Ghost"]]]))
    rom.write_bytes(0x10db90, bytearray([enemy_ids[world.acting_enemy_list["Filthy Attack Roach"]]]))
    rom.write_bytes(0x10db94, bytearray([enemy_ids[world.acting_enemy_list["Filthy Attack Roach"]]]))
    rom.write_bytes(0x10db98, bytearray([enemy_ids[world.acting_enemy_list["Filthy Attack Roach"]]]))
    rom.write_bytes(0x10db9c, bytearray([enemy_ids[world.acting_enemy_list["Filthy Attack Roach"]]]))
    rom.write_bytes(0x10dba0, bytearray([enemy_ids[world.acting_enemy_list["Deadly Mouse"]]]))
    rom.write_bytes(0x10dba4, bytearray([enemy_ids[world.acting_enemy_list["Deadly Mouse"]]]))
    rom.write_bytes(0x10dba8, bytearray([enemy_ids[world.acting_enemy_list["Thunder Mite"]]]))
    rom.write_bytes(0x10dbac, bytearray([enemy_ids[world.acting_enemy_list["Tangoo"]]]))
    rom.write_bytes(0x10dbb0, bytearray([enemy_ids[world.acting_enemy_list["Thunder Mite"]]]))
    rom.write_bytes(0x10dbb3, bytearray([enemy_ids[world.acting_enemy_list["Tangoo"]]]))
    rom.write_bytes(0x10dbb7, bytearray([enemy_ids[world.acting_enemy_list["Tangoo"]]]))
    rom.write_bytes(0x10dbba, bytearray([enemy_ids[world.acting_enemy_list["Kiss of Death"]]]))
    rom.write_bytes(0x10dbbe, bytearray([enemy_ids[world.acting_enemy_list["Thunder Mite"]]]))
    rom.write_bytes(0x10dbc1, bytearray([enemy_ids[world.acting_enemy_list["Tangoo"]]]))
    rom.write_bytes(0x10dbc5, bytearray([enemy_ids[world.acting_enemy_list["Tangoo"]]]))
    rom.write_bytes(0x10dbc9, bytearray([enemy_ids[world.acting_enemy_list["Thunder Mite"]]]))
    rom.write_bytes(0x10dbcd, bytearray([enemy_ids[world.acting_enemy_list["Conducting Menace"]]]))
    rom.write_bytes(0x10dbd0, bytearray([enemy_ids[world.acting_enemy_list["Tangoo"]]]))
    rom.write_bytes(0x10dbd4, bytearray([enemy_ids[world.acting_enemy_list["Conducting Menace"]]]))
    rom.write_bytes(0x10dbd8, bytearray([enemy_ids[world.acting_enemy_list["Kiss of Death"]]]))
    rom.write_bytes(0x10dbdc, bytearray([enemy_ids[world.acting_enemy_list["Kiss of Death"]]]))
    rom.write_bytes(0x10dbdf, bytearray([enemy_ids[world.acting_enemy_list["Conducting Menace"]]]))
    rom.write_bytes(0x10dbe3, bytearray([enemy_ids[world.acting_enemy_list["Conducting Menace"]]]))
    rom.write_bytes(0x10dbe7, bytearray([enemy_ids[world.acting_enemy_list["Conducting Menace"]]]))
    rom.write_bytes(0x10dbea, bytearray([enemy_ids[world.acting_enemy_list["Tangoo"]]]))
    rom.write_bytes(0x10dbee, bytearray([enemy_ids[world.acting_enemy_list["Conducting Menace"]]]))
    rom.write_bytes(0x10dbf1, bytearray([enemy_ids[world.acting_enemy_list["Tangoo"]]]))
    rom.write_bytes(0x10dbf4, bytearray([enemy_ids[world.acting_enemy_list["Kiss of Death"]]]))
    rom.write_bytes(0x10dbf8, bytearray([enemy_ids[world.acting_enemy_list["Arachnid!!!"]]]))
    rom.write_bytes(0x10dbfc, bytearray([enemy_ids[world.acting_enemy_list["Arachnid!!!"]]]))
    rom.write_bytes(0x10dc00, bytearray([enemy_ids[world.acting_enemy_list["Fierce Shattered Man"]]]))
    rom.write_bytes(0x10dc04, bytearray([enemy_ids[world.acting_enemy_list["Fierce Shattered Man"]]]))
    rom.write_bytes(0x10dc07, bytearray([enemy_ids[world.acting_enemy_list["Arachnid!!!"]]]))
    rom.write_bytes(0x10dc0b, bytearray([enemy_ids[world.acting_enemy_list["Arachnid!!!"]]]))
    rom.write_bytes(0x10dc0f, bytearray([enemy_ids[world.acting_enemy_list["Arachnid!!!"]]]))
    rom.write_bytes(0x10dc13, bytearray([enemy_ids[world.acting_enemy_list["Arachnid!!!"]]]))
    rom.write_bytes(0x10dc17, bytearray([enemy_ids[world.acting_enemy_list["Arachnid!!!"]]]))
    rom.write_bytes(0x10dc1b, bytearray([enemy_ids[world.acting_enemy_list["Petrified Royal Guard"]]]))
    rom.write_bytes(0x10dc1e, bytearray([enemy_ids[world.acting_enemy_list["Lethal Asp Hieroglyph"]]]))
    rom.write_bytes(0x10dc22, bytearray([enemy_ids[world.acting_enemy_list["Arachnid!!!"]]]))
    rom.write_bytes(0x10dc25, bytearray([enemy_ids[world.acting_enemy_list["Guardian Hieroglyph"]]]))
    rom.write_bytes(0x10dc29, bytearray([enemy_ids[world.acting_enemy_list["Fierce Shattered Man"]]]))
    rom.write_bytes(0x10dc2d, bytearray([enemy_ids[world.acting_enemy_list["Fierce Shattered Man"]]]))
    rom.write_bytes(0x10dc30, bytearray([enemy_ids[world.acting_enemy_list["Petrified Royal Guard"]]]))
    rom.write_bytes(0x10dc34, bytearray([enemy_ids[world.acting_enemy_list["Petrified Royal Guard"]]]))
    rom.write_bytes(0x10dc38, bytearray([enemy_ids[world.acting_enemy_list["Lethal Asp Hieroglyph"]]]))
    rom.write_bytes(0x10dc3c, bytearray([enemy_ids[world.acting_enemy_list["Arachnid!!!"]]]))
    rom.write_bytes(0x10dc40, bytearray([enemy_ids[world.acting_enemy_list["Arachnid!!!"]]]))
    rom.write_bytes(0x10dc44, bytearray([enemy_ids[world.acting_enemy_list["Arachnid!!!"]]]))
    rom.write_bytes(0x10dc48, bytearray([enemy_ids[world.acting_enemy_list["Arachnid!!!"]]]))
    rom.write_bytes(0x10dc4c, bytearray([enemy_ids[world.acting_enemy_list["Fierce Shattered Man"]]]))
    rom.write_bytes(0x10dc50, bytearray([enemy_ids[world.acting_enemy_list["Fierce Shattered Man"]]]))
    rom.write_bytes(0x10dc53, bytearray([enemy_ids[world.acting_enemy_list["Petrified Royal Guard"]]]))
    rom.write_bytes(0x10dc57, bytearray([enemy_ids[world.acting_enemy_list["Petrified Royal Guard"]]]))
    rom.write_bytes(0x10dc5a, bytearray([enemy_ids[world.acting_enemy_list["Lethal Asp Hieroglyph"]]]))
    rom.write_bytes(0x10dc5e, bytearray([enemy_ids[world.acting_enemy_list["Fierce Shattered Man"]]]))
    rom.write_bytes(0x10dc61, bytearray([enemy_ids[world.acting_enemy_list["Guardian Hieroglyph"]]]))
    rom.write_bytes(0x10dc65, bytearray([enemy_ids[world.acting_enemy_list["Scalding Coffee Cup"]]]))
    rom.write_bytes(0x10dc68, bytearray([enemy_ids[world.acting_enemy_list["Mystical Record"]]]))
    rom.write_bytes(0x10dc6b, bytearray([enemy_ids[world.acting_enemy_list["Worthless Protoplasm"]]]))
    rom.write_bytes(0x10dc6f, bytearray([enemy_ids[world.acting_enemy_list["Cute Li'l UFO"]]]))
    rom.write_bytes(0x10dc73, bytearray([enemy_ids[world.acting_enemy_list["Cute Li'l UFO"]]]))
    rom.write_bytes(0x10dc77, bytearray([enemy_ids[world.acting_enemy_list["Dali's Clock"]]]))
    rom.write_bytes(0x10dc7b, bytearray([enemy_ids[world.acting_enemy_list["Robo-pump"]]]))
    rom.write_bytes(0x10dc7e, bytearray([enemy_ids[world.acting_enemy_list["Enraged Fire Plug"]]]))
    rom.write_bytes(0x10dc82, bytearray([enemy_ids[world.acting_enemy_list["Robo-pump"]]]))
    rom.write_bytes(0x10dc86, bytearray([enemy_ids[world.acting_enemy_list["Enraged Fire Plug"]]]))
    rom.write_bytes(0x10dc8a, bytearray([enemy_ids[world.acting_enemy_list["Lesser Mook"]]]))
    rom.write_bytes(0x10dc8e, bytearray([enemy_ids[world.acting_enemy_list["Lesser Mook"]]]))
    rom.write_bytes(0x10dc92, bytearray([enemy_ids[world.acting_enemy_list["Lesser Mook"]]]))
    rom.write_bytes(0x10dc95, bytearray([enemy_ids[world.acting_enemy_list["Mook Senior"]]]))
    rom.write_bytes(0x10dc99, bytearray([enemy_ids[world.acting_enemy_list["Mook Senior"]]]))
    rom.write_bytes(0x10dc9d, bytearray([enemy_ids[world.acting_enemy_list["Mook Senior"]]]))
    rom.write_bytes(0x10dca1, bytearray([enemy_ids[world.acting_enemy_list["Lesser Mook"]]]))
    rom.write_bytes(0x10dca5, bytearray([enemy_ids[world.acting_enemy_list["Lesser Mook"]]]))
    rom.write_bytes(0x10dca9, bytearray([enemy_ids[world.acting_enemy_list["Lesser Mook"]]]))
    rom.write_bytes(0x10dcad, bytearray([enemy_ids[world.acting_enemy_list["Worthless Protoplasm"]]]))
    rom.write_bytes(0x10dcb1, bytearray([enemy_ids[world.acting_enemy_list["Worthless Protoplasm"]]]))
    rom.write_bytes(0x10dcb5, bytearray([enemy_ids[world.acting_enemy_list["Worthless Protoplasm"]]]))
    rom.write_bytes(0x10dcb9, bytearray([enemy_ids[world.acting_enemy_list["Mook Senior"]]]))
    rom.write_bytes(0x10dcbd, bytearray([enemy_ids[world.acting_enemy_list["Mook Senior"]]]))
    rom.write_bytes(0x10dcc1, bytearray([enemy_ids[world.acting_enemy_list["Mook Senior"]]]))
    rom.write_bytes(0x10dcc5, bytearray([enemy_ids[world.acting_enemy_list["Starman"]]]))
    rom.write_bytes(0x10dcc9, bytearray([enemy_ids[world.acting_enemy_list["Mook Senior"]]]))
    rom.write_bytes(0x10dccd, bytearray([enemy_ids[world.acting_enemy_list["Starman"]]]))
    rom.write_bytes(0x10dcd1, bytearray([enemy_ids[world.acting_enemy_list["Mook Senior"]]]))
    rom.write_bytes(0x10dcd5, bytearray([enemy_ids[world.acting_enemy_list["Starman"]]]))
    rom.write_bytes(0x10dcd8, bytearray([enemy_ids[world.acting_enemy_list["Mook Senior"]]]))
    rom.write_bytes(0x10dcdc, bytearray([enemy_ids[world.acting_enemy_list["Mook Senior"]]]))
    rom.write_bytes(0x10dcdf, bytearray([enemy_ids[world.acting_enemy_list["Atomic Power Robot"]]]))
    rom.write_bytes(0x10dce3, bytearray([enemy_ids[world.acting_enemy_list["Starman"]]]))
    rom.write_bytes(0x10dce7, bytearray([enemy_ids[world.acting_enemy_list["Mook Senior"]]]))
    rom.write_bytes(0x10dceb, bytearray([enemy_ids[world.acting_enemy_list["Mook Senior"]]]))
    rom.write_bytes(0x10dcee, bytearray([enemy_ids[world.acting_enemy_list["Starman"]]]))
    rom.write_bytes(0x10dcf2, bytearray([enemy_ids[world.acting_enemy_list["Mook Senior"]]]))
    rom.write_bytes(0x10dcf5, bytearray([enemy_ids[world.acting_enemy_list["Starman"]]]))
    rom.write_bytes(0x10dcf9, bytearray([enemy_ids[world.acting_enemy_list["Starman"]]]))
    rom.write_bytes(0x10dcfd, bytearray([enemy_ids[world.acting_enemy_list["Atomic Power Robot"]]]))
    rom.write_bytes(0x10dd00, bytearray([enemy_ids[world.acting_enemy_list["Starman"]]]))
    rom.write_bytes(0x10dd04, bytearray([enemy_ids[world.acting_enemy_list["Atomic Power Robot"]]]))
    rom.write_bytes(0x10dd07, bytearray([enemy_ids[world.acting_enemy_list["Starman"]]]))
    rom.write_bytes(0x10dd0b, bytearray([enemy_ids[world.acting_enemy_list["Starman Super"]]]))
    rom.write_bytes(0x10dd0f, bytearray([enemy_ids[world.acting_enemy_list["Starman"]]]))
    rom.write_bytes(0x10dd12, bytearray([enemy_ids[world.acting_enemy_list["Starman Super"]]]))
    rom.write_bytes(0x10dd16, bytearray([enemy_ids[world.acting_enemy_list["Starman Super"]]]))
    rom.write_bytes(0x10dd19, bytearray([enemy_ids[world.acting_enemy_list["Atomic Power Robot"]]]))
    rom.write_bytes(0x10dd1d, bytearray([enemy_ids[world.acting_enemy_list["Starman"]]]))
    rom.write_bytes(0x10dd20, bytearray([enemy_ids[world.acting_enemy_list["Starman Super"]]]))
    rom.write_bytes(0x10dd24, bytearray([enemy_ids[world.acting_enemy_list["Atomic Power Robot"]]]))
    rom.write_bytes(0x10dd27, bytearray([enemy_ids[world.acting_enemy_list["Starman"]]]))
    rom.write_bytes(0x10dd2a, bytearray([enemy_ids[world.acting_enemy_list["Starman Super"]]]))
    rom.write_bytes(0x10dd2e, bytearray([enemy_ids[world.acting_enemy_list["Atomic Power Robot"]]]))
    rom.write_bytes(0x10dd31, bytearray([enemy_ids[world.acting_enemy_list["Starman"]]]))
    rom.write_bytes(0x10dd34, bytearray([enemy_ids[world.acting_enemy_list["Starman Super"]]]))
    rom.write_bytes(0x10dd38, bytearray([enemy_ids[world.acting_enemy_list["Starman Super"]]]))
    rom.write_bytes(0x10dd3b, bytearray([enemy_ids[world.acting_enemy_list["Atomic Power Robot"]]]))
    rom.write_bytes(0x10dd3f, bytearray([enemy_ids[world.acting_enemy_list["Starman Super"]]]))
    rom.write_bytes(0x10dd42, bytearray([enemy_ids[world.acting_enemy_list["Military Octobot"]]]))
    rom.write_bytes(0x10dd46, bytearray([enemy_ids[world.acting_enemy_list["Atomic Power Robot"]]]))
    rom.write_bytes(0x10dd49, bytearray([enemy_ids[world.acting_enemy_list["Starman Super"]]]))
    rom.write_bytes(0x10dd4d, bytearray([enemy_ids[world.acting_enemy_list["Atomic Power Robot"]]]))
    rom.write_bytes(0x10dd50, bytearray([enemy_ids[world.acting_enemy_list["Military Octobot"]]]))
    rom.write_bytes(0x10dd54, bytearray([enemy_ids[world.acting_enemy_list["Atomic Power Robot"]]]))
    rom.write_bytes(0x10dd57, bytearray([enemy_ids[world.acting_enemy_list["Military Octobot"]]]))
    rom.write_bytes(0x10dd5b, bytearray([enemy_ids[world.acting_enemy_list["Atomic Power Robot"]]]))
    rom.write_bytes(0x10dd5e, bytearray([enemy_ids[world.acting_enemy_list["Military Octobot"]]]))
    rom.write_bytes(0x10dd62, bytearray([enemy_ids[world.acting_enemy_list["Fobby"]]]))
    rom.write_bytes(0x10dd66, bytearray([enemy_ids[world.acting_enemy_list["Fobby"]]]))
    rom.write_bytes(0x10dd6a, bytearray([enemy_ids[world.acting_enemy_list["Fobby"]]]))
    rom.write_bytes(0x10dd6e, bytearray([enemy_ids[world.acting_enemy_list["Fobby"]]]))
    rom.write_bytes(0x10dd72, bytearray([enemy_ids[world.acting_enemy_list["Uncontrollable Sphere"]]]))
    rom.write_bytes(0x10dd75, bytearray([enemy_ids[world.acting_enemy_list["Fobby"]]]))
    rom.write_bytes(0x10dd79, bytearray([enemy_ids[world.acting_enemy_list["Fobby"]]]))
    rom.write_bytes(0x10dd7d, bytearray([enemy_ids[world.acting_enemy_list["Hyper Spinning Robo"]]]))
    rom.write_bytes(0x10dd80, bytearray([enemy_ids[world.acting_enemy_list["Fobby"]]]))
    rom.write_bytes(0x10dd84, bytearray([enemy_ids[world.acting_enemy_list["Fobby"]]]))
    rom.write_bytes(0x10dd88, bytearray([enemy_ids[world.acting_enemy_list["Fobby"]]]))
    rom.write_bytes(0x10dd8c, bytearray([enemy_ids[world.acting_enemy_list["Conducting Spirit"]]]))
    rom.write_bytes(0x10dd8f, bytearray([enemy_ids[world.acting_enemy_list["Fobby"]]]))
    rom.write_bytes(0x10dd93, bytearray([enemy_ids[world.acting_enemy_list["Uncontrollable Sphere"]]]))
    rom.write_bytes(0x10dd96, bytearray([enemy_ids[world.acting_enemy_list["Conducting Spirit"]]]))
    rom.write_bytes(0x10dd9a, bytearray([enemy_ids[world.acting_enemy_list["Uncontrollable Sphere"]]]))
    rom.write_bytes(0x10dd9e, bytearray([enemy_ids[world.acting_enemy_list["Conducting Spirit"]]]))
    rom.write_bytes(0x10dda2, bytearray([enemy_ids[world.acting_enemy_list["Conducting Spirit"]]]))
    rom.write_bytes(0x10dda6, bytearray([enemy_ids[world.acting_enemy_list["Hyper Spinning Robo"]]]))
    rom.write_bytes(0x10dda9, bytearray([enemy_ids[world.acting_enemy_list["Conducting Spirit"]]]))
    rom.write_bytes(0x10ddad, bytearray([enemy_ids[world.acting_enemy_list["Conducting Spirit"]]]))
    rom.write_bytes(0x10ddb1, bytearray([enemy_ids[world.acting_enemy_list["Uncontrollable Sphere"]]]))
    rom.write_bytes(0x10ddb4, bytearray([enemy_ids[world.acting_enemy_list["Conducting Spirit"]]]))
    rom.write_bytes(0x10ddb8, bytearray([enemy_ids[world.acting_enemy_list["Hyper Spinning Robo"]]]))
    rom.write_bytes(0x10ddbb, bytearray([enemy_ids[world.acting_enemy_list["Conducting Spirit"]]]))
    rom.write_bytes(0x10ddbf, bytearray([enemy_ids[world.acting_enemy_list["Hyper Spinning Robo"]]]))
    rom.write_bytes(0x10ddc3, bytearray([enemy_ids[world.acting_enemy_list["Hyper Spinning Robo"]]]))
    rom.write_bytes(0x10ddc6, bytearray([enemy_ids[world.acting_enemy_list["Uncontrollable Sphere"]]]))
    rom.write_bytes(0x10ddca, bytearray([enemy_ids[world.acting_enemy_list["Soul Consuming Flame"]]]))
    rom.write_bytes(0x10ddce, bytearray([enemy_ids[world.acting_enemy_list["Psychic Psycho"]]]))
    rom.write_bytes(0x10ddd2, bytearray([enemy_ids[world.acting_enemy_list["Evil Elemental"]]]))
    rom.write_bytes(0x10ddd6, bytearray([enemy_ids[world.acting_enemy_list["Evil Elemental"]]]))
    rom.write_bytes(0x10ddd9, bytearray([enemy_ids[world.acting_enemy_list["Soul Consuming Flame"]]]))
    rom.write_bytes(0x10dddd, bytearray([enemy_ids[world.acting_enemy_list["Evil Elemental"]]]))
    rom.write_bytes(0x10dde0, bytearray([enemy_ids[world.acting_enemy_list["Soul Consuming Flame"]]]))
    rom.write_bytes(0x10dde4, bytearray([enemy_ids[world.acting_enemy_list["Evil Elemental"]]]))
    rom.write_bytes(0x10dde8, bytearray([enemy_ids[world.acting_enemy_list["Evil Elemental"]]]))
    rom.write_bytes(0x10ddeb, bytearray([enemy_ids[world.acting_enemy_list["Soul Consuming Flame"]]]))
    rom.write_bytes(0x10ddef, bytearray([enemy_ids[world.acting_enemy_list["Soul Consuming Flame"]]]))
    rom.write_bytes(0x10ddf3, bytearray([enemy_ids[world.acting_enemy_list["Soul Consuming Flame"]]]))
    rom.write_bytes(0x10ddf7, bytearray([enemy_ids[world.acting_enemy_list["Psychic Psycho"]]]))
    rom.write_bytes(0x10ddfa, bytearray([enemy_ids[world.acting_enemy_list["Major Psychic Psycho"]]]))
    rom.write_bytes(0x10ddfe, bytearray([enemy_ids[world.acting_enemy_list["Evil Elemental"]]]))
    rom.write_bytes(0x10de01, bytearray([enemy_ids[world.acting_enemy_list["Psychic Psycho"]]]))
    rom.write_bytes(0x10de05, bytearray([enemy_ids[world.acting_enemy_list["Soul Consuming Flame"]]]))
    rom.write_bytes(0x10de08, bytearray([enemy_ids[world.acting_enemy_list["Major Psychic Psycho"]]]))
    rom.write_bytes(0x10de0c, bytearray([enemy_ids[world.acting_enemy_list["Soul Consuming Flame"]]]))
    rom.write_bytes(0x10de0f, bytearray([enemy_ids[world.acting_enemy_list["Major Psychic Psycho"]]]))
    rom.write_bytes(0x10de13, bytearray([enemy_ids[world.acting_enemy_list["Soul Consuming Flame"]]]))
    rom.write_bytes(0x10de17, bytearray([enemy_ids[world.acting_enemy_list["Ghost of Starman"]]]))
    rom.write_bytes(0x10de1a, bytearray([enemy_ids[world.acting_enemy_list["Nuclear Reactor Robot"]]]))
    rom.write_bytes(0x10de1e, bytearray([enemy_ids[world.acting_enemy_list["Wild 'n Wooly Shambler"]]]))
    rom.write_bytes(0x10de21, bytearray([enemy_ids[world.acting_enemy_list["Ultimate Octobot"]]]))
    rom.write_bytes(0x10de25, bytearray([enemy_ids[world.acting_enemy_list["Ultimate Octobot"]]]))
    rom.write_bytes(0x10de28, bytearray([enemy_ids[world.acting_enemy_list["Nuclear Reactor Robot"]]]))
    rom.write_bytes(0x10de2c, bytearray([enemy_ids[world.acting_enemy_list["Squatter Demon"]]]))
    rom.write_bytes(0x10de30, bytearray([enemy_ids[world.acting_enemy_list["Ghost of Starman"]]]))
    rom.write_bytes(0x10de33, bytearray([enemy_ids[world.acting_enemy_list["Wild 'n Wooly Shambler"]]]))
    rom.write_bytes(0x10de37, bytearray([enemy_ids[world.acting_enemy_list["Ghost of Starman"]]]))
    rom.write_bytes(0x10de3a, bytearray([enemy_ids[world.acting_enemy_list["Nuclear Reactor Robot"]]]))
    rom.write_bytes(0x10de3e, bytearray([enemy_ids[world.acting_enemy_list["Nuclear Reactor Robot"]]]))
    rom.write_bytes(0x10de41, bytearray([enemy_ids[world.acting_enemy_list["Final Starman"]]]))
    rom.write_bytes(0x10de45, bytearray([enemy_ids[world.acting_enemy_list["Ghost of Starman"]]]))
    rom.write_bytes(0x10de48, bytearray([enemy_ids[world.acting_enemy_list["Final Starman"]]]))
    rom.write_bytes(0x10de4c, bytearray([enemy_ids[world.acting_enemy_list["Ghost of Starman"]]]))
    rom.write_bytes(0x10de4f, bytearray([enemy_ids[world.acting_enemy_list["Final Starman"]]]))
    rom.write_bytes(0x10de52, bytearray([enemy_ids[world.acting_enemy_list["Nuclear Reactor Robot"]]]))
    rom.write_bytes(0x10de56, bytearray([enemy_ids[world.acting_enemy_list["Bionic Kraken"]]]))
    rom.write_bytes(0x10de5a, bytearray([enemy_ids[world.acting_enemy_list["Mobile Sprout"]]]))
    rom.write_bytes(0x10de5d, bytearray([enemy_ids[world.acting_enemy_list["Ramblin' Evil Mushroom"]]]))
    rom.write_bytes(0x10de61, bytearray([enemy_ids[world.acting_enemy_list["Mobile Sprout"]]]))
    rom.write_bytes(0x10de65, bytearray([enemy_ids[world.acting_enemy_list["Mobile Sprout"]]]))
    rom.write_bytes(0x10de69, bytearray([enemy_ids[world.acting_enemy_list["Insane Cultist"]]]))
    rom.write_bytes(0x10de6d, bytearray([enemy_ids[world.acting_enemy_list["Insane Cultist"]]]))
    rom.write_bytes(0x10de71, bytearray([enemy_ids[world.acting_enemy_list["Zombie Possessor"]]]))
    rom.write_bytes(0x10de75, bytearray([enemy_ids[world.acting_enemy_list["Mr. Batty"]]]))
    rom.write_bytes(0x10de79, bytearray([enemy_ids[world.acting_enemy_list["Mr. Batty"]]]))
    rom.write_bytes(0x10de7c, bytearray([enemy_ids[world.acting_enemy_list["Zombie Possessor"]]]))
    rom.write_bytes(0x10de80, bytearray([enemy_ids[world.acting_enemy_list["Skelpion"]]]))
    rom.write_bytes(0x10de84, bytearray([enemy_ids[world.acting_enemy_list["Mad Taxi"]]]))
    rom.write_bytes(0x10de88, bytearray([enemy_ids[world.acting_enemy_list["Criminal Caterpillar"]]]))
    rom.write_bytes(0x10de8c, bytearray([enemy_ids[world.acting_enemy_list["Master Criminal Worm"]]]))
    rom.write_bytes(0x10de94, bytearray([enemy_ids[world.acting_enemy_list["Coil Snake"]]]))
    rom.write_bytes(0x10de98, bytearray([enemy_ids[world.acting_enemy_list["Coil Snake"]]]))
    rom.write_bytes(0x10de9c, bytearray([enemy_ids[world.acting_enemy_list["Mole Playing Rough"]]]))
    rom.write_bytes(0x10dea0, bytearray([enemy_ids[world.acting_enemy_list["Mole Playing Rough"]]]))
    rom.write_bytes(0x10dea4, bytearray([enemy_ids[world.acting_enemy_list["Mole Playing Rough"]]]))
    rom.write_bytes(0x10dea8, bytearray([enemy_ids[world.acting_enemy_list["Skate Punk"]]]))
    rom.write_bytes(0x10deab, bytearray([enemy_ids[world.acting_enemy_list["Pogo Punk"]]]))
    rom.write_bytes(0x10deae, bytearray([enemy_ids[world.acting_enemy_list["Yes Man Junior"]]]))
    rom.write_bytes(0x10deb2, bytearray([enemy_ids[world.acting_enemy_list["Pogo Punk"]]]))
    rom.write_bytes(0x10deb6, bytearray([enemy_ids[world.acting_enemy_list["Yes Man Junior"]]]))
    rom.write_bytes(0x10deba, bytearray([enemy_ids[world.acting_enemy_list["Insane Cultist"]]]))
    rom.write_bytes(0x10debe, bytearray([enemy_ids[world.acting_enemy_list["Unassuming Local Guy"]]]))
    rom.write_bytes(0x10dec2, bytearray([enemy_ids[world.acting_enemy_list["Insane Cultist"]]]))
    rom.write_bytes(0x10dec5, bytearray([enemy_ids[world.acting_enemy_list["Spiteful Crow"]]]))
    rom.write_bytes(0x10dec9, bytearray([enemy_ids[world.acting_enemy_list["Slimy Little Pile"]]]))
    rom.write_bytes(0x10decd, bytearray([enemy_ids[world.acting_enemy_list["Enraged Fire Plug"]]]))
    rom.write_bytes(0x10ded1, bytearray([enemy_ids[world.acting_enemy_list["Robo-pump"]]]))
    rom.write_bytes(0x10ded5, bytearray([enemy_ids[world.acting_enemy_list["Abstract Art"]]]))
    rom.write_bytes(0x10ded9, bytearray([enemy_ids[world.acting_enemy_list["Sentry Robot"]]]))
    rom.write_bytes(0x10dedd, bytearray([enemy_ids[world.acting_enemy_list["Shattered Man"]]]))
    rom.write_bytes(0x10dee1, bytearray([enemy_ids[world.acting_enemy_list["Guardian Hieroglyph"]]]))
    rom.write_bytes(0x10dee5, bytearray([enemy_ids[world.acting_enemy_list["Lethal Asp Hieroglyph"]]]))
    rom.write_bytes(0x10dee9, bytearray([enemy_ids[world.acting_enemy_list["Mad Duck"]]]))
    rom.write_bytes(0x10deed, bytearray([enemy_ids[world.acting_enemy_list["Worthless Protoplasm"]]]))
    rom.write_bytes(0x10def1, bytearray([enemy_ids[world.acting_enemy_list["Rowdy Mouse"]]]))
    rom.write_bytes(0x10dF00, bytearray([enemy_ids[world.acting_enemy_list["Black Antoid (2)"]]]))
    rom.write_bytes(0x10df04, bytearray([enemy_ids[world.acting_enemy_list["Cop"]]]))
    rom.write_bytes(0x10df1b, bytearray([enemy_ids[world.acting_enemy_list["Slimy Little Pile"]]]))
    rom.write_bytes(0x10df22, bytearray([enemy_ids[world.acting_enemy_list["Tough Mobile Sprout"]]]))
    rom.write_bytes(0x10df31, bytearray([enemy_ids[world.acting_enemy_list["Insane Cultist"]]]))
    rom.write_bytes(0x10df4c, bytearray([enemy_ids[world.acting_enemy_list["Starman"]]]))
    rom.write_bytes(0x10df4f, bytearray([enemy_ids[world.acting_enemy_list["Starman Super"]]]))
    rom.write_bytes(0x10df5e, bytearray([enemy_ids[world.acting_enemy_list["Even Slimier Little Pile"]]]))

    # Calls for help

    if not world.options.randomize_enemy_attacks:
        rom.write_bytes(0x15A601, bytearray([enemy_ids[world.acting_enemy_list["Care Free Bomb"]]]))  # Loaded Dice
        rom.write_bytes(0x15A602, bytearray([enemy_ids[world.acting_enemy_list["Beautiful UFO"]]]))
        rom.write_bytes(0x15A603, bytearray([enemy_ids[world.acting_enemy_list["High-class UFO"]]]))
        rom.write_bytes(0x15A604, bytearray([enemy_ids[world.acting_enemy_list["Care Free Bomb"]]]))

        rom.write_bytes(0x15DD73, bytearray([enemy_ids[world.acting_enemy_list["Electro Swoosh"]]]))  # Loaded Dice 2
        rom.write_bytes(0x15DD74, bytearray([enemy_ids[world.acting_enemy_list["Fobby"]]]))
        rom.write_bytes(0x15DD75, bytearray([enemy_ids[world.acting_enemy_list["Uncontrollable Sphere"]]]))
        rom.write_bytes(0x15DD76, bytearray([enemy_ids[world.acting_enemy_list["Electro Swoosh"]]]))

        rom.write_bytes(0x15AD5B, bytearray([enemy_ids[world.acting_enemy_list["Yes Man Junior"]]]))  # Skate Punk
        rom.write_bytes(0x15AD5C, bytearray([enemy_ids[world.acting_enemy_list["Pogo Punk"]]]))

        rom.write_bytes(0x15AED2, bytearray([enemy_ids[world.acting_enemy_list["Starman"]]]))  # S Super

    rom.write_bytes(0x15B108, bytearray([enemy_ids[world.acting_enemy_list["Starman Super"]]]))  # SDX
    rom.write_bytes(0x15DA86, bytearray([enemy_ids[world.acting_enemy_list["Starman Super"]]]))

    rom.write_bytes(0x15DC5B, bytearray([enemy_ids[world.acting_enemy_list["Slimy Little Pile"]]]))  # Belch
    rom.write_bytes(0x15B801, bytearray([enemy_ids[world.acting_enemy_list["Slimy Little Pile"]]]))

    rom.write_bytes(0x15DD15, bytearray([enemy_ids[world.acting_enemy_list["Even Slimier Little Pile"]]]))  # Barf

    rom.write_bytes(0x0F92F4, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Skate Punk"]]))
    rom.write_bytes(0x0F9305, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Pogo Punk"]]))
    rom.write_bytes(0x0F8997, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Yes Man Junior"]]))
    rom.write_bytes(0x0F89A8, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Pogo Punk"]]))
    rom.write_bytes(0x0F89B9, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Skate Punk"]]))
    rom.write_bytes(0x0F89CA, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Pogo Punk"]]))
    rom.write_bytes(0x0F89DB, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Yes Man Junior"]]))
    rom.write_bytes(0x0F89FD, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Skate Punk"]]))

    rom.write_bytes(0x0FA2A0, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Insane Cultist"]]))
    rom.write_bytes(0x0FA2B1, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Insane Cultist"]]))
    rom.write_bytes(0x0FA2C2, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Insane Cultist"]]))
    rom.write_bytes(0x0FA2D3, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Insane Cultist"]]))
    rom.write_bytes(0x0FA2E4, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Insane Cultist"]]))
    rom.write_bytes(0x0FA2F5, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Insane Cultist"]]))
    rom.write_bytes(0x0FA306, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Insane Cultist"]]))
    rom.write_bytes(0x0FA317, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Insane Cultist"]]))
    rom.write_bytes(0x0FA328, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Insane Cultist"]]))
    rom.write_bytes(0x0FA339, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Insane Cultist"]]))
    rom.write_bytes(0x0FA34A, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Insane Cultist"]]))
    rom.write_bytes(0x0FA35B, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Insane Cultist"]]))
    rom.write_bytes(0x0FA36C, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Insane Cultist"]]))
    rom.write_bytes(0x0FA37D, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Insane Cultist"]]))
    rom.write_bytes(0x0FA38E, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Insane Cultist"]]))
    rom.write_bytes(0x0FA39F, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Insane Cultist"]]))
    rom.write_bytes(0x0FA427, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Insane Cultist"]]))
    rom.write_bytes(0x0FA6BE, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Insane Cultist"]]))
    rom.write_bytes(0x0FA6CF, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Insane Cultist"]]))
    rom.write_bytes(0x0FA6E0, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Spiteful Crow"]]))
    rom.write_bytes(0x0FA4E2, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Unassuming Local Guy"]]))
    rom.write_bytes(0x0FA3B0, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Insane Cultist"]]))
    rom.write_bytes(0x0FA3C1, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Insane Cultist"]]))
    rom.write_bytes(0x0FA3D2, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Insane Cultist"]]))

    rom.write_bytes(0x0FCE85, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Shattered Man"]]))
    rom.write_bytes(0x0FCE96, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Shattered Man"]]))

    rom.write_bytes(0x0FB6D0, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Rowdy Mouse"]]))
    rom.write_bytes(0x0FB6E1, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Rowdy Mouse"]]))
    rom.write_bytes(0x0FB6AE, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Worthless Protoplasm"]]))
    rom.write_bytes(0x0FB6BF, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Worthless Protoplasm"]]))
    rom.write_bytes(0x0FB68C, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Mad Duck"]]))
    rom.write_bytes(0x0FB69D, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Mad Duck"]]))

    rom.write_bytes(0x0FD716, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Guardian Hieroglyph"]]))
    rom.write_bytes(0x0FD727, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Guardian Hieroglyph"]]))
    rom.write_bytes(0x0FD738, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Lethal Asp Hieroglyph"]]))
    rom.write_bytes(0x0FD749, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Lethal Asp Hieroglyph"]]))
    rom.write_bytes(0x0FD75A, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Guardian Hieroglyph"]]))
    rom.write_bytes(0x0FD76B, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Guardian Hieroglyph"]]))
    rom.write_bytes(0x0FD77C, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Guardian Hieroglyph"]]))
    rom.write_bytes(0x0FD78D, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Lethal Asp Hieroglyph"]]))
    rom.write_bytes(0x0FD79E, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Guardian Hieroglyph"]]))
    rom.write_bytes(0x0FD7AF, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Lethal Asp Hieroglyph"]]))
    rom.write_bytes(0x0FD7C0, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Guardian Hieroglyph"]]))
    rom.write_bytes(0x0FD7D1, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Lethal Asp Hieroglyph"]]))
    rom.write_bytes(0x0FD7F3, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Guardian Hieroglyph"]]))
    rom.write_bytes(0x0FD804, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Guardian Hieroglyph"]]))
    rom.write_bytes(0x0FD815, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Guardian Hieroglyph"]]))
    rom.write_bytes(0x0FD826, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Lethal Asp Hieroglyph"]]))
    rom.write_bytes(0x0FD837, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Guardian Hieroglyph"]]))
    rom.write_bytes(0x0FD848, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Guardian Hieroglyph"]]))
    rom.write_bytes(0x0FD859, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Lethal Asp Hieroglyph"]]))
    rom.write_bytes(0x0FD86A, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Guardian Hieroglyph"]]))
    rom.write_bytes(0x0FD87B, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Guardian Hieroglyph"]]))
    rom.write_bytes(0x0FD88C, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Guardian Hieroglyph"]]))
    rom.write_bytes(0x0FD89D, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Lethal Asp Hieroglyph"]]))
    rom.write_bytes(0x0FD8AE, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Lethal Asp Hieroglyph"]]))

    rom.write_bytes(0x0F8E1B, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Cop"]]))
    rom.write_bytes(0x0F8E2C, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Cop"]]))
    rom.write_bytes(0x0F8E5F, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Cop"]]))
    rom.write_bytes(0x0F8E70, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Cop"]]))
    rom.write_bytes(0x0F8E81, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Cop"]]))
    rom.write_bytes(0x0F8E92, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Cop"]]))
    rom.write_bytes(0x0F8EA3, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Cop"]]))
    rom.write_bytes(0x0F9316, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Cop"]]))
    rom.write_bytes(0x0F9327, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Cop"]]))

    rom.write_bytes(0x0FE409, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Robo-pump"]]))
    rom.write_bytes(0x0FE491, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Robo-pump"]]))
    rom.write_bytes(0x0FE43C, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Abstract Art"]]))

    rom.write_bytes(0x0FD9F1, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Mad Duck"]]))
    rom.write_bytes(0x0FDA02, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Mad Duck"]]))
    rom.write_bytes(0x0FDA13, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Mad Duck"]]))
    rom.write_bytes(0x0FDA24, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Slimy Little Pile"]]))
    rom.write_bytes(0x0FDA35, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Slimy Little Pile"]]))
    rom.write_bytes(0x0FDA46, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Slimy Little Pile"]]))
    rom.write_bytes(0x0FDA57, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Gruff Goat"]]))
    rom.write_bytes(0x0FDA68, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Gruff Goat"]]))

    rom.write_bytes(0x0FB736, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Slimy Little Pile"]]))
    rom.write_bytes(0x0FB747, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Slimy Little Pile"]]))
    rom.write_bytes(0x0FB758, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Slimy Little Pile"]]))
    rom.write_bytes(0x0FB769, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Slimy Little Pile"]]))
    rom.write_bytes(0x0FB77A, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Slimy Little Pile"]]))

    rom.write_bytes(0x0FC3E5, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Sentry Robot"]]))
    rom.write_bytes(0x0FC3F6, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Sentry Robot"]]))
    rom.write_bytes(0x0FC407, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Sentry Robot"]]))
    rom.write_bytes(0x0FC418, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Sentry Robot"]]))
    rom.write_bytes(0x0FC48F, struct.pack("H", world.enemy_sprites[world.acting_enemy_list["Sentry Robot"]]))

    dungeon_zoo = [
        "Mad Duck",
        "Gruff Goat",
        "Slimy Little Pile"
    ]

    name_addresses = [
        0x330544,
        0x330555,
        0x330566
    ]

    desc_addresses = [
        0x33054B,
        0x33055C,
        0x33056D
    ]

    normal_pointers = {
        "Mad Duck": 0xC8796C,
        "Gruff Goat": 0xC879A3,
        "Slimy Little Pile": 0xC87A31
    }

    pointer = 0x313000

    if world.enemy_sprites[world.acting_enemy_list["Insane Cultist"]] not in can_walkthrough:
        rom.write_bytes(0x0983D2, bytearray([0x1f, 0x1e, 0x7A, 0x01, 0x00, 0x00, 0x00, 0x00]))
        rom.write_bytes(0x098459, bytearray([0x1f, 0x1e, 0x7B, 0x01, 0x00, 0x00, 0x00, 0x00]))
        rom.write_bytes(0x0984D1, bytearray([0x1f, 0x1e, 0x7C, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                             0x00, 0x00]))
        rom.write_bytes(0x09855F, bytearray([0x1f, 0x1e, 0x7D, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                             0x00, 0x00]))
        rom.write_bytes(0x0985CE, bytearray([0x1f, 0x1e, 0x7E, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                             0x00, 0x00]))
        rom.write_bytes(0x098625, bytearray([0x1f, 0x1e, 0x7F, 0x01, 0x00, 0x00, 0x00, 0x00]))
        rom.write_bytes(0x09869E, bytearray([0x1f, 0x1e, 0x80, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                             0x00, 0x00]))

        rom.write_bytes(0x098375, bytearray([0x44]))
        rom.write_bytes(0x098425, bytearray([0x44]))
        rom.write_bytes(0x098480, bytearray([0x44]))
        rom.write_bytes(0x098518, bytearray([0x44]))
        rom.write_bytes(0x098599, bytearray([0x44]))
        rom.write_bytes(0x098603, bytearray([0x44]))
        rom.write_bytes(0x09864C, bytearray([0x44]))

    for i in range(3):

        name = text_encoder(world.acting_enemy_list[dungeon_zoo[i]].replace(" (2)", ""), 255)
        name.append(0x02)

        if world.acting_enemy_list[dungeon_zoo[i]] not in dungeon_zoo:
            text = text_encoder(enemy_descriptions[world.acting_enemy_list[dungeon_zoo[i]]], 255)
            text.append(0x02)
        else:
            text = text_encoder("ERROR", 255)
        rom.write_bytes(pointer, name)
        rom.write_bytes(name_addresses[i], struct.pack("I", pointer + 0xC00000))
        pointer += len(name)
        rom.write_bytes(pointer, text)
        if world.acting_enemy_list[dungeon_zoo[i]] not in dungeon_zoo:
            rom.write_bytes(desc_addresses[i], struct.pack("I", pointer + 0xC00000))
        else:
            rom.write_bytes(desc_addresses[i], struct.pack("I",
                                                           normal_pointers[world.acting_enemy_list[dungeon_zoo[i]]]))
        pointer += len(text)
    # Todo; action scripts for npc enemies?
