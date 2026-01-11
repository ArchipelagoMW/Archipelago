surfaces = [
    "Overworld",
    "Underworld",
    "Moon"
]

areas = [
    "BaronTown",
    "Mist",
    "Kaipo",
    "Silvera",
    "ToroiaTown",
    "Agart",
    "BaronWeaponShop",
    "ChocoboForest",
    "BaronCastle",
    "Sewer",
    "Damcyan",
    "Fabul",
    "ToroiaCastle",
    "ToroiaTreasury",
    "Eblan",
    "MistCave",
    "WateryPass",
    "Waterfall",
    "AntlionCave",
    "MountHobs",
    "MountOrdeals",
    "CaveMagnes",
    "Zot",
    "UpperBabil",
    "Giant",
    "CaveEblan",
    "Smithy",
    "Tomra",
    "DwarfCastle",
    "LowerBabil",
    "UpperBabilAfterFall",
    "CaveOfSummons",
    "Feymarch",
    "SylvanCave",
    "SealedCave",
    "BahamutCave",
    "LunarPath",
    "LunarCore",
    "Adamant",
    "Mysidia",
    "LunarPalace"
]

hook_areas = [
    "UpperBabil",
    "UpperBabilAfterFall",
    "CaveEblan",
    "Adamant"
]

underworld_areas = [
    "Smithy",
    "Tomra",
    "DwarfCastle",
    "LowerBabil",
    "CaveOfSummons",
    "Feymarch",
    "SylvanCave",
    "SealedCave"
]

moon_areas = [
    "Giant",
    "BahamutCave",
    "LunarPath",
    "LunarCore",
    "LunarPalace"
]

overworld_areas = [area for area in areas if area not in [*hook_areas, *underworld_areas, *moon_areas]]
