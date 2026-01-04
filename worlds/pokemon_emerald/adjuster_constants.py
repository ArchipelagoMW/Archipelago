from worlds._pokemon_gen3_adjuster.adjuster_constants import *
from .data import data

EMERALD_PATCH_EXTENSIONS = ".apemerald"

EMERALD_POKEMON_SPRITES = ["front_anim", "back", "icon", "footprint"]
EMERALD_POKEMON_MAIN_PALETTE_EXTRACTION_PRIORITY = ["front_anim", "back"]
EMERALD_POKEMON_SHINY_PALETTE_EXTRACTION_PRIORITY = ["sfront_anim", "sback"]
EMERALD_POKEMON_PALETTES = {
    "palette": EMERALD_POKEMON_MAIN_PALETTE_EXTRACTION_PRIORITY,
    "palette_shiny": EMERALD_POKEMON_SHINY_PALETTE_EXTRACTION_PRIORITY
}

EMERALD_EGG_SPRITES = [*EMERALD_POKEMON_SPRITES, "hatch_anim"]
EMERALD_EGG_PALETTES = {**EMERALD_POKEMON_PALETTES, "palette_hatch": POKEMON_HATCH_PALETTE_EXTRACTION_PRIORITY}

EMERALD_TRAINER_FOLDERS = ["Brendan", "May"]
EMERALD_TRAINER_SPRITES = ["walking_running", "acro_bike", "mach_bike", "surfing", "field_move", "underwater",
                           "fishing", "watering", "decorating", "battle_front", "battle_back"]
EMERALD_TRAINER_MAIN_PALETTE_EXTRACTION_PRIORITY = ["walking_running", "acro_bike", "mach_bike", "surfing",
                                                    "field_move", "fishing", "watering", "decorating"]
EMERALD_TRAINER_PALETTES = {
    "palette": EMERALD_TRAINER_MAIN_PALETTE_EXTRACTION_PRIORITY,
    "palette_reflection": TRAINER_REFLECTION_PALETTE_EXTRACTION_PRIORITY,
    "palette_underwater": TRAINER_UNDERWATER_PALETTE_EXTRACTION_PRIORITY,
    "palette_battle_back": TRAINER_BATTLE_BACK_PALETTE_EXTRACTION_PRIORITY,
    "palette_battle_front": TRAINER_BATTLE_FRONT_PALETTE_EXTRACTION_PRIORITY
}

EMERALD_SIMPLE_TRAINER_FOLDERS: list[str] = []

EMERALD_FOLDER_OBJECT_INFOS: list[dict[str, str | list[str] | dict[str, list[str]]]] = [
    {
        "name": "Egg",
        "key": "pokemon",
        "folders": POKEMON_FOLDERS,
        "sprites": EMERALD_EGG_SPRITES,
        "palettes": EMERALD_EGG_PALETTES
    },
    {
        "key": "pokemon",
        "folders": POKEMON_FOLDERS,
        "sprites": EMERALD_POKEMON_SPRITES,
        "palettes": EMERALD_POKEMON_PALETTES
    },
    {
        "key": "players",
        "folders": EMERALD_TRAINER_FOLDERS,
        "sprites": EMERALD_TRAINER_SPRITES,
        "palettes": EMERALD_TRAINER_PALETTES
    },
    {
        "key": "trainer",
        "folders": EMERALD_SIMPLE_TRAINER_FOLDERS,
        "sprites": SIMPLE_TRAINER_SPRITES,
        "palettes": SIMPLE_TRAINER_PALETTES
    }
]

EMERALD_INTERNAL_ID_TO_OBJECT_ADDRESS = {
    "pokemon_front_anim":    ("gMonFrontPicTable",      8,  False),
    "pokemon_back":          ("gMonBackPicTable",       8,  False),
    "pokemon_icon":          ("gMonIconTable",          4,  False),
    "pokemon_icon_index":    ("gMonIconPaletteIndices", 1,  False),
    "pokemon_footprint":     ("gMonFootprintTable",     4,  False),
    "pokemon_hatch_anim":    ("sEggHatchTiles",         0,  True),
    "pokemon_palette":       ("gMonPaletteTable",       8,  False),
    "pokemon_palette_shiny": ("gMonShinyPaletteTable",  8,  False),
    "pokemon_palette_hatch": ("sEggPalette",            0,  True),
    "pokemon_stats":         ("gSpeciesInfo",           28, False),
    "pokemon_move_pool":     ("gLevelUpLearnsets",      4,  False),

    "brendan_walking_running":      ("gObjectEventGraphicsInfoPointers", 400, False),
    "brendan_mach_bike":            ("gObjectEventGraphicsInfoPointers", 404, False),
    "brendan_acro_bike":            ("gObjectEventGraphicsInfoPointers", 408, False),
    "brendan_surfing":              ("gObjectEventGraphicsInfoPointers", 412, False),
    "brendan_field_move":           ("gObjectEventGraphicsInfoPointers", 416, False),
    "brendan_underwater":           ("gObjectEventGraphicsInfoPointers", 444, False),
    "brendan_fishing":              ("gObjectEventGraphicsInfoPointers", 548, False),
    "brendan_watering":             ("gObjectEventGraphicsInfoPointers", 764, False),
    "brendan_decorating":           ("gObjectEventGraphicsInfoPointers", 772, False),
    "brendan_battle_front":         ("gTrainerFrontPicTable",            568, False),
    "brendan_battle_back":          ("gTrainerBackPicTable",             0,   False),
    "brendan_battle_back_throw":    ("sTrainerBackSpriteTemplates",      0,   False),
    "brendan_palette":              ("sObjectEventSpritePalettes",       64,  False),
    "brendan_palette_reflection":   ("sObjectEventSpritePalettes",       72,  False),
    "brendan_palette_underwater":   ("sObjectEventSpritePalettes",       88,  False),
    "brendan_palette_battle_back":  ("gTrainerBackPicPaletteTable",      0,   False),
    "brendan_palette_battle_front": ("gTrainerFrontPicPaletteTable",     568, False),

    "may_walking_running":      ("gObjectEventGraphicsInfoPointers", 420, False),
    "may_mach_bike":            ("gObjectEventGraphicsInfoPointers", 424, False),
    "may_acro_bike":            ("gObjectEventGraphicsInfoPointers", 428, False),
    "may_surfing":              ("gObjectEventGraphicsInfoPointers", 432, False),
    "may_field_move":           ("gObjectEventGraphicsInfoPointers", 436, False),
    "may_underwater":           ("gObjectEventGraphicsInfoPointers", 448, False),
    "may_fishing":              ("gObjectEventGraphicsInfoPointers", 552, False),
    "may_watering":             ("gObjectEventGraphicsInfoPointers", 768, False),
    "may_decorating":           ("gObjectEventGraphicsInfoPointers", 776, False),
    "may_battle_front":         ("gTrainerFrontPicTable",            576, False),
    "may_battle_back":          ("gTrainerBackPicTable",             8,   False),
    "may_battle_back_throw":    ("sTrainerBackSpriteTemplates",      24,  False),
    "may_palette":              ("sObjectEventSpritePalettes",       136, False),
    "may_palette_reflection":   ("sObjectEventSpritePalettes",       144, False),
    "may_palette_underwater":   ("sObjectEventSpritePalettes",       88,  False),
    "may_palette_battle_back":  ("gTrainerBackPicPaletteTable",      8,   False),
    "may_palette_battle_front": ("gTrainerFrontPicPaletteTable",     576, False),

    "brendan_battle_throw_anim": ("gTrainerBackAnimsPtrTable", 0, False),
    "may_battle_throw_anim":     ("gTrainerBackAnimsPtrTable", 4, False),
    "emerald_battle_throw_anim": ("gTrainerBackAnimsPtrTable", 0, True),
    "frlg_battle_throw_anim":    ("gTrainerBackAnimsPtrTable", 8, True),
}

EMERALD_OVERWORLD_SPRITE_ADDRESSES = {
    "brendan_walking_running": [0,   400, 864],
    "brendan_mach_bike":       [4,   404],
    "brendan_acro_bike":       [252, 408],
    "brendan_surfing":         [8,   412],
    "brendan_field_move":      [12,  416],
    "brendan_underwater":      [444],
    "brendan_fishing":         [548],
    "brendan_watering":        [764],
    "brendan_decorating":      [772],
    "may_walking_running":     [356, 420, 868],
    "may_mach_bike":           [360, 424],
    "may_acro_bike":           [364, 428],
    "may_surfing":             [368, 432],
    "may_field_move":          [372, 436],
    "may_underwater":          [448],
    "may_fishing":             [552],
    "may_watering":            [768],
    "may_decorating":          [776],
}

EMERALD_POINTER_REFERENCES = {
    "overworld_palette_table": [("LoadObjectEventPalette", 40), ("PatchObjectPalette", 52),
                                ("FindObjectEventPaletteIndexByTag", 40)]
}

EMERALD_OVERWORLD_PALETTE_IDS = {
    "Brendan": 0x1100,
    "May": 0x1110,
    "Underwater": 0x1115
}

EMERALD_DATA_ADDRESSES_ORIGINAL = {
    "LoadObjectEventPalette": 0x08e894,
    "PatchObjectPalette": 0x08e91c,
    "FindObjectEventPaletteIndexByTag": 0x08e980,
    "gSpeciesInfo": 0x3203cc,
    "gLevelUpLearnsets": 0x32937c,
    "gMonFrontPicTable": 0x30a18c,
    "gMonBackPicTable": 0x3028b8,
    "gMonIconTable": 0x57bca8,
    "gMonFootprintTable": 0x56e694,
    "gMonPaletteTable": 0x303678,
    "gMonShinyPaletteTable": 0x304438,
    "gMonIconPaletteIndices": 0x57c388,
    "sEggPalette": 0x32b70c,
    "sEggHatchTiles": 0x32b72c,
    "gObjectEventGraphicsInfoPointers": 0x505620,
    "sObjectEventSpritePalettes": 0x50bbc8,
    "gTrainerFrontPicTable": 0x305654,
    "gTrainerFrontPicPaletteTable": 0x30593c,
    "gTrainerBackPicTable": 0x305d4c,
    "gTrainerBackPicPaletteTable": 0x305d8c,
    "sTrainerBackSpriteTemplates": 0x329df8,
    "gTrainerBackAnimsPtrTable": 0x305d0c,
    "sBackAnims_Brendan": 0x305ccc,
    "sBackAnims_Red": 0x305cdc,
    "gObjectEventBaseOam_16x16": 0x5094fc,
    "gObjectEventBaseOam_16x32": 0x509514,
    "gObjectEventBaseOam_32x32": 0x50951c,
    "sOamTables_16x16": 0x50954c,
    "sOamTables_16x32": 0x5095a0,
    "sOamTables_32x32": 0x5095f4,
    "sEmpty6": 0xe3cf31
}

EMERALD_DATA_ADDRESS_BEGINNING = 0x00
EMERALD_DATA_ADDRESS_END = 0xFFFFFF

EMERALD_DATA_ADDRESS_INFOS: dict[str, int | dict[str, int]] = {
    "Emerald": {
        "crc32": 0x1f1c08fb,
        "original_addresses": EMERALD_DATA_ADDRESSES_ORIGINAL,
        "ap_addresses": data.rom_addresses,
        "data_address_beginning": EMERALD_DATA_ADDRESS_BEGINNING,
        "data_address_end": EMERALD_DATA_ADDRESS_END
    }
}

EMERALD_VALID_OVERWORLD_SPRITE_SIZES: list[dict[str, int | str]] = [
    {"width": 16, "height": 16, "data": "sOamTables_16x16", "distrib": "gObjectEventBaseOam_16x16"},
    {"width": 16, "height": 32, "data": "sOamTables_16x32", "distrib": "gObjectEventBaseOam_16x32"},
    {"width": 32, "height": 32, "data": "sOamTables_32x32", "distrib": "gObjectEventBaseOam_32x32"},
]

EMERALD_SPRITES_REQUIREMENTS: dict[str, dict[str, bool | int | list[int]]] = {
    "pokemon_front_anim":        {"frames": 2,      "width": 64, "height": 64},
    "pokemon_back":              {"frames": 1,      "width": 64, "height": 64},
    "pokemon_icon":              {"frames": 2,      "width": 32, "height": 32, "palette": VALID_ICON_PALETTES},
    "pokemon_footprint":         {"frames": 1,      "width": 16, "height": 16, "palette_size": 2,
                                  "palette": VALID_FOOTPRINT_PALETTE},
    "pokemon_hatch_anim":        {"frames": 1,      "width": 32, "height": 136},
    "players_walking_running":   {"frames": 18,     "width": 16, "height": 32, "palette": VALID_OVERWORLD_PALETTE},
    "players_reflection":        {"frames": 18,     "width": 16, "height": 32, "palette": []},
    "players_mach_bike":         {"frames": 9,      "width": 32, "height": 32, "palette": VALID_OVERWORLD_PALETTE},
    "players_acro_bike":         {"frames": 27,     "width": 32, "height": 32, "palette": VALID_OVERWORLD_PALETTE},
    "players_surfing":           {"frames": 12,     "width": 32, "height": 32, "palette": VALID_OVERWORLD_PALETTE},
    "players_field_move":        {"frames": 5,      "width": 32, "height": 32, "palette": VALID_OVERWORLD_PALETTE},
    "players_underwater":        {"frames": 9,      "width": 32, "height": 32,
                                  "palette": VALID_OVERWORLD_UNDERWATER_PALETTE},
    "players_fishing":           {"frames": 12,     "width": 32, "height": 32, "palette": VALID_OVERWORLD_PALETTE},
    "players_watering":          {"frames": 9,      "width": 32, "height": 32, "palette": VALID_OVERWORLD_PALETTE},
    "players_decorating":        {"frames": 1,      "width": 16, "height": 32, "palette": VALID_OVERWORLD_PALETTE},
    "players_battle_front":      {"frames": 1,      "width": 64, "height": 64},
    "players_battle_back":       {"frames": [4, 5], "width": 64, "height": 64},
    "players_battle_back_throw": {"frames": [4, 5], "width": 64, "height": 64},
    "trainer_walking":           {"frames": 9,      "width": 16, "height": 32, "palette": VALID_WEAK_OVERWORLD_PALETTE},
    "trainer_battle_front":      {"frames": 1,      "width": 64, "height": 64},
}

EMERALD_SPRITES_REQUIREMENTS_EXCEPTIONS: dict[str, dict[str, dict[str, bool | int | list[int]]]] = {
    "Castform": {
        "pokemon_front_anim": {"frames": 4, "palette_size": 16, "palettes": 4, "palette_per_frame": True},
        "pokemon_back":       {"frames": 4, "palette_size": 16, "palettes": 4, "palette_per_frame": True},
    },
    "Deoxys": {
        "pokemon_back":       {"frames": 2},
        "pokemon_icon":       {"frames": 4},
    },
    "Unown A": {
        "pokemon_front_anim":  {"palette": VALID_UNOWN_PALETTE},
        "pokemon_back":        {"palette": VALID_UNOWN_PALETTE},
        "pokemon_sfront_anim": {"palette": VALID_UNOWN_SHINY_PALETTE},
        "pokemon_sback":       {"palette": VALID_UNOWN_SHINY_PALETTE},
    }
}