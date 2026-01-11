from . import items

area_rules = {
    "BaronWeaponShop": ["Baron Key"],
    "BaronCastle": ["Baron Key", "Baigan Slot Defeated"],
    "Sewer": ["Baron Key"],
    "ToroiaTreasury": ["Earth Crystal"],
    "Adamant": ["Hook"],
    "UpperBabilAfterFall": ["King and Queen Slot Defeated", "Rubicant Slot Defeated"],
    "SealedCave": ["Luca Key"]
}

boss_rules = {
    "Officer Slot": ["Package"],
    "Milon Z. Slot": ["Milon Slot Defeated"],
    "Mirror Cecil Slot": ["Milon Slot Defeated", "Milon Z. Slot Defeated"],
    "Karate Slot": ["Guards Slot Defeated"],
    "Baigan Slot": ["Baron Key"],
    "Kainazzo Slot": ["Baron Key", "Baigan Slot Defeated"],
    "Dark Elf Slot": ["TwinHarp"],
    "Valvalis Slot": ["Earth Crystal", "Magus Sisters Slot Defeated"],
    "Golbez Slot": ["Calbrena Slot Defeated"],
    "Dark Imp Slot": ["Tower Key"],
    "Rubicant Slot": ["King and Queen Slot Defeated"],
    "Odin Slot": ["Baron Key", "Baigan Slot Defeated"],
    "CPU Slot": ["Elements Slot Defeated"],
    "Zeromus": ["Crystal"]
}

individual_location_rules = {
    # This is a really janky way of ensuring we can find D. Mist without having to randomize the bosses through AP
    "Mist -- Exterior -- Rydia's Mom item": [
        "Hook", "Earth Crystal", "Package",
        "TwinHarp", "Tower Key", "Darkness Crystal",
        "Luca Key", "Baron Key"
    ],
    "Mist Character": ["Package"],
    "Kaipo Character": ["SandRuby"],
    "Mt. Hobs Character": ["MomBomb Slot Defeated"],
    "Baron Inn Character": ["Karate Slot Defeated"],
    "Baron Castle Character": ["Kainazzo Slot Defeated"],
    "Tower of Zot Character 1": ["Valvalis Slot Defeated"],
    "Tower of Zot Character 2": ["Valvalis Slot Defeated"],
    "Dwarf Castle Character": ["Golbez Slot Defeated"],
    "Cave Eblana Character": ["Hook"],
    "Lunar Palace Character": ["Darkness Crystal"],
    "Giant of Bab-il Character": ["CPU Slot Defeated"],
    "Antlion Cave -- B3F -- Antlion Nest item": ["Antlion Slot Defeated"],
    "Baron Town -- Inn -- item": ["Karate Slot Defeated"],
    "Baron Castle -- Throne Room -- item": ["Kainazzo Slot Defeated"],
    "Tower of Zot -- 6F -- item": ["Valvalis Slot Defeated"],
    "Dwarf Castle -- Throne Room -- Luca item": ["Golbez Slot Defeated"],
    "Sealed Cave -- Crystal Room --  item": ["Evilwall Slot Defeated"],
    "Fabul -- West tower 3F (Yang's room) -- Found Yang item": ["Hook", "Magma Key"],
    "Fabul -- West tower 3F (Yang's room) -- Pan Trade item": ["Hook", "Magma Key", "Pan"],
    "Sylvan Cave -- B3F -- Sylph item": ["Hook", "Magma Key", "Pan"],
    "Mt. Ordeals -- Mirror Room -- item": ["Mirror Cecil Slot Defeated"],
    "Cave Magnes -- Crystal Room -- item": ["Dark Elf Slot Defeated"],
    "Tower of Bab-il (lower) -- 5F -- item (Super Cannon destruction)": ["Dark Imp Slot Defeated"],
    "Baron Castle -- Basement -- Odin item": ["Odin Slot Defeated"],
    "Cave Bahamut -- B3F -- Baham item": ["Bahamut Slot Defeated"],
    "Town of Monsters -- Throne Room -- Asura item": ["Asura Slot Defeated"],
    "Town of Monsters -- Throne Room -- Levia item": ["Leviatan Slot Defeated"],
    "Adamant -- Cave -- Rat Tail Trade item": ["Rat Tail"],
    "Adamant -- Cave -- Pink Tail Trade item": ["Pink Tail"],
    "Kokkol's House 2F -- Kokkol -- forge item": ["Legend Sword", "Adamant"],
    "Lunar Subterrane -- B7 (right room) -- Ribbon Left": ["D. Lunars Slot Defeated"],
    "Lunar Subterrane -- B7 (right room) -- Ribbon Right": ["D. Lunars Slot Defeated"],
    "Objectives Status": [*[item for item in items.key_item_names if item not in ["Crystal", "Spoon", "Pass"]]],
    "Objective Reward": ["All Objectives Cleared"]
}

location_tiers = {
    # -- Tier 0 --
    # -- Available from start of game with no gating or difficulty --
    0: [
        "BaronTown", "Mist", "Kaipo", "Silvera", "ToroiaTown", "Agart",
        "ChocoboForest", "Damcyan", "Fabul", "ToroiaCastle", "Mysidia"
    ],
    # -- Tier 1 --
    # -- Available from start of game with minimal gating or difficulty --
    1: [
        "MistCave", "WateryPass", "AntlionCave", "MountOrdeals"
    ],
    # -- Tier 2 --
    # -- Available after defeating a boss or receiving a single key item --
    2: [
        "BaronWeaponShop", "Sewer", "ToroiaTreasury", "Waterfall", "MountHobs",
        "DwarfCastle", "Smithy", "Tomra"
    ],
    # -- Tier 3 --
    # -- Available after defeating a boss or receiving a key item with some difficulty
    3: [
        "CaveMagnes", "Zot", "CaveEblan", "LowerBabil", "CaveOfSummons",
        "UpperBabil", "UpperBabilAfterFall", "SealedCave"
    ],
    # -- Tier 4 --
    # -- Requires multiple key items and/or bosses to access
    4: [
        "BaronCastle", "Eblan", "Feymarch", "SylvanCave", "Adamant"
    ],
    # -- Tier 5 --
    # -- THE MOON --
    5: [
        "Giant", "BahamutCave", "LunarPath", "LunarCore", "LunarPalace"
    ]
}

logical_gating = {
    0: {"characters": 0, "key_items": 0},
    1: {"characters": 2, "key_items": 2},
    2: {"characters": 4, "key_items": 4},
    3: {"characters": 6, "key_items": 6},
    4: {"characters": 8, "key_items": 8},
    5: {"characters": 10, "key_items": 10},
}
