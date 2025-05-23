from worlds.pokemon_emerald.adjuster_constants import \
    TRAINER_REFLECTION_PALETTE_EXTRACTION_PRIORITY, TRAINER_BATTLE_BACK_PALETTE_EXTRACTION_PRIORITY, \
    TRAINER_BATTLE_FRONT_PALETTE_EXTRACTION_PRIORITY, VALID_UNOWN_PALETTE, VALID_UNOWN_SHINY_PALETTE, \
    VALID_ICON_PALETTES, VALID_FOOTPRINT_PALETTE, SIMPLE_TRAINER_SPRITES, SIMPLE_TRAINER_PALETTES, \
    EMERALD_DATA_ADDRESS_INFOS, POKEMON_HATCH_PALETTE_EXTRACTION_PRIORITY, POKEMON_FOLDERS, \
    VALID_OVERWORLD_PALETTE, VALID_WEAK_OVERWORLD_PALETTE
from .data import data

FR_LG_POKEMON_SPRITES = ['front', 'back', 'icon', 'footprint']
FR_LG_POKEMON_MAIN_PALETTE_EXTRACTION_PRIORITY = ['front', 'back']
FR_LG_POKEMON_SHINY_PALETTE_EXTRACTION_PRIORITY = ['sfront', 'sback']
FR_LG_POKEMON_PALETTES = {
    'palette': FR_LG_POKEMON_MAIN_PALETTE_EXTRACTION_PRIORITY,
    'palette_shiny': FR_LG_POKEMON_SHINY_PALETTE_EXTRACTION_PRIORITY
}

FR_LG_EGG_SPRITES = [*FR_LG_POKEMON_SPRITES, 'hatch_anim']
FR_LG_EGG_PALETTES = {**FR_LG_POKEMON_PALETTES, 'palette_hatch': POKEMON_HATCH_PALETTE_EXTRACTION_PRIORITY}

FR_LG_TRAINER_FOLDERS = ['Red', 'Leaf']
FR_LG_TRAINER_SPRITES = ['walking_running', 'bike', 'surfing', 'field_move', 'fishing', 'bike_vs_seeker', 'battle_front', 'battle_back']
FR_LG_TRAINER_MAIN_PALETTE_EXTRACTION_PRIORITY = ['walking_running', 'bike', 'surfing', 'field_move', 'fishing', 'bike_vs_seeker']
FR_LG_TRAINER_PALETTES = {
    'palette': FR_LG_TRAINER_MAIN_PALETTE_EXTRACTION_PRIORITY,
    'palette_reflection': TRAINER_REFLECTION_PALETTE_EXTRACTION_PRIORITY,
    'palette_battle_back': TRAINER_BATTLE_BACK_PALETTE_EXTRACTION_PRIORITY,
    'palette_battle_front': TRAINER_BATTLE_FRONT_PALETTE_EXTRACTION_PRIORITY
}

BLUE_TRAINER_SPRITES = ['walking', 'battle_front_1', 'battle_front_2', 'battle_front_3']
BLUE_TRAINER_MAIN_PALETTE_EXTRACTION_PRIORITY = ['walking']
BLUE_TRAINER_BATTLE_FRONT_1_PALETTE_EXTRACTION_PRIORITY = ['battle_front_1']
BLUE_TRAINER_BATTLE_FRONT_2_PALETTE_EXTRACTION_PRIORITY = ['battle_front_2']
BLUE_TRAINER_BATTLE_FRONT_3_PALETTE_EXTRACTION_PRIORITY = ['battle_front_3']
BLUE_TRAINER_PALETTES = {
    'palette': BLUE_TRAINER_MAIN_PALETTE_EXTRACTION_PRIORITY,
    'palette_battle_front_1': BLUE_TRAINER_BATTLE_FRONT_1_PALETTE_EXTRACTION_PRIORITY,
    'palette_battle_front_2': BLUE_TRAINER_BATTLE_FRONT_2_PALETTE_EXTRACTION_PRIORITY,
    'palette_battle_front_3': BLUE_TRAINER_BATTLE_FRONT_3_PALETTE_EXTRACTION_PRIORITY,
}

FR_LG_SIMPLE_TRAINER_FOLDERS = ['Blue']

FR_LG_FOLDER_OBJECT_INFOS = [
    {
        'name': 'Blue',
        'key': 'strainr',
        'folders': FR_LG_SIMPLE_TRAINER_FOLDERS,
        'sprites': BLUE_TRAINER_SPRITES,
        'palettes': BLUE_TRAINER_PALETTES
    },
    {
        'name': 'Egg',
        'key': 'pokemon',
        'folders': POKEMON_FOLDERS,
        'sprites': FR_LG_EGG_SPRITES,
        'palettes': FR_LG_EGG_PALETTES
    },
    {
        'key': 'pokemon',
        'folders': POKEMON_FOLDERS,
        'sprites': FR_LG_POKEMON_SPRITES,
        'palettes': FR_LG_POKEMON_PALETTES
    },
    {
        'key': 'trainer',
        'folders': FR_LG_TRAINER_FOLDERS,
        'sprites': FR_LG_TRAINER_SPRITES,
        'palettes': FR_LG_TRAINER_PALETTES
    },
    {
        'key': 'strainr',
        'folders': FR_LG_SIMPLE_TRAINER_FOLDERS,
        'sprites': SIMPLE_TRAINER_SPRITES,
        'palettes': SIMPLE_TRAINER_PALETTES
    }
]

FR_LG_INTERNAL_ID_TO_OBJECT_ADDRESS = {
    'pokemon_front':         lambda c, a : c['gMonFrontPicTable']      + 8 * a,
    'pokemon_back':          lambda c, a : c['gMonBackPicTable']       + 8 * a,
    'pokemon_icon':          lambda c, a : c['gMonIconTable']          + 4 * a,
    'pokemon_icon_index':    lambda c, a : c['gMonIconPaletteIndices'] + a,
    'pokemon_footprint':     lambda c, a : c['gMonFootprintTable']     + 4 * a,
    'pokemon_hatch_anim':    lambda c, _ : (c['sEggHatchTiles'], True),
    'pokemon_palette':       lambda c, a : c['gMonPaletteTable']       + 8 * a,
    'pokemon_palette_shiny': lambda c, a : c['gMonShinyPaletteTable']  + 8 * a,
    'pokemon_palette_hatch': lambda c, _ : (c['sEggPalette'], True),
    'pokemon_stats':         lambda c, a : c['gSpeciesInfo']           + 28 * a,
    'pokemon_move_pool':     lambda c, a : c['gLevelUpLearnsets']      + 4 * a,

    'red_walking_running':      lambda c : c['gObjectEventGraphicsInfoPointers'] + 0,
    'red_bike':                 lambda c : c['gObjectEventGraphicsInfoPointers'] + 4,
    'red_surfing':              lambda c : c['gObjectEventGraphicsInfoPointers'] + 8,
    'red_field_move':           lambda c : c['gObjectEventGraphicsInfoPointers'] + 12,
    'red_fishing':              lambda c : c['gObjectEventGraphicsInfoPointers'] + 16,
    'red_bike_vs_seeker':       lambda c : c['gObjectEventGraphicsInfoPointers'] + 24,
    'red_battle_front':         lambda c : c['gTrainerFrontPicTable'] + 1080,
    'red_battle_back':          lambda c : c['gTrainerBackPicTable'] + 0,
    'red_battle_back_throw':    lambda c : c['sTrainerBackSpriteTemplates'] + 0,
    'red_palette':              lambda c : c['sObjectEventSpritePalettes'] + 64,
    'red_palette_battle_back':  lambda c : c['gTrainerBackPicPaletteTable'] + 0,
    'red_palette_battle_front': lambda c : c['gTrainerFrontPicPaletteTable'] + 1080,

    'leaf_walking_running':      lambda c : c['gObjectEventGraphicsInfoPointers'] + 28,
    'leaf_bike':                 lambda c : c['gObjectEventGraphicsInfoPointers'] + 32,
    'leaf_surfing':              lambda c : c['gObjectEventGraphicsInfoPointers'] + 36,
    'leaf_field_move':           lambda c : c['gObjectEventGraphicsInfoPointers'] + 40,
    'leaf_fishing':              lambda c : c['gObjectEventGraphicsInfoPointers'] + 44,
    'leaf_bike_vs_seeker':       lambda c : c['gObjectEventGraphicsInfoPointers'] + 52,
    'leaf_battle_front':         lambda c : c['gTrainerFrontPicTable'] + 1088,
    'leaf_battle_back':          lambda c : c['gTrainerBackPicTable'] + 8,
    'leaf_battle_back_throw':    lambda c : c['sTrainerBackSpriteTemplates'] + 24,
    'leaf_palette':              lambda c : c['sObjectEventSpritePalettes'] + 104,
    'leaf_palette_battle_back':  lambda c : c['gTrainerBackPicPaletteTable'] + 8,
    'leaf_palette_battle_front': lambda c : c['gTrainerFrontPicPaletteTable'] + 1088,

    'blue_walking':                lambda c : c['gObjectEventGraphicsInfoPointers'] + 288,
    'blue_battle_front_1':         lambda c : c['gTrainerFrontPicTable'] + 848,
    'blue_battle_front_2':         lambda c : c['gTrainerFrontPicTable'] + 992,
    'blue_battle_front_3':         lambda c : c['gTrainerFrontPicTable'] + 1000,
    'blue_palette':                lambda c : c['sObjectEventSpritePalettes'] + 16,
    'blue_palette_battle_front_1': lambda c : c['gTrainerFrontPicPaletteTable'] + 848,
    'blue_palette_battle_front_2': lambda c : c['gTrainerFrontPicPaletteTable'] + 992,
    'blue_palette_battle_front_3': lambda c : c['gTrainerFrontPicPaletteTable'] + 1000,
}

FR_LG_OVERWORLD_SPRITE_ADDRESSES = {
    'red_walking_running':  lambda c : [ c['gObjectEventGraphicsInfoPointers'] + 0 ],
    'red_bike':             lambda c : [ c['gObjectEventGraphicsInfoPointers'] + 4 ],
    'red_surfing':          lambda c : [ c['gObjectEventGraphicsInfoPointers'] + 8 ],
    'red_field_move':       lambda c : [ c['gObjectEventGraphicsInfoPointers'] + 12, c['gObjectEventGraphicsInfoPointers'] + 20 ],
    'red_fishing':          lambda c : [ c['gObjectEventGraphicsInfoPointers'] + 16 ],
    'red_bike_vs_seeker':   lambda c : [ c['gObjectEventGraphicsInfoPointers'] + 24 ],
    'leaf_walking_running': lambda c : [ c['gObjectEventGraphicsInfoPointers'] + 28 ],
    'leaf_bike':            lambda c : [ c['gObjectEventGraphicsInfoPointers'] + 32 ],
    'leaf_surfing':         lambda c : [ c['gObjectEventGraphicsInfoPointers'] + 36 ],
    'leaf_field_move':      lambda c : [ c['gObjectEventGraphicsInfoPointers'] + 40, c['gObjectEventGraphicsInfoPointers'] + 48 ],
    'leaf_fishing':         lambda c : [ c['gObjectEventGraphicsInfoPointers'] + 44 ],
    'leaf_bike_vs_seeker':  lambda c : [ c['gObjectEventGraphicsInfoPointers'] + 52 ],
}

FR_LG_OVERWORLD_PALETTE_IDS = {
    'Red': 0x1100,
    'Leaf': 0x1110
}

FIRERED_DATA_ADDRESSES_ORIGINAL = {
    'LoadObjectEventPalette': 0x05f4b0,
    'PatchObjectPalette': 0x05f538,
    'FindObjectEventPaletteIndexByTag': 0x05f5a0,
    'gSpeciesInfo': 0x254784,
    'gLevelUpLearnsets': 0x25d7b4,
    'gMonFrontPicTable': 0x2350ac,
    'gMonBackPicTable': 0x23654c,
    'gMonIconTable': 0x3d37a0,
    'gMonFootprintTable': 0x43fab0,
    'gMonPaletteTable': 0x23730c,
    'gMonShinyPaletteTable': 0x2380cc,
    'gMonIconPaletteIndices': 0x3d3e80,
    'sEggPalette': 0x25f842,
    'sEggHatchTiles': 0x25f862,
    'gObjectEventGraphicsInfoPointers': 0x39fdb0,
    'sObjectEventSpritePalettes': 0x3a5158,
    'gTrainerFrontPicTable': 0x23957c,
    'gTrainerFrontPicPaletteTable': 0x239a1c,
    'gTrainerBackAnimsPtrTable': 0x239f74,
    'gTrainerBackPicTable': 0x239fa4,
    'gTrainerBackPicPaletteTable': 0x239fd4,
    'sTrainerBackSpriteTemplates': 0x25df50,
    'gObjectEventSpriteOamTables_16x16': 0x50954c,
    'gObjectEventSpriteOamTables_16x32': 0x5095a0,
    'gObjectEventSpriteOamTables_32x32': 0x5095f4,
}
FIRERED_REV1_DATA_ADDRESSES_ORIGINAL = {
    'LoadObjectEventPalette': 0x05f4c4,
    'PatchObjectPalette': 0x05f54c,
    'FindObjectEventPaletteIndexByTag': 0x05f5b4,
    'gSpeciesInfo': 0x2547f4,
    'gLevelUpLearnsets': 0x25d824,
    'gMonFrontPicTable': 0x23511c,
    'gMonBackPicTable': 0x2365bc,
    'gMonIconTable': 0x3d3810,
    'gMonFootprintTable': 0x43fb20,
    'gMonPaletteTable': 0x23737c,
    'gMonShinyPaletteTable': 0x23813c,
    'gMonIconPaletteIndices': 0x3d3ef0,
    'sEggPalette': 0x25f8b2,
    'sEggHatchTiles': 0x25f8d2,
    'gObjectEventGraphicsInfoPointers': 0x39fe20,
    'sObjectEventSpritePalettes': 0x3a51c8,
    'gTrainerFrontPicTable': 0x2395ec,
    'gTrainerFrontPicPaletteTable': 0x239a8c,
    'gTrainerBackAnimsPtrTable': 0x239fe4,
    'gTrainerBackPicTable': 0x23a014,
    'gTrainerBackPicPaletteTable': 0x23a044,
    'sTrainerBackSpriteTemplates': 0x25dfc0,
    'gObjectEventSpriteOamTables_16x16': 0x3a37b8,
    'gObjectEventSpriteOamTables_16x32': 0x3a380c,
    'gObjectEventSpriteOamTables_32x32': 0x3a3860,
}
LEAFGREEN_DATA_ADDRESSES_ORIGINAL = {
    'LoadObjectEventPalette': 0x05f4b0,
    'PatchObjectPalette': 0x05f538,
    'FindObjectEventPaletteIndexByTag': 0x05f5a0,
    'gSpeciesInfo': 0x254760,
    'gLevelUpLearnsets': 0x25d794,
    'gMonFrontPicTable': 0x235088,
    'gMonBackPicTable': 0x236528,
    'gMonIconTable': 0x3d35dc,
    'gMonFootprintTable': 0x43f8ec,
    'gMonPaletteTable': 0x2372e8,
    'gMonShinyPaletteTable': 0x2380a8,
    'gMonIconPaletteIndices': 0x3d3cbc,
    'sEggPalette': 0x25f822,
    'sEggHatchTiles': 0x25f842,
    'gObjectEventGraphicsInfoPointers': 0x39fd90,
    'sObjectEventSpritePalettes': 0x3a5138,
    'gTrainerFrontPicTable': 0x239558,
    'gTrainerFrontPicPaletteTable': 0x2399f8,
    'gTrainerBackAnimsPtrTable': 0x239f50,
    'gTrainerBackPicTable': 0x239f80,
    'gTrainerBackPicPaletteTable': 0x239fb0,
    'sTrainerBackSpriteTemplates': 0x25df30,
    'gObjectEventSpriteOamTables_16x16': 0x3a3728,
    'gObjectEventSpriteOamTables_16x32': 0x3a377c,
    'gObjectEventSpriteOamTables_32x32': 0x3a37d0,
}
LEAFGREEN_REV1_DATA_ADDRESSES_ORIGINAL = {
    'LoadObjectEventPalette': 0x05f4c4,
    'PatchObjectPalette': 0x05f54c,
    'FindObjectEventPaletteIndexByTag': 0x05f5b4,
    'gSpeciesInfo': 0x2547d0,
    'gLevelUpLearnsets': 0x25d804,
    'gMonFrontPicTable': 0x2350f8,
    'gMonBackPicTable': 0x236598,
    'gMonIconTable': 0x3d364c,
    'gMonFootprintTable': 0x43f95c,
    'gMonPaletteTable': 0x237358,
    'gMonShinyPaletteTable': 0x238118,
    'gMonIconPaletteIndices': 0x3d3d2c,
    'sEggPalette': 0x25f892,
    'sEggHatchTiles': 0x25f8b2,
    'gObjectEventGraphicsInfoPointers': 0x39fe00,
    'sObjectEventSpritePalettes': 0x3a51a8,
    'gTrainerFrontPicTable': 0x2395c8,
    'gTrainerFrontPicPaletteTable': 0x239a68,
    'gTrainerBackAnimsPtrTable': 0x239fc0,
    'gTrainerBackPicTable': 0x239ff0,
    'gTrainerBackPicPaletteTable': 0x23a020,
    'sTrainerBackSpriteTemplates': 0x25dfa0,
    'gObjectEventSpriteOamTables_16x16': 0x3a3798,
    'gObjectEventSpriteOamTables_16x32': 0x3a37ec,
    'gObjectEventSpriteOamTables_32x32': 0x3a3840,
}

FR_LG_DATA_ADDRESS_BEGINNING = 0xA00000
FR_LG_DATA_ADDRESS_END = 0xCFFFFF

FR_LG_DATA_ADDRESS_INFOS = {
    **EMERALD_DATA_ADDRESS_INFOS,
    'Firered': {
        'crc32': 0xdd88761c,
        'original_addresses': FIRERED_DATA_ADDRESSES_ORIGINAL,
        'ap_addresses': {k: v['firered'] for k, v in data.rom_addresses.items()},
        'data_address_beginning': FR_LG_DATA_ADDRESS_BEGINNING,
        'data_address_end': FR_LG_DATA_ADDRESS_END
    },
    'Firered_rev1': {
        'crc32': 0x84ee4776,
        'original_addresses': FIRERED_REV1_DATA_ADDRESSES_ORIGINAL,
        'ap_addresses': {k: v['firered_rev1'] for k, v in data.rom_addresses.items()},
        'data_address_beginning': FR_LG_DATA_ADDRESS_BEGINNING,
        'data_address_end': FR_LG_DATA_ADDRESS_END
    },
    'Leafgreen': {
        'crc32': 0xd69c96cc,
        'original_addresses': LEAFGREEN_DATA_ADDRESSES_ORIGINAL,
        'ap_addresses': {k: v['leafgreen'] for k, v in data.rom_addresses.items()},
        'data_address_beginning': FR_LG_DATA_ADDRESS_BEGINNING,
        'data_address_end': FR_LG_DATA_ADDRESS_END
    },
    'Leafgreen_rev1': {
        'crc32': 0xdaffecec,
        'original_addresses': LEAFGREEN_REV1_DATA_ADDRESSES_ORIGINAL,
        'ap_addresses': {k: v['leafgreen_rev1'] for k, v in data.rom_addresses.items()},
        'data_address_beginning': FR_LG_DATA_ADDRESS_BEGINNING,
        'data_address_end': FR_LG_DATA_ADDRESS_END
    }
}

FR_LG_VALID_OVERWORLD_SPRITE_SIZES = [
    { 'width': 16, 'height': 16, 'data': 'gObjectEventSpriteOamTables_16x16' },
    { 'width': 16, 'height': 32, 'data': 'gObjectEventSpriteOamTables_16x32' },
    { 'width': 32, 'height': 32, 'data': 'gObjectEventSpriteOamTables_32x32' },
]

FR_LG_SPRITES_REQUIREMENTS = {
    'pokemon_front':             { 'frames': [1, 2], 'width': 64, 'height': 64 },
    'pokemon_back':              { 'frames': 1,      'width': 64, 'height': 64 },
    'pokemon_icon':              { 'frames': 2,      'width': 32, 'height': 32, 'palette': VALID_ICON_PALETTES },
    'pokemon_footprint':         { 'frames': 1,      'width': 16, 'height': 16, 'palette_size': 2, 'palette': VALID_FOOTPRINT_PALETTE },
    'pokemon_hatch_anim':        { 'frames': 1,      'width': 32, 'height': 136 },
    'trainer_walking_running':   { 'frames': 20,     'width': 16, 'height': 32, 'palette': VALID_WEAK_OVERWORLD_PALETTE },
    'trainer_bike':              { 'frames': 9,      'width': 32, 'height': 32, 'palette': VALID_WEAK_OVERWORLD_PALETTE },
    'trainer_surfing':           { 'frames': 12,     'width': 16, 'height': 32, 'palette': VALID_WEAK_OVERWORLD_PALETTE },
    'trainer_field_move':        { 'frames': 9,      'width': 16, 'height': 32, 'palette': VALID_WEAK_OVERWORLD_PALETTE },
    'trainer_fishing':           { 'frames': 12,     'width': 32, 'height': 32, 'palette': VALID_WEAK_OVERWORLD_PALETTE },
    'trainer_bike_vs_seeker':    { 'frames': 6,      'width': 32, 'height': 32, 'palette': VALID_WEAK_OVERWORLD_PALETTE },
    'trainer_battle_front':      { 'frames': 1,      'width': 64, 'height': 64 },
    'trainer_battle_back':       { 'frames': [4, 5], 'width': 64, 'height': 64, 'internal_frames': 5 },
    'trainer_battle_back_throw': { 'frames': [4, 5], 'width': 64, 'height': 64, 'internal_frames': 5 },
    'strainr_walking':           { 'frames': 10,     'width': 16, 'height': 32, 'palette': VALID_OVERWORLD_PALETTE },
    'strainr_battle_front':      { 'frames': 1,      'width': 64, 'height': 64 },
}

FR_LG_SPRITES_REQUIREMENTS_EXCEPTIONS = {
    'Castform': {
        'pokemon_front':      { 'frames': 4, 'palette_size': 16, 'palettes': 4, 'palette_per_frame': True },
        'pokemon_back':       { 'frames': 4, 'palette_size': 16, 'palettes': 4, 'palette_per_frame': True },
    },
    'Deoxys': {
        'pokemon_front':      { 'frames': 2 },
        'pokemon_back':       { 'frames': 2 },
        'pokemon_icon':       { 'frames': 4 },
    },
    'Unown A': {
        'pokemon_front':  { 'palette': VALID_UNOWN_PALETTE },
        'pokemon_back':   { 'palette': VALID_UNOWN_PALETTE },
        'pokemon_sfront': { 'palette': VALID_UNOWN_SHINY_PALETTE },
        'pokemon_sback':  { 'palette': VALID_UNOWN_SHINY_PALETTE },
    },
    'Blue': {
        'strainr_walking':        { 'frames': 9 },
        'strainr_battle_front_1': { 'frames': 1, 'width': 64, 'height': 64 },
        'strainr_battle_front_2': { 'frames': 1, 'width': 64, 'height': 64 },
        'strainr_battle_front_3': { 'frames': 1, 'width': 64, 'height': 64 },
    }
}