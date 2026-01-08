from typing import Dict, Set
from BaseClasses import Location
from . import names


class DWLocation(Location):
    game = "Dragon Warrior"

# Dev notes I'm just leaving here:
# Chests in DQ1 are stored as 4 bytes in the ROM, Map ID,X,Y,Contents. There is nothing stored to determine if a chest
# ever been opened before if it contains gold or a consumable, only that certain chests with key items don't spawn if
# the player has them in their inventory. However, data for chests opened on the CURRENT MAP are stored in the
# NES System Bus from address 0x601C to 0x602B, where each two bytes are the X and Y coords of the checked chest. The
# game compares these values with the current map to determine which chests to unload. Using this, we can set the
# location checks for these chests to be a 3 byte ID, building it from the Map ID stored in the RAM at 0x0045 with
# the two location bytes stored in the System Bus between 0x601C to 0x602B.

##########
# Default #
##########
# These locations are always on regardless of any -sanity options.
# This includes 31 chests, 2 checks with rescuing Gwaelin, and the Rainbow Drop / Ball of Light as locked items

throne_room_locations = {
    names.tantegel_throne_room_gold_chest: 0x050404,
    names.tantegel_throne_room_key_chest: 0x050601,
    names.tantegel_throne_room_torch_chest: 0x050504,
}

mountain_cave_locations = {
    names.mountain_cave_1_chest: 0x160D05,

    names.mountain_cave_2_chest_1: 0x170106,
    names.mountain_cave_2_chest_2: 0x170302,
    names.mountain_cave_2_chest_3: 0x170202,
    names.mountain_cave_2_chest_4: 0x170A09,
}

erdricks_cave_locations = {
    names.erdrick_tablet: 0x1D0903,
}

tantegel_castle_locations = {  # Requires Magic Key
    names.tantegel_castle_gold_chest_1: 0x04010D,
    names.tantegel_castle_gold_chest_2: 0x04010F,
    names.tantegel_castle_gold_chest_3: 0x04020E,
    names.tantegel_castle_gold_chest_4: 0x04030F,
    names.tantegel_castle_basement: 0x0C0405,
}

garinham_key_locations = {  # Requires Magic Key
    names.garinham_chest_1: 0x090805,
    names.garinham_chest_2: 0x090806,
    names.garinham_chest_3: 0x090905,
}

rimuldar_key_locations = {  # Requires Magic Key
    names.rimuldar_inn_chest: 0x0B1817,
}

garins_grave_locations = {  # Requires Magic Key
    names.garins_grave_1_chest_1: 0x180B00,
    names.garins_grave_1_chest_2: 0x180C00,
    names.garins_grave_1_chest_3: 0x180D00,

    names.garins_grave_3_chest_1: 0x1A0101,
    names.garins_grave_3_chest_2: 0x1A0D06,
}

swamp_cave_locations = {  # Requires Magic Key
    names.gwaelin_rescue: 0x150513,
    names.gwaelins_love_location: 0x050304,
}

shrine_of_rain_locations = {  # Requires Silver Harp
    names.staff_of_rain_location: 0x0D0304,
}

# Requires Stones of Sunlight & Staff of Rain (& Erdrick's Token if Searchsanity enabled)
# This location is always locked to the Rainbow Drop.
rainbow_shrine_locations = {
    names.rainbow_drop_location: 0xFF
}

charlock_locations = {  # Requires Rainbow Drop + Magic Key
    names.charlock_castle_erdrick_sword: 0x100505,

    names.charlock_castle_chest_1: 0x060B0B,
    names.charlock_castle_chest_2: 0x060B0C,
    names.charlock_castle_chest_3: 0x060B0D,
    names.charlock_castle_chest_4: 0x060C0C,
    names.charlock_castle_chest_5: 0x060C0D,
    names.charlock_castle_chest_6: 0x060D0D,

    names.ball_of_light_location: 0xDD  # Victory!
}

#############
# Level-Ups #
#############
# These checks are enabled with the Levelsanity option.
# These add between 1-29 checks depending on the LevelsanityRange option.

level_locations = {
    names.level_2: 0xD02,
    names.level_3: 0xD03,
    names.level_4: 0xD04,
    names.level_5: 0xD05,
    names.level_6: 0xD06,
    names.level_7: 0xD07,
    names.level_8: 0xD08,
    names.level_9: 0xD09,
}

# Levels above 9 have the Magic Key in logic so worst-case the player doesn't need to grind
# to max level in starting areas.
high_level_locations = {
    names.level_10: 0xD10,
    names.level_11: 0xD11,
    names.level_12: 0xD12,
    names.level_13: 0xD13,
    names.level_14: 0xD14,
    names.level_15: 0xD15,
    names.level_16: 0xD16,
    names.level_17: 0xD17,
    names.level_18: 0xD18,
    names.level_19: 0xD19,
    names.level_20: 0xD20,
    names.level_21: 0xD21,
    names.level_22: 0xD22,
    names.level_23: 0xD23,
    names.level_24: 0xD24,
    names.level_25: 0xD25,
    names.level_26: 0xD26,
    names.level_27: 0xD27,
    names.level_28: 0xD28,
    names.level_29: 0xD29,
    names.level_30: 0xD30,
}

############
# Searches #
############
# These 3 locations are enabled with the Searchsanity option.
# Their respective key items are also added to the multiworld itempool if enabled.

kol_locations = {
    names.fairy_flute_location: 0xE40
}

hauksness_locations = {
    names.erdricks_armor_location: 0xE20,
}

erdricks_token_locations = {
    names.erdricks_token_location: 0xE80
}

#############
# Equipment #
#############
# These 15 locations are enabled with the Shopsanity option.
# Buying a piece of equipment will send the associated check instead rather than actually obtaining it,
# instead equipment is gained through new Progressive Weapon/Armor/Shield items placed in the itempool.
# Region connection rules are also updated to account for equipment as progression items.
#
# NOTE: Some equipment appears in multiple shops, region placement is simply the earliest opportunity.

brecconary_locations = {
    names.bamboo_pole: 0x20,
    names.club: 0x40,
    names.copper_sword: 0x60,

    names.clothes: 0x4,
    names.leather_armor: 0x8,

    names.small_shield: 0x1
}

garinham_locations = {
    names.chain_mail: 0xC,
    names.large_shield: 0x2
}

kol_shop_locations = {
    names.hand_axe: 0x80,
    names.half_plate: 0x10,
    names.full_plate: 0x14,
}

rimuldar_locations = {
    names.broad_sword: 0xA0,
    names.magic_armor: 0x18,
}

cantlin_locations = {  # Requires Magic Key
    names.flame_sword: 0xC0,
    names.silver_shield: 0x3
}

############
# Monsters #
############
# These 40 checks are enabled with the Monstersanity option.
# Defeating a monster for the first time sends it's associated check.
#
# NOTE: Several monsters appear in multiple locations, region placement is simply the earliest opportunity,
# otherwise roughly ordered by internal ID.

brecconary_monster_locations = {
    names.slime: 0xDEF00,
    names.red_slime: 0xDEF02,
    names.drakee: 0xDEF04
}

garinham_monster_locations = {
    names.ghost: 0xDEF06,
    names.magician: 0xDEF08
}

kol_monster_locations = {
    names.magidrakee: 0xDEF0A,
    names.scorpion: 0xDEF0C,
}

mountain_cave_monster_locations = {
    names.druin: 0xDEF0E,
    names.poltergeist: 0xDEF10,
    names.droll: 0xDEF12,
    names.drakeema: 0xDEF14,
    names.skeleton: 0xDEF16,
    names.warlock: 0xDEF18
}

rimuldar_monster_locations = {
    names.metal_scorpion: 0xDEF1A,
    names.wolf: 0xDEF1C,
    names.wraith: 0xDEF1E,
    names.wolflord: 0xDEF24,
    names.goldman: 0xDEF32,
}

cantlin_monster_locations = {
    names.metal_slime: 0xDEF20,
    names.specter: 0xDEF22,
    names.druinlord: 0xDEF26,
    names.drollmagi: 0xDEF28,
    names.wyvern: 0xDEF2A,
    names.rogue_scorpion: 0xDEF2C,
    names.wraith_knight: 0xDEF2E,
    names.knight: 0xDEF34,
    names.magiwyvern: 0xDEF36,
    names.demon_knight: 0xDEF38,
    names.werewolf: 0xDEF3A,
    names.starwyvern: 0xDEF3E,
    names.wizard: 0xDEF40
}

swamp_cave_monster_locations = {  # Requires Magic Key
    names.green_dragon: 0xDEF3C
}

hauksness_monster_locations = {
    names.axe_knight: 0xDEF42
}

charlock_monster_locations = {  # Requires Rainbow Drop + Magic Key
    names.blue_dragon: 0xDEF44,
    names.stoneman: 0xDEF46,
    names.armored_knight: 0xDEF48,
    names.red_dragon: 0xDEF4A,
}

charlock_dragonlord_locations = {  # Requires Rainbow Drop + Magic Key (+ Max Equipment if Shopsanity)
    # Golem is here so it doesn't self-lock fairy flute
    names.golem: 0xDEF30,
    names.dragonlord_1: 0xDEF4C,
    names.dragonlord_2: 0xDEF4E
}

all_locations = {
    **throne_room_locations,
    **tantegel_castle_locations,
    **brecconary_locations,
    **garinham_locations,
    **garinham_key_locations,
    **kol_locations,
    **kol_shop_locations,
    **rimuldar_locations,
    **rimuldar_key_locations,
    **cantlin_locations,
    **mountain_cave_locations,
    **swamp_cave_locations,
    **garins_grave_locations,
    **charlock_locations,
    **hauksness_locations,
    **erdricks_cave_locations,
    **shrine_of_rain_locations,
    **erdricks_token_locations,
    **rainbow_shrine_locations,
    **level_locations,
    **high_level_locations,
    **brecconary_monster_locations,
    **garinham_monster_locations,
    **kol_monster_locations,
    **mountain_cave_monster_locations,
    **rimuldar_monster_locations,
    **cantlin_monster_locations,
    **swamp_cave_monster_locations,
    **hauksness_monster_locations,
    **charlock_monster_locations,
    **charlock_dragonlord_locations
}

location_names: Dict[str, Set[str]] = { 
    "Tantegel Castle": set(name for name in list(throne_room_locations.keys()) + list(tantegel_castle_locations.keys())),
    "Brecconary": set(name for name in list(brecconary_locations.keys()) + list(brecconary_monster_locations.keys())),
    "Garinham": set(name for name in list(garinham_locations.keys()) + list(garinham_key_locations.keys()) + list(garinham_monster_locations.keys())),
    "Kol": set(name for name in list(kol_locations.keys()) + list(kol_shop_locations.keys()) + list(kol_monster_locations.keys())),
    "Rimuldar": set(name for name in list(rimuldar_locations.keys()) + list(rimuldar_key_locations.keys()) + list(rimuldar_monster_locations.keys())),
    "Cantlin": set(name for name in list(cantlin_locations.keys()) + list(cantlin_monster_locations.keys())),
    "Mountain Cave": set(name for name in list(mountain_cave_locations.keys()) + list(mountain_cave_monster_locations.keys())),
    "Swamp Cave": set(name for name in list(swamp_cave_locations.keys()) + list(swamp_cave_monster_locations.keys())),
    "Garin's Grave": set(name for name in garins_grave_locations.keys()),
    "Charlock": set(name for name in list(charlock_locations.keys()) + list(charlock_monster_locations.keys()) + list(charlock_dragonlord_locations.keys())),
    "Hauksness": set(name for name in list(hauksness_locations.keys()) + list(hauksness_monster_locations.keys())),
    "Erdrick's Grave": set([names.erdrick_tablet]),
    "Staff of Rain Shrine": set([names.staff_of_rain_location]),
    "Rainbow Drop Shrine": set([names.rainbow_drop_location]),
    "Erdrick's Token": set([names.erdricks_token_location]),
    "Level Ups": set(name for name in list(level_locations.keys()) + list(high_level_locations.keys())),
}

def create_locations(levels: int):
    temp_level_locations = {}
    temp_high_level_locations = {}

    if levels > 1:
        for level in range(2, min(levels + 1, 10)):
            temp_level_locations["Level " + str(level)] = int('0xD0' + str(level), 16)
        for level in range(10, levels + 1):
            temp_high_level_locations["Level " + str(level)] = int('0xD' + str(level), 16)

    return (temp_level_locations, temp_high_level_locations)


lookup_location_to_id: Dict[str, int] = {location: idx for location, idx in all_locations.items() if idx is not None}

