

VERSION = "0.3.0"
ROM_HASH = "f2dc6c4e093e4f8c6cbea80e8dbd62cb"

STARTING_FLAGS = [
    # Starting flags (these are in the same memory block so can be simplified, but it's called once and this is
    # easier to bugfix)
    [0x1B557C, 0xEF],
    [0x1B557D, 0x34],
    [0x1B557E, 0x2E],
    [0x1B557F, 0x03],
    [0x1B5580, 0xED],
    [0x1B5581, 0xB0],
    [0x1B5582, 0x40],
    [0x1B5583, 0xAB],
    [0x1B5584, 0xFF],
    [0x1B5585, 0xFB],
    [0x1B5586, 0x2F],
    [0x1B5587, 0xFC],
    [0x1B5588, 0x3B],
    [0x1B5589, 0x00],
    [0x1B558A, 0x04],
    [0x1B558B, 0x00],
    [0x1B558C, 0xD9],
    [0x1B558D, 0x4F],
    [0x1B558E, 0x12],
    [0x1B558F, 0x04],
    [0x1B5590, 0x02],
    [0x1B5591, 0x7E],
    [0x1B5592, 0x04],
    [0x1B5593, 0xEA],
    [0x1B5594, 0x47],
    [0x1B5595, 0x00],
    [0x1B5596, 0xF8],
    [0x1B5597, 0xDF],
    [0x1B5598, 0x35],
    [0x1B5599, 0xE0],
    [0x1B559A, 0x10],
    [0x1B559B, 0xE0],
    [0x1B559C, 0x4E],
    [0x1B559D, 0xF9],
    [0x1B559E, 0x0F],
    [0x1B559F, 0x05],
    [0x1B55A0, 0x31],
    [0x1B55A1, 0x00],
    [0x1B55A2, 0x60],
    [0x1B55A3, 0x20],
    [0x1B55A4, 0x26],
    [0x1B55A5, 0xCC],
    [0x1B55A6, 0x00],
    [0x1B55A7, 0xC8],
    [0x1B55A8, 0x1F],
    [0x1B55A9, 0x00],
    [0x1B55AA, 0x08],
    [0x1B55AB, 0x48],
    [0x1B55AC, 0x78],
    [0x1B55AD, 0x00],
    [0x1B55AE, 0x00],
    [0x1B55AF, 0x00],
    # Set item can use flags
    [0x1BA6BC, 0x01],
    [0x1BA6BE, 0x01],
    [0x1BA6C4, 0x01],
    [0x1BA6C8, 0x01],
    # Starting items, Phantom Hourglass
    [0x1BA648, 0x01],
    # Show treasure/ship part prices
    [0x1BA658, 0xFF],
    [0x1BA659, 0xFF],
    [0x1BA65A, 0xFF],
    [0x1BA65B, 0xFF],
    [0x1BA65C, 0xFF],
    [0x1BA65D, 0xFF],
    [0x1BA65E, 0xFF],
    [0x1BA65F, 0xFF],
    [0x1BA660, 0xFF],
    [0x1BA664, 0xFF],
    # Starting treasure at 0 so incr works properly
    [0x1BA5AC, 0],
    [0x1BA5AD, 0],
    [0x1BA5AE, 0],
    [0x1BA5AF, 0],
    [0x1BA5B0, 0],
    [0x1BA5B1, 0],
    [0x1BA5B2, 0],
    [0x1BA5B3, 0],
]

STARTING_FROG_FLAGS = [
    [0x1B55A2, 0xE0],
    [0x1B55A3, 0x3F]
]

FOG_SETTINGS_FLAGS = [
    [[0x1B5582, 0xC0], [0x1B55AB, 0x58]],
    [],
    [[0x1B557E, 0x3E]]
]

STAGE_FLAGS = {
    11: [0xC4, 0xDC, 0x06, 0x00],  # Mercay
    39: [0x40, 0x00, 0x00, 0x00],  # Mountain Passage
    37: [0xFE, 0xBE, 0xFB, 0xAF],  # TotOK
    0:  [0x82, 0xFC, 0x66, 0xED],  # Sea
    13: [0xEC, 0x18, 0x17, 0x00],  # Ember
    28: [0x8E, 0xB9, 0x00, 0x00],  # ToF
    12: [0x34, 0x01, 0x00, 0x00],  # Molida
    14: [0x02, 0x02, 0x00, 0x00],  # Gusts
    29: [0x00, 0x10, 0x00, 0x00],  # ToW
    30: [0x00, 0x00, 0x02, 0x00],  # ToC
    41: [0xC2, 0x10, 0xED, 0x00],  # Ghost Ship
    16: [0x84, 0x13, 0x00, 0xE0],  # Goron Island
    32: [0x00, 0x00, 0x30, 0xF0],  # Goron Temple
    15: [0x00, 0x3C, 0x00, 0x40],  # Isle of Frost
    31: [0x00, 0x00, 0xD0, 0x00],  # Temple of Ice
    21: [0xB6, 0x01, 0x00, 0x00],  # Isle of the Dead
    17: [0x12, 0x4C, 0x43, 0x00],  # Isle of ruins
    18: [0x10, 0x4C, 0x43, 0x00],  # Isle of ruins
    36: [0x20, 0x00, 0x00, 0x00],  # Bremeur's Temple
    33: [0x00, 0x26, 0x00, 0x00],  # Mutoh's Temple
}

SKIP_OCEAN_FIGHTS_FLAGS = [0x86, 0xFC, 0x66, 0xFD]
SPAWN_B3_REAPLING_FLAGS = [0xC2, 0x10, 0xED, 0x08]

STAGES = {
    0: "Sea",
    1: "Cannon Game",
    2: "Fishing",
    3: "Salvage",
    4: "Linebeck's Ship",
    5: "Beedle's Ship",
    6: "Man of Smiles' Ship",
    7: "PoRL's Ship",
    8: "SS Wayfarer",
    9: "Wayaway's Ship",
    10: "Nyave's Ship",
    11: "Mercay Island",
    12: "Molida Island",
    13: "Isle of Ember",
    14: "Isle of Gust",
    15: "Isle of Frost",
    16: "Goron Island",
    17: "Isle of Ruins (High Water)",
    18: "Isle of Ruins (Low Water)",
    19: "Cannon Island",
    20: "Bannan Island",
    21: "Isle of the Dead",
    22: "Zauz's Island",
    23: "Spirit Island",
    24: "Harrow Island",
    25: "Maze Island",
    26: "Uncharted Island",
    27: "Dee Ess Island",
    28: "Temple of Fire",
    29: "Temple of Wind",
    30: "Temple of Courage",
    31: "Temple of Ice",
    32: "Goron Temple",
    33: "Mutoh's Temple",
    34: "Doylan's Temple",
    35: "Max's Temple",
    36: "Bremeur's Temple",
    37: "Temple of the Ocean King",
    38: "Temple of the Ocean King Entrance",
    39: "Mountain Passage",
    40: "Cannon Island Cave",
    41: "Ghost Ship",
    42: "Cyclok",
    43: "Blaaz",
    44: "Crayk",
    45: "Gleeok",
    46: "Dongorongo",
    47: "Eox",
    48: "Cubus Sisters",
    49: "Bellum",
    50: "Bellum's Ghost Ship",
    51: "Bellumbeck",
    0x36: "Credits",

}

ISLANDS = [
    "Mercay Island",
    "Cannon Island",
    "Isle of Ember",
    "Molida Island",
    "Spirit Island",
    "Isle of Gust",
    "Bannan Island",
    "Zauz's Island",
    "Uncharted Island",
    "Goron Island",
    "Harrow Island",
    "Dee Ess Island",
    "Isle of Frost",
    "Isle of the Dead",
    "Maze Island",
    "Isle of Ruins"
]

SEA_REGIONS = [
    "Ocean SW",
    "Ocean NW",
    "Ocean NE",
    "Ocean SE",
    "Ocean Unspecific"
]

SEA_CHARTS = [
    "SW Sea Chart",
    "NW Sea Chart",
    "SE Sea Chart",
    "NE Sea Chart",
]

TREASURE_MAPS = [
    "Treasure Map #1 (Molida SW)",
    "Treasure Map #2 (Mercay NE)",
    "Treasure Map #3 (Gusts SW)",
    "Treasure Map #4 (Bannan SE)",
    "Treasure Map #5 (Molida N)",
    "Treasure Map #6 (Bannan W)",
    "Treasure Map #7 (Gusts E)",
    "Treasure Map #8 (Mercay SE)",
    "Treasure Map #9 (Cannon W)",
    "Treasure Map #10 (Gusts SE)",
    "Treasure Map #11 (Gusts N)",
    "Treasure Map #12 (Dee Ess N)",
    "Treasure Map #13 (Harrow E)",
    "Treasure Map #14 (Goron NW)",
    "Treasure Map #15 (Goron W)",
    "Treasure Map #16 (Goron NE)",
    "Treasure Map #17 (Frost S)",
    "Treasure Map #18 (Cannon S)",
    "Treasure Map #19 (Gusts NE)",
    "Treasure Map #20 (Bannan E)",
    "Treasure Map #21 (Molida NW)",
    "Treasure Map #22 (Harrow S)",
    "Treasure Map #23 (Frost NW)",
    "Treasure Map #24 (Ruins W)",
    "Treasure Map #25 (Dead E)",
    "Treasure Map #26 (Ruins SW)",
    "Treasure Map #27 (Maze E)",
    "Treasure Map #28 (Ruins NW)",
    "Treasure Map #29 (Maze W)",
    "Treasure Map #30 (Ruins S)",
    "Treasure Map #31 (Dead S)",
]


ITEM_GROUPS: dict[str, set[str]] = {
    "Small Keys": {
        "Small Key (Mountain Passage)",
        "Small Key (Temple of the Ocean King)",
        "Small Key (Temple of Fire)",
        "Small Key (Temple of Wind)",
        "Small Key (Temple of Courage)",
        "Small Key (Temple of Ice)",
        "Small Key (Mutoh's Temple)"
    },
    "Vanilla Metals": {
        "Crimzonine",
        "Azurine",
        "Aquanine"
    },
    "Custom Metals": {
        "Verdanine",
        "Lavendine",
        "Amberine",
        "Vermilline",
        "Burgundine",
        "Crystaline",
        "Carrotine",
        "Olivine",
        "Chartreusine",
        "Violetine",
        "Ceruline",
        "Fuchsianine",
        "Saffronine",
        "Viridine",
        "Sepianine",
        "Apricotine",
        "Scarletine",
        "Coraline",
        "Magentine",
        "Cyanine",
        "Mauvine",
        "Lilacine",
        "Indigorine",
        "Junipine",
        "Limeinine",
        "Mintine",
        "Umberine",
    },
    "Treasure Items": {
        "Treasure: Pink Coral",
        "Treasure: White Pearl Loop",
        "Treasure: Dark Pearl Loop",
        "Treasure: Zora Scale",
        "Treasure: Goron Amber",
        "Treasure: Ruto Crown",
        "Treasure: Helmaroc Plume",
        "Treasure: Regal Ring"
    },
    "Ammo Refills": {
        "Refill: Bombs",
        "Refill: Arrows",
        "Refill: Bombchus",
        "Refill: Health",
    },
    "Treasure Maps": set(TREASURE_MAPS),
    "Items With Ammo": {
        "Bombs (Progressive)",
        "Bombchus (Progressive)",
        "Bow (Progressive)",
    },
    "Items Without Ammo": {
        "Boomerang",
        "Grappling Hook",
        "Shovel",
        "Hammer",
    },
    "Spirits": {
        "Spirit of Power (Progressive)",
        "Spirit of Wisdom (Progressive)",
        "Spirit of Courage (Progressive)",
    },
    "Ship Items": {
        "Cannon",
        "Salvage Arm",
        "Fishing Rod",
        "Big Catch Lure",
        "Cyclone Slate",
    },
    "Fish": {
        "Fish: Skippyjack",
        "Fish: Toona",
        "Fish: Loovar",
        "Fish: Rusty Swordfish",
        "Fish: Legendary Neptoona",
        "Fish: Stowfish"
    },
    "Sea Charts": set(SEA_CHARTS),
    "Upgrades": {
        "Heart Container",
        "Sand of Hours",
        "Swordsman's Scroll",
    },
    "Rupees": {
        "Green Rupee (1)",
        "Blue Rupee (5)",
        "Red Rupee (20)",
        "Big Green Rupee (100)",
        "Big Red Rupee (200)",
        "Gold Rupee (300)",
        "Rupoor (-10)",
        "Big Rupoor (-50)",
        "Pre-Alpha Rupee (5000)",
    },
    "Boss Keys": {
        "Boss Key (Temple of Fire)",
        "Boss Key (Temple of Wind)",
        "Boss Key (Temple of Courage)",
        "Boss Key (Goron Temple)",
        "Boss Key (Temple of Ice)",
        "Boss Key (Mutoh's Temple)",
    },
    "Single Spirit Gems": {
        "Power Gem",
        "Wisdom Gem",
        "Courage Gem",
    },
    "Spirit Gem Packs": {
        "Power Gem Pack",
        "Wisdom Gem Pack",
        "Courage Gem Pack",
    },

    "Unique Crystal Items": {
        "Triangle Pedestal B8 (Temple of the Ocean King)",
        "Triangle Pedestal B9 (Temple of the Ocean King)",
        "Round Pedestal B8 (Temple of the Ocean King)",
        "Round Pedestal B9 (Temple of the Ocean King)",
        "Square Pedestal West (Temple of the Ocean King)",
        "Square Pedestal Center (Temple of the Ocean King)",
        "Square Pedestal North (Temple of Courage)",
        "Square Pedestal South (Temple of Courage)",
        "Triangle Crystal (Ghost Ship)",
        "Round Crystal (Ghost Ship)",
    },
    "Regular Crystal Items": {
        "Square Crystal (Temple of Courage)",
        "Triangle Crystal (Ghost Ship)",
        "Round Crystal (Ghost Ship)",
        "Round Crystal (Temple of the Ocean King)",
        "Triangle Crystal (Temple of the Ocean King)",
        "Square Crystal (Temple of the Ocean King)",
    },
    "Global Crystal Items": {
        "Square Crystals",
        "Round Crystals",
        "Triangle Crystals",
    },
    "Unique Force Gems": {
        "Force Gem (B3)",
        "Force Gem (B12)",
    },
    "Force Gems": {
        "Force Gem (B3)",
        "Force Gem (B12)",
        "Force Gem"
    },
    "Collection Screen Keys": {
        "Sun Key",
        "Ghost Key",
        "King's Key",
        "Regal Necklace",
    },
    "Trade Quest Items": {
        "Hero's New Clothes",
        "Kaleidoscope",
        "Guard Notebook",
        "Wood Heart",
    },
    "Crests": {
        "Courage Crest",
        "Triforce Crest",
    },
    "Golden Frog Glyphs": {
        "Golden Frog Glyph X",
        "Golden Frog Glyph Phi",
        "Golden Frog Glyph N",
        "Golden Frog Glyph Omega",
        "Golden Frog Glyph W",
        "Golden Frog Glyph Square"
    },
    "Ships": {
#         "S.S. Linebeck",
        "Ship: Bright Ship",
        "Ship: Iron Ship",
        "Ship: Stone Ship",
        "Ship: Vintage Ship",
        "Ship: Demon Ship",
        "Ship: Tropical Ship",
        "Ship: Dignified Ship",
        "Ship: Golden Ship",
    },
    "Technical Items": {
        "Treasure",
        "Ship Part",
        "Potion",
        "Nothing!",
        "Sand of Hours (Boss)",
        "Sand of Hours (Small)",
        "Spirit of Courage (White)"
    },
    "Potions": {
        "Red Potion",
        "Purple Potion",
        "Yellow Potion",
        "Potion"
    },
    "Rupoors": {
        "Rupoor (-10)",
        "Big Rupoor (-50)",
    },
    "Swords": {
        "Sword (Progressive)",
        "Oshus' Sword",
        "Phantom Sword",
    },
}

# Combo groups
ITEM_GROUPS |= {
    "Metals":
        ITEM_GROUPS["Vanilla Metals"] |
        ITEM_GROUPS["Custom Metals"] |
        {"Additional Rare Metal"},
    "Equipable Items":
        ITEM_GROUPS["Items With Ammo"] |
        ITEM_GROUPS["Items Without Ammo"],
    "Fishing Items": {
                         "Fishing Rod",
                         "Big Catch Lure"
                     } |
                     ITEM_GROUPS["Fish"],
    "Regular Pedestal Items":
        ITEM_GROUPS["Regular Crystal Items"] |
        ITEM_GROUPS["Unique Force Gems"],
    "Unique Pedestal Items":
        ITEM_GROUPS["Unique Force Gems"] |
        ITEM_GROUPS["Unique Crystal Items"],
    "Global Pedestal Items":
        ITEM_GROUPS["Global Crystal Items"] |
        {"Force Gems"},
    "Spirit Gems":
        ITEM_GROUPS["Single Spirit Gems"] |
        ITEM_GROUPS["Spirit Gem Packs"],
}

ITEM_GROUPS |=  {
    "Shape Crystals":
        ITEM_GROUPS["Unique Crystal Items"] |
        ITEM_GROUPS["Regular Crystal Items"] |
        ITEM_GROUPS["Global Crystal Items"],
    "Pedestal Items":
        ITEM_GROUPS["Regular Pedestal Items"] |
        ITEM_GROUPS["Unique Pedestal Items"] |
        ITEM_GROUPS["Global Pedestal Items"],
    "Player Items": {
                        "Shield",
                    } | ITEM_GROUPS["Equipable Items"] |
                    ITEM_GROUPS["Swords"],
}

ITEM_GROUPS |=  {
    "Throwable Keys":
        ITEM_GROUPS["Boss Keys"] |
        ITEM_GROUPS["Pedestal Items"],
    "Keys":
        ITEM_GROUPS["Collection Screen Keys"] |
        ITEM_GROUPS["Small Keys"] |
        ITEM_GROUPS["Boss Keys"] |
        ITEM_GROUPS["Pedestal Items"],
}

STAGE_LOCATION_GROUPS = {
    "Mercay Island": [
        "Mercay Sword Chest",
        "Mercay Clear Rocks",
        "Mercay Oshus Dig",
        "Mercay Cuccoo Chest",
        "Mercay North Bonk Tree",
        "Mercay Geozard Cave Chest",
        "Mercay Geozard Cave South Chest West",
        "Mercay Geozard Cave South Chest East",
        "Mercay Freedle Tunnel Chest",
        "Mercay Freedle Island Chest",
        "Mercay Freedle Gift Item",
        "Mercay Ojibe (Docks Guy) Item",
        "Mercay Shipyard Chest",
        "Mercay Oshus Spirit Gem",
        "Mercay Oshus Phantom Sword",
        "Island Shop Power Gem",
        "Island Shop Quiver",
        "Island Shop Bombchu Bag",
        "Island Shop Heart Container",
        "TotOK Phantom Hourglass",
        "Mountain Passage Chest 1",
        "Mountain Passage Chest 2",
        "Mountain Passage Key Drop",
        "Mountain Passage Rat Key",
    ],
    "Mountain Passage": [
        "Mountain Passage Chest 1",
        "Mountain Passage Chest 2",
        "Mountain Passage Key Drop",
        "Mountain Passage Rat Key",
    ],
    "Beedle's Ship": [
        "Beedle Shop Bomb Bag",
        "Beedle Shop Wisdom Gem",
        "Masked Beedle Heart Container",
        "Masked Beedle Courage Gem",
        "Beedle Membership Bronze",
        "Beedle Membership Silver",
        "Beedle Membership Gold",
        "Beedle Membership Platinum",
        "Beedle Membership VIP",
    ],
    "Temple of the Ocean King": [
        "TotOK 1F SW Sea Chart Chest",
        "TotOK 1F Linebeck Key",
        "TotOK 1F Empty Chest",
        "TotOK B1 Small Key",
        "TotOK B1 Shoot Eye Chest",
        "TotOK B1 Phantom Chest",
        "TotOK B2 Bombchu Chest",
        "TotOK B2 Phantom Chest",
        "TotOK B2 Small Key",
        "TotOK B3 Bow Chest",
        "TotOK B3 Phantom Chest",
        "TotOK B3 NW Chest",
        "TotOK B3 SW Chest",
        "TotOK B3 SE Chest",
        "TotOK B3 Small Key",
        "TotOK B3 NW Sea Chart Chest",
        "TotOK B4 Phantom Eye Chest",
        "TotOK B4 Phantom Chest",
        "TotOK B4 Small Key",
        "TotOK B5 Alt Path Chest",
        "TotOK B5 Chest",
        "TotOK B6 Phantom Chest",
        "TotOK B6 Bow Chest",
        "TotOK B6 Courage Crest",
        "TotOK B7 North Chest",
        "TotOK B7 Peg Chest",
        "TotOK B7 Phantom Chest",
        "TotOK B8 2 Crystals Chest",
        "TotOK B8 Phantom Chest",
        "TotOK B9 NW Chest",
        "TotOK B9 Wizzrobe Chest",
        "TotOK B9 Phantom Chest",
        "TotOK B9.5 SE Sea Chart Chest",
        "TotOK B10 Hammer Switch Chest",
        "TotOK B10 Phantom Chest",
        "TotOK B10 Phantom Eye Chest",
        "TotOK B10 Small Key",
        "TotOK B11 Phantom Eye Chest",
        "TotOK B11 Phantom Chest",
        "TotOK B12 NW Chest",
        "TotOK B12 NE Chest",
        "TotOK B12 Hammer Chest",
        "TotOK B12 Kill Everything Chest",
        "TotOK B12 Phantom Chest",
        "TotOK B13 NE Sea Chart Chest",
        "GOAL: Triforce Door",
    ],
    "Ocean": [
        "Ocean SW Salvage Courage Crest",
        "Ocean SW Golden Frog X",
        "Ocean SW Golden Frog Phi",
        "Ocean NW Golden Frog N",
        "Ocean SE Golden Frog Omega",
        "Ocean SE Golden Frog W",
        "Ocean NE Golden Frog Square",
        "Ocean SW Nyave Treasure",
        "Ocean SW Nyave Trade Quest Item",
        "Ocean NW Prince of Red Lion Combat Reward",
        "Ocean NW Prince of Red Lions Trade Quest Item",
        "Ocean SE Hoiger Howgendoogen Trade Quest Item",
        "Ocean NE Man Of Smiles Item 1",
        "Ocean NE Man Of Smiles Item 2",
        "Ocean NE Man of Smiles Prize Postcard",
        "Ocean Pirate Ambush Item",
        "Beedle Shop Bomb Bag",
        "Beedle Shop Wisdom Gem",
        "Beedle Membership Bronze",
        "Beedle Membership Silver",
        "Beedle Membership Gold",
        "Beedle Membership Platinum",
        "Beedle Membership VIP",
        "Masked Beedle Heart Container",
        "Masked Beedle Courage Gem",
        "Fishing Catch Skippyjack",
        "Fishing Catch Toona",
        "Fishing Catch Loovar",
        "Fishing Catch Rusty Swordfish",
        "Fishing Catch Legendary Neptoona",
        "Fishing Catch Stowfish",
    ],
    "Open Ocean": [
        "Ocean SW Salvage Courage Crest",
        "Ocean SW Golden Frog X",
        "Ocean SW Golden Frog Phi",
        "Ocean NW Golden Frog N",
        "Ocean SE Golden Frog Omega",
        "Ocean SE Golden Frog W",
        "Ocean NE Golden Frog Square",
        "Fishing Catch Skippyjack",
        "Fishing Catch Toona",
        "Fishing Catch Loovar",
        "Fishing Catch Rusty Swordfish",
        "Fishing Catch Legendary Neptoona",
        "Fishing Catch Stowfish",
    ],
    "Ocean SW": [
        "Ocean SW Salvage Courage Crest",
        "Ocean SW Golden Frog X",
        "Ocean SW Golden Frog Phi",
        "Ocean SW Nyave Treasure",
        "Ocean SW Nyave Trade Quest Item",
        "Ocean SW Salvage #1 Molida SW",
        "Ocean SW Salvage #2 Mercay NE",
		"Ocean SW Salvage #5 Molida N",
		"Ocean SW Salvage #8 Mercay SE",
        "Ocean SW Salvage #9 Cannon W",
		"Ocean SW Salvage #18 Cannon S",
		"Ocean SW Salvage #21 Molida NW",
    ],
    "Ocean NW": [
        "Ocean NW Golden Frog N",
        "Ocean NW Prince of Red Lion Combat Reward",
        "Ocean NW Prince of Red Lions Trade Quest Item",
		"Ocean NW Salvage #3 Gusts SW",
        "Ocean NW Salvage #4 Bannan SE",
		"Ocean NW Salvage #6 Bannan W",
        "Ocean NW Salvage #7 Gusts E",
		"Ocean NW Salvage #10 Gusts SE",
        "Ocean NW Salvage #11 Gusts N",
		"Ocean NW Salvage #19 Gusts NE",
        "Ocean NW Salvage #20 Bannan E",
    ],
    "Ocean SE": [
        "Ocean SE Golden Frog Omega",
        "Ocean SE Golden Frog W",
        "Ocean SE Hoiger Howgendoogen Trade Quest Item",
		"Ocean SE Salvage #12 Dee Ess N",
        "Ocean SE Salvage #13 Harrow E",
        "Ocean SE Salvage #14 Goron NW",
        "Ocean SE Salvage #15 Goron W",
        "Ocean SE Salvage #16 Goron NE",
        "Ocean SE Salvage #17 Frost S",
		"Ocean SE Salvage #22 Harrow S",
        "Ocean SE Salvage #23 Frost NW",
    ],
    "Ocean NE": [
        "Ocean NE Golden Frog Square",
        "Ocean NE Man Of Smiles Item 1",
        "Ocean NE Man Of Smiles Item 2",
        "Ocean NE Man of Smiles Prize Postcard",
		"Ocean NE Salvage #24 Ruins W",
        "Ocean NE Salvage #25 Dead E",
        "Ocean NE Salvage #26 Ruins SW",
        "Ocean NE Salvage #27 Maze E",
        "Ocean NE Salvage #28 Ruins NW",
        "Ocean NE Salvage #29 Maze W",
        "Ocean NE Salvage #30 Ruins S",
        "Ocean NE Salvage #31 Dead S",
    ],
    "Ocean Unspecific": [
        "Ocean Pirate Ambush Item",
        "Beedle Shop Bomb Bag",
        "Beedle Shop Wisdom Gem",
        "Masked Beedle Heart Container",
        "Masked Beedle Courage Gem",
        "Fishing Catch Skippyjack",
        "Fishing Catch Toona",
        "Fishing Catch Loovar",
        "Fishing Catch Rusty Swordfish",
        "Fishing Catch Legendary Neptoona",
        "Fishing Catch Stowfish",
        "Beedle Membership Bronze",
        "Beedle Membership Silver",
        "Beedle Membership Gold",
        "Beedle Membership Platinum",
        "Beedle Membership VIP",
    ],
    "Traveller Ships": [
        "Ocean SW Nyave Treasure",
        "Ocean SW Nyave Trade Quest Item",
        "Ocean NW Prince of Red Lion Combat Reward",
        "Ocean NW Prince of Red Lions Trade Quest Item",
        "Ocean SE Hoiger Howgendoogen Trade Quest Item",
        "Ocean NE Man Of Smiles Item 1",
        "Ocean NE Man Of Smiles Item 2",
        "Ocean NE Man of Smiles Prize Postcard",
    ],
    "Ships": [
        "Ocean SW Nyave Treasure",
        "Ocean SW Nyave Trade Quest Item",
        "Ocean NW Prince of Red Lion Combat Reward",
        "Ocean NW Prince of Red Lions Trade Quest Item",
        "Ocean SE Hoiger Howgendoogen Trade Quest Item",
        "Ocean NE Man Of Smiles Item 1",
        "Ocean NE Man Of Smiles Item 2",
        "Ocean NE Man of Smiles Prize Postcard",
        "Ocean Pirate Ambush Item",
        "Beedle Shop Bomb Bag",
        "Beedle Shop Wisdom Gem",
        "Masked Beedle Heart Container",
        "Masked Beedle Courage Gem",
        "Beedle Membership Bronze",
        "Beedle Membership Silver",
        "Beedle Membership Gold",
        "Beedle Membership Platinum",
        "Beedle Membership VIP",
    ],
    "Nyave's Ship": [
        "Ocean SW Nyave Treasure",
        "Ocean SW Nyave Trade Quest Item",
    ],
    "Cannon Island": [
        "Cannon Island Bee Chest",
        "Cannon Island Cliff Chest",
        "Cannon Island Bonk Tree",
        "Cannon Island East Dig",
        "Cannon Island Cannon",
        "Cannon Island Salvage Arm",
        "Cannon Island SE Dig",
        "Cannon Island Bee Dig",
        "Cannon Island Cave Chest",
    ],
    "Isle of Ember": [
        "Isle of Ember Astrid's Basement Dig",
        "Isle of Ember Grapple Chest",
        "Isle of Ember Summit Dig",
        "Isle of Ember Summit Chest",
        "Isle of Ember Astrid after Fire Temple",
    ],
    "Temple of Fire": [
        "Temple of Fire 1F Keese Chest",
        "Temple of Fire 1F Maze Chest",
        "Temple of Fire 2F Boomerang Chest",
        "Temple of Fire 2F Fire Keese Chest",
        "Temple of Fire 2F Rat Key",
        "Temple of Fire 3F Key Drop",
        "Temple of Fire 3F Boss Key Chest",
        "Blaaz Heart Container",
        "Blaaz Boss Reward",
    ],
    "Blaaz": [
        "Blaaz Heart Container",
        "Blaaz Boss Reward",
    ],
    "Molida Island": [
        "Molida Island 2nd House Chest",
        "Molida Island Romanos Tree Dig",
        "Molida Cave Wayfarer Hideaway Chest",
        "Molida Cave Grapple Chest",
        "Molida Cave Geozard Dig",
        "Molida Cave Shovel Chest",
        "Molida Cave Shovel Room Dig",
        "Molida Island Cliff Chest",
        "Molida Island Cuccoo Grapple Tree Dig",
        "Molida Island North Dig Chest",
        "Molida Island North Grapple Chest",
        "Molida Archery 1700",
        "Molida Archery 2000",
        "Molida Island Cuccoo Grapple Small Island Dig",
    ],
    "Temple of Courage": [
        "Temple of Courage 1F Bomb Alcove Chest",
        "Temple of Courage 1F Raised Platform Chest",
        "Temple of Courage 1F Map Room Chest East",
        "Temple of Courage 1F Map Room Chest West",
        "Temple of Courage 1F Pols Voice Key",
        "Temple of Courage 2F Beamos Maze Chest",
        "Temple of Courage B1 Maze Chest",
        "Temple of Courage B1 Bow Chest",
        "Temple of Courage 2F Moving Platform Chest",
        "Temple of Courage 2F Spike Corridor Chest",
        "Temple of Courage B1 Torch Room Secret Chest",
        "Temple of Courage 1F Pols Voice Key 2",
        "Temple of Courage 2F Boss Key Chest",
        "Temple of Courage 3F Before Boss Chest",
        "Crayk Boss Reward",
        "Crayk Sand of Hours",
        "Crayk Heart Container",
    ],
    "Crayk": [
        "Crayk Boss Reward",
        "Crayk Sand of Hours",
        "Crayk Heart Container",
    ],
    "Spirit Island": [
        "Spirit Island Outside Chest",
        "Spirit Island Gauntlet Chest",
        "Spirit Island Power Upgrade Level 1",
        "Spirit Island Power Upgrade Level 2",
        "Spirit Island Wisdom Upgrade Level 1",
        "Spirit Island Wisdom Upgrade Level 2",
        "Spirit Island Courage Upgrade Level 1",
        "Spirit Island Courage Upgrade Level 2",
    ],
    "PoRL's Ship": [
        "Ocean NW Prince of Red Lion Combat Reward",
        "Ocean NW Prince of Red Lions Trade Quest Item",
    ],
    "Isle of Gust": [
        "Isle of Gust Hideout Chest",
        "Isle of Gust Miblin Cave North Chest",
        "Isle of Gust Miblin Cave South Chest",
        "Isle of Gust East Cliff Dig",
        "Isle of Gust West Cliff Chest",
        "Isle of Gust NW Dig",
        "Isle of Gust Sandworm Chest",
    ],
    "Temple of Wind": [
        "Temple of Wind B1 SE Corner Chest",
        "Temple of Wind B1 Ledge Chest",
        "Temple of Wind B2 Chest",
        "Temple of Wind B2 Bombable Wall Item",
        "Temple of Wind B1 Key Drop",
        "Temple of Wind B2 Bomb Bag Chest",
        "Temple of Wind 1F Boss Key Chest",
        "Cyclok Sand of Hours",
        "Cyclok Boss Reward",
        "Cyclok Heart Container",
    ],
    "Cyclok": [
        "Cyclok Sand of Hours",
        "Cyclok Boss Reward",
        "Cyclok Heart Container",
    ],
    "Bannan Island": [
        "Bannan Island Entrance Grapple Chest",
        "Bannan Island Wayfarers Dig",
        "Bannan Island Wayfarer Gift",
        "Bannan Island East Grapple Chest East",
        "Bannan Island East Grapple Chest West",
        "Bannan Island East Grapple Dig",
        "Bannan Island Cannon Game",
        "Bannan Island Wayfarer Trade Quest Chest",
        "Bannan Island Wayfarer Give Loovar",
        "Bannan Island Wayfarer Give Rusty Swordfish",
        "Bannan Island Wayfarer Give Legendary Neptoona",
        "Bannan Island Wayfarer Give Stowfish",
        "Bannan Island Give Letter to Joanne"
    ],
    "Uncharted Island": [
        "Uncharted Island Eye Dig",
        "Uncharted Island Grapple Chest",
        "Uncharted Island Cyclone Slate",
    ],
    "Zauz's Island": [
        "Zauz's Island Cuccoo Chest",
        "Zauz's Island Secret Dig",
        "Zauz's Island Triforce Crest",
        "Zauz's Island Phantom Blade",
    ],
    "Ghost Ship": [
        "Ghost Ship B1 Entrance Chest",
        "Ghost Ship B1 Second Sister Chest",
        "Ghost Ship B2 Third Sister Left Chest",
        "Ghost Ship B2 Third Sister Right Chest",
        "Ghost Ship B2 Spike Chest",
        "Ghost Ship B3 Chest",
        "Ghost Ship Rescue Tetra",
        "Cubus Sisters Ghost Key",
        "Cubus Sisters Heart Container",
    ],
    "Cubus Sisters": [
        "Cubus Sisters Ghost Key",
        "Cubus Sisters Heart Container",
    ],
    "Linebeck's Ship": [
        "Ocean Pirate Ambush Item",
    ],
    "Goron Island": [
        "Goron Island Yellow Chu Item",
        "Goron Island Grapple Chest",
        "Goron Island Goron Quiz",
        "Goron Island North Bombchu Switch Chest",
        "Goron Island North Dead End Chest",
        "Goron Island North Spike Chest",
        "Goron Island Chief Post Dungeon Item",
    ],
    "Goron Temple": [
        "Goron Temple 1F Switch Chest",
        "Goron Temple 1F Bow Chest",
        "Goron Temple B1 Bombchu Bag Chest",
        "Goron Temple B1 Kill Eyeslugs Chest",
        "Goron Temple B3 Kill Miblins Chest",
        "Goron Temple B2 Kill Eyeslugs Chest",
        "Goron Temple B2 Boss Key Chest",
        "Dongorongo Boss Reward",
        "Dongorongo Sand of Hours",
        "Dongorongo Heart Container",
    ],
    "Dongorongo": [
        "Dongorongo Boss Reward",
        "Dongorongo Sand of Hours",
        "Dongorongo Heart Container",
    ],
    "Harrow Island": [
        "Harrow Island Dig 1",
        "Harrow Island Dig 2",
        "Harrow Island Dig 3",
        "Harrow Island Dig 4",
    ],
    "Dee Ess Island": [
        "Dee Ess Menu Button Dig",
        "Dee Ess Left Speakers Dig SSW",
        "Dee Ess Right Speakers Dig SE",
        "Dee Ess Left Speakers Dig West",
        "Dee Ess Win Goron Game",
        "Dee Ess Eye Brute Chest",
        "Dee Ess Blow in Microphone Chest",
    ],
    "Isle of Frost": [
        "Isle of Frost Nobodo Grapple Chest",
        "Isle of Frost Chief House Dig",
        "Isle of Frost Estate Sign Dig",
        "Isle of Frost Fofo Dig (SE)",
        "Isle of Frost Dobo Dig (SW)",
        "Isle of Frost Estate SW Island Dig",
        "Isle of Frost Estate SE Island Dig",
        "Isle of Frost Ice Field South Ledge West Chest",
        "Isle of Frost Ice Field South Ledge East Chest",
        "Isle of Frost Ice Field SE Ledge Chest",
        "Isle of Frost Ice Field East Ledge Chest",
    ],
    "Temple of Ice": [
        "Temple of Ice 3F Corner Chest",
        "Temple of Ice 3F Switch State Chest",
        "Temple of Ice 3F Key Drop",
        "Temple of Ice 2F Grappling Hook Chest",
        "Temple of Ice B1 Entrance Chest",
        "Temple of Ice B1 SE Chest",
        "Temple of Ice B1 Locked Room Chest",
        "Temple of Ice B2 Bow Bounce Chest",
        "Temple of Ice B2 Fight Chest",
        "Temple of Ice B2 Boss Key Chest",
        "Gleeok Boss Reward",
        "Gleeok Sand of Hours",
        "Gleeok Heart Container",
    ],
    "Gleeok": [
        "Gleeok Boss Reward",
        "Gleeok Sand of Hours",
        "Gleeok Heart Container",
    ],
    "Isle of the Dead": [
        "Isle of the Dead Rupoor Cave 1",
        "Isle of the Dead Rupoor Cave 4",
        "Isle of the Dead Rupoor Cave 2",
        "Isle of the Dead Rupoor Cave 3",
        "Isle of the Dead Face Cave Chest",
        "Isle of the Dead Face Chest",
        "Isle of the Dead Regal Necklace Chest",
    ],
    "Isle of Ruins": [
        "Isle of Ruins Lower Water Cave Chest",
        "Isle of Ruins Maze Chest",
        "Isle of Ruins Dodge Boulders Chest",
        "Isle of Ruins Push Boulder Chest",
        "Isle of Ruins Doylan's Item",
        "Isle of Ruins Outside Doylan's Temple Chest",
        "Isle of Ruins Like-Like Dig",
        "Isle of Ruins Bonk Tree",
        "Isle of Ruins Outside Mutoh's Temple Chest",
    ],
    "Mutoh's Temple": [
        "Mutoh's Temple 2F Like-Like Maze Chest",
        "Mutoh's Temple 3F Hammer Chest",
        "Mutoh's Temple B2 Spike Roller Chest",
        "Mutoh's Temple B2 Ledge Chest",
        "Mutoh's Temple B1 Lower Water Chest",
        "Mutoh's Temple B1 Push Boulder Chest",
        "Mutoh's Temple B1 Boss Key Chest",
        "Eox Boss Reward",
        "Eox Sand of Hours",
        "Eox Heart Container",
    ],
    "Eox": [
        "Eox Boss Reward",
        "Eox Sand of Hours",
        "Eox Heart Container",],
    "Maze Island": [
        "Maze Island Maze Chest",
        "Maze Island Beginner",
        "Maze Island Normal",
        "Maze Island Expert",
        "Maze Island Bonus Reward",
        "Maze Island SE Dig",
        "Maze Island NE Dig",
        "Maze Island NW Dig",
    ],
    "Credits": [
        "GOAL: Triforce Door",
    ],
    "Man of Smiles' Ship": [
        "Ocean NE Man Of Smiles Item 1",
        "Ocean NE Man Of Smiles Item 2",
        "Ocean NE Man of Smiles Prize Postcard"
    ],
    "Wayaway's Ship": [
        "Ocean SE Hoiger Howgendoogen Trade Quest Item",
    ],
}

CATEGORY_LOCATION_GROUPS = {
    "Shops": [
        "Beedle Shop Bomb Bag",
        "Beedle Shop Wisdom Gem",
        "Masked Beedle Heart Container",
        "Masked Beedle Courage Gem",
        "Island Shop Power Gem",
        "Island Shop Quiver",
        "Island Shop Bombchu Bag",
        "Island Shop Heart Container",
        "Cannon Island Cannon",
        "Cannon Island Salvage Arm",
        "Mercay Ojibe (Docks Guy) Item",
    ],
    "Island Shops": [
        "Island Shop Power Gem",
        "Island Shop Quiver",
        "Island Shop Bombchu Bag",
        "Island Shop Heart Container",
    ],
    "Beedle": [
        "Beedle Shop Bomb Bag",
        "Beedle Shop Wisdom Gem",
        "Beedle Membership Bronze",
        "Beedle Membership Silver",
        "Beedle Membership Gold",
        "Beedle Membership Platinum",
        "Beedle Membership VIP",
    ],
    "Masked Beedle": [
        "Masked Beedle Heart Container",
        "Masked Beedle Courage Gem",
    ],
    "Minigames": [
        "Bannan Island Cannon Game",
        "Ocean NW Prince of Red Lion Combat Reward",
        "Molida Archery 1700",
        "Molida Archery 2000",
        "Dee Ess Win Goron Game",
        "Maze Island Beginner",
        "Maze Island Normal",
        "Maze Island Expert",
        "Maze Island Bonus Reward",
    ],
    "Rupee Dig Spots": [
        "Maze Island SE Dig",
        "Maze Island NE Dig",
        "Maze Island NW Dig",
        "Isle of Ruins Like-Like Dig",
        "Isle of Frost Chief House Dig",
        "Isle of Frost Estate SE Island Dig",
        "Isle of Frost Chief House Dig",
        "Isle of Frost Estate Sign Dig",
        "Isle of Frost Estate Fofo Dig (SE)",
        "Isle of Frost Estate Dobo Dig (SW)",
        "Dee Ess Left Speakers Dig SSW",
        "Dee Ess Right Speakers Dig SE",
        "Dee Ess Left Speakers Dig West ",
        "Isle of Gust NW Dig",
        "Isle of Gust East Cliff Dig",
        "Molida Island Cuccoo Grapple Small Island Dig",
        "Molida Cave Shovel Room Dig",
        "Molida Cave Geozard Dig",
        "Molida Island Romanos Tree Dig",
        "Cannon Island SE Dig",
        "Cannon Island Bee Dig",
        "Cannon Island East Dig",
    ],
    "Trade Quest": [
        "Ocean SW Nyave Trade Quest Item",
        "Ocean NW Prince of Red Lions Trade Quest Item",
        "Ocean SE Hoiger Howgendoogen Trade Quest Item",
        "Bannan Island Wayfarer Trade Quest Chest",
    ],
    "Bonk Trees": [
        "Mercay North Bonk Tree",
        "Isle of Ruins Bonk Tree",
        "Cannon Island Bonk Tree",
    ],
    "Wayaway's Ship": [
        "Ocean SE Hoiger Howgendoogen Trade Quest Item",
    ],
    "Golden Frogs": [
        "Ocean SW Golden Frog X",
        "Ocean SW Golden Frog Phi",
        "Ocean NW Golden Frog N",
        "Ocean SE Golden Frog Omega",
        "Ocean SE Golden Frog W",
        "Ocean NE Golden Frog Square"
    ],
    "Salvage": [
        "Ocean SW Salvage Courage Crest",
    ],
    "Spirit Upgrades": [
        "Spirit Island Power Upgrade Level 1",
        "Spirit Island Power Upgrade Level 2",
        "Spirit Island Wisdom Upgrade Level 1",
        "Spirit Island Wisdom Upgrade Level 2",
        "Spirit Island Courage Upgrade Level 1",
        "Spirit Island Courage Upgrade Level 2",
    ],
    "Fishing Locations": [
        "Bannan Island Wayfarer Give Loovar",
        "Bannan Island Wayfarer Give Rusty Swordfish",
        "Bannan Island Wayfarer Give Legendary Neptoona",
        "Bannan Island Wayfarer Give Stowfish",
        "Fishing Catch Skippyjack",
        "Fishing Catch Toona",
        "Fishing Catch Loovar",
        "Fishing Catch Rusty Swordfish",
        "Fishing Catch Legendary Neptoona",
        "Fishing Catch Stowfish",
    ],
    "Fish": [
        "Fishing Catch Skippyjack",
        "Fishing Catch Toona",
        "Fishing Catch Loovar",
        "Fishing Catch Rusty Swordfish",
        "Fishing Catch Legendary Neptoona",
        "Fishing Catch Stowfish",
    ],
    "Salvage Locations": [
        "Ocean SW Salvage #1 Molida SW",
        "Ocean SW Salvage #2 Mercay NE",
        "Ocean NW Salvage #3 Gusts SW",
        "Ocean NW Salvage #4 Bannan SE",
        "Ocean SW Salvage #5 Molida N",
        "Ocean NW Salvage #6 Bannan W",
        "Ocean NW Salvage #7 Gusts E",
        "Ocean SW Salvage #8 Mercay SE",
        "Ocean SW Salvage #9 Cannon W",
        "Ocean NW Salvage #10 Gusts SE",
        "Ocean NW Salvage #11 Gusts N",
        "Ocean SE Salvage #12 Dee Ess N",
        "Ocean SE Salvage #13 Harrow E",
        "Ocean SE Salvage #14 Goron NW",
        "Ocean SE Salvage #15 Goron W",
        "Ocean SE Salvage #16 Goron NE",
        "Ocean SE Salvage #17 Frost S",
        "Ocean SW Salvage #18 Cannon S",
        "Ocean NW Salvage #19 Gusts NE",
        "Ocean NW Salvage #20 Bannan E",
        "Ocean SW Salvage #21 Molida NW",
        "Ocean SE Salvage #22 Harrow S",
        "Ocean SE Salvage #23 Frost NW",
        "Ocean NE Salvage #24 Ruins W",
        "Ocean NE Salvage #25 Dead E",
        "Ocean NE Salvage #26 Ruins SW",
        "Ocean NE Salvage #27 Maze E",
        "Ocean NE Salvage #28 Ruins NW",
        "Ocean NE Salvage #29 Maze W",
        "Ocean NE Salvage #30 Ruins S",
        "Ocean NE Salvage #31 Dead S",
    ],
    "Boss Rewards": [
        "Blaaz Boss Reward",
        "Cyclok Boss Reward",
        "Crayk Boss Reward",
        "Dongorongo Boss Reward",
        "Gleeok Boss Reward",
        "Eox Boss Reward",
    ],
    "Grappling Hook Excludes": [
        "TotOK B3 NW Chest",
        "TotOK B3 SW Chest",
        "TotOK B3 SE Chest"
    ]
}

LOCATION_GROUPS = CATEGORY_LOCATION_GROUPS | STAGE_LOCATION_GROUPS

CUSTOM_METALS = {
    "Custom Metals": [
        "Verdanine",
        "Lavendine",
        "Amberine",
        "Vermilline",
        "Burgundine",
        "Crystaline",
        "Carrotine",
    ],
}

DUNGEON_NAMES = [
    "Mountain Passage",
    "Temple of the Ocean King",
    "Temple of Fire",
    "Temple of Wind",
    "Temple of Courage",
    "Goron Temple",
    "Temple of Ice",
    "Mutoh's Temple",
    "Ghost Ship"
]

DUNGEON_TO_BOSS_ITEM_LOCATION = {
    "Temple of the Ocean King": "TotOK B13 NE Sea Chart Chest",
    "Temple of Fire": "Blaaz Boss Reward",
    "Temple of Wind": "Cyclok Boss Reward",
    "Temple of Courage": "Crayk Boss Reward",
    "Goron Temple": "Dongorongo Boss Reward",
    "Temple of Ice": "Gleeok Boss Reward",
    "Mutoh's Temple": "Eox Boss Reward",
    "Ghost Ship": "_gs",
}

GHOST_SHIP_BOSS_ITEM_LOCATION = [
    "Ghost Ship Rescue Tetra",
    "Cubus Sisters Ghost Key",
    "Cubus Sisters Ghost Key"
]

DUNGEON_KEY_DATA = {
    39: {
        "name": "Mountain Passage",
        "address": 0x1BA64E,
        "filter": 0x0C,
        "value": 4,
        "size": 2,
    },
    37: {
        "name": "Temple of the Ocean King",
        "address": 0x1BA64E,
        "filter": 0xE0,
        "value": 0x20,
        "size": 3,
    },
    372: {
        "name": "Temple of the Ocean King",
        "address": 0x1BA64F,
        "filter": 0xC0,
        "value": 0x40,
        "size": 2,
    },
    0x1C: {
        "name": "Temple of Fire",
        "address": 0x1BA64E,
        "value": 1,
        "size": 2,
        "filter": 0x03,
    },
    0x1E: {
        "name": "Temple of Courage",
        "address": 0x1BA64F,
        "value": 0x10,
        "size": 2,
        "filter": 0x30,
    },
    0x1D: {
        "name": "Temple of Wind",
        "address": 0x1BA64E,
        "value": 0x10,
        "size": 1,
        "filter": 0x10
    },
    0x1F: {
        "name": "Temple of Ice",
        "address": 0x1BA64F,
        "value": 0x1,
        "size": 2,
        "filter": 0x03
    },
    0x21: {
        "name": "Mutoh's Temple",
        "address": 0x1BA64F,
        "value": 0x4,
        "size": 2,
        "filter": 0x0C
    },
}

BOSS_DOOR_DATA = {
    0x1C: {
        "name": "Temple of Fire",
        "address": 0x258D20,
        "value": 0x1
    },
    0x1D: {
        "name": "Temple of Wind",
        "address": 0x24D740,
        "value": 0x400
    },
    0x1E: {
        "name": "Temple of Courage",
        "address": 0x252360,
        "value": 0x2
    },
    0x20: {
        "name": "Goron Temple",
        "address": 0x25D9B0,
        "value": 0x1
    },
    0x1F: {
        "name": "Temple of Ice",
        "address": 0x259CA0,
        "value": 0x80
    },
    0x21: {
        "name": "Mutoh's Temple",
        "address": 0x24DED0,
        "value": 0x1
    },
}

# Entrance name: dungeon name
BOSS_STAIRCASES = {
    "ToF Enter Boss": "Temple of Fire",
    "ToW Enter Boss": "Temple of Wind",
    "ToC Enter Boss": "Temple of Courage",
    "Ghost Ship Cubus Sisters Reunion": "Ghost Ship",
    "GT Enter Boss": "Goron Temple",
    "ToI Enter Boss": "Temple of Ice",
    "MT Enter Boss": "Mutoh's Temple",
}

BOSS_LOOKUP = {
    "Temple of Fire": "Blaaz",
    "Temple of Wind": "Cyclok",
    "Temple of Courage": "Crayk",
    "Ghost Ship": "Cubus Sisters",
    "Goron Temple": "Dongorongo",
    "Temple of Ice": "Gleeok",
    "Mutoh's Temple": "Eox"
}

# Boss Room Entrance name: boss reward location name
BOSS_ENTRANCE_LOOKUP = {
    "Blaaz Exit": "Blaaz Boss Reward",
    "Cyclok Exit": "Cyclok Boss Reward",
    "Crayk Exit": "Crayk Boss Reward",
    "Cubus Sisters Blue Warp": "Cubus Sisters Ghost Key",
    "Dongo Exit": "Dongorongo Boss Reward",
    "Gleeok Exit": "Gleeok Boss Reward",
    "Eox Exit": "Eox Boss Reward",
}

COLOR_SWITCH_DATA = {
    0x1F: {
        "name": "Temple of Ice",
        "address": 0x20DBE0,
        "value": 0x1
    },
    0x1E: {
        "name": "Temple of Courage",
        "address": 0x207CA8,
        "value": 0x1
    },
}

# Decode classification for humans
CLASSIFICATION = {
    1: "progression",
    2: "useful",
    4: "trap",
    9: "progression_skip_balancing",
    17: "progression_deprioritized",
    25: "progression_deprioritized_skip_balancing",
    0: "filler"
                  }

BOSS_WARP_LOOKUP = {
    28: "ToF Exit",
    29: "ToW Exit",
    30: "ToC Exit",
    31: "ToI Exit",
    32: "GT Exit",
    33: "MT Exit",
    0x29: "Ghost Ship B1 Ascend"
}

BOSS_WARP_SCENE_LOOKUP = {
    0x2B00: "Blaaz Exit",
    0x2A00: "Cyclok Exit",
    0x2C00: "Crayk Exit",
    0x200A: "Dongo Exit",
    0x1F06: "Gleeok Exit",
    0x2106: "Eox Exit",
    0x3000: "Cubus Sisters Blue Warp"
}

EQUIPPED_SHIP_PARTS_ADDR = [
    0x1BA544,
    0x1BA548,
    0x1BA54C,
    0x1BA550,
    0x1BA554,
    0x1BA558,
    0x1BA55C,
    0x1BA560,
]

TREASURE_READ_LIST = {i: (0x1BA5AC + i * 4, 4, "Main RAM") for i in range(8)}

if __name__ == "__main__":
    for group in LOCATION_GROUPS:
        print("-", group)