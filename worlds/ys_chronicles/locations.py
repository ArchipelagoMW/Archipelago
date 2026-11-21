"""
Ys I Chronicles - Location Definitions

All locations (checks) that can contain randomized items.
Memory flags verified from PC version (ys1plus.exe) — see docs/flag_mapping_guide.md.
"""

from typing import Dict, NamedTuple
from enum import IntEnum


class YsLocationType(IntEnum):
    """Location type categories."""
    CHEST = 0
    NPC = 1
    BOSS = 2
    EVENT = 3
    PICKUP = 4
    SHOP = 5


class YsLocationData(NamedTuple):
    """Location definition."""
    code: int             # AP location ID
    region: str           # Which region this belongs to
    loc_type: YsLocationType
    vanilla_item: str     # Item here in vanilla game
    memory_flag: int      # Primary flag address to poll (0→1 unless noted)


# Base ID for Ys I locations
YS1_LOCATION_BASE_ID = 0x59530000

# =============================================================================
# Location Definitions
# =============================================================================

YS1_LOCATIONS: Dict[str, YsLocationData] = {
    # -------------------------------------------------------------------------
    # Barbado Port
    # -------------------------------------------------------------------------
    "Slaff's Gift": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 2, region="Barbado",
        loc_type=YsLocationType.NPC, vanilla_item="Short Sword",
        memory_flag=0x531B20,
    ),

    # -------------------------------------------------------------------------
    # Minea (Starting Town)
    # -------------------------------------------------------------------------
    "Sara's Gift": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 1, region="Minea",
        loc_type=YsLocationType.NPC, vanilla_item="Sara's Crystal",
        memory_flag=0x531BB4,  # gift flag (also has cutscene flag 0x531BAC)
    ),
    "Franz's Gift": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 31, region="Minea",
        loc_type=YsLocationType.NPC, vanilla_item="Book of Ys (Tovah)",
        memory_flag=0x531BC0,  # also has secondary 0x531BC4
    ),

    # -------------------------------------------------------------------------
    # Zepik Village
    # -------------------------------------------------------------------------
    "Jeba's Gift": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 3, region="Zepik",
        loc_type=YsLocationType.NPC, vanilla_item="Shrine Key",
        memory_flag=0x531C6C,  # also has secondary 0x53206C
    ),
    "Silver Bell Reward": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 4, region="Zepik",
        loc_type=YsLocationType.NPC, vanilla_item="Power Ring",
        memory_flag=0x531CAC,  # Mayor Robels
    ),
    "Slaff's Second Gift": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 5, region="Zepik",
        loc_type=YsLocationType.NPC, vanilla_item="Talwar",
        memory_flag=0x531B2C,  # also has secondary 0x531B44
    ),

    # -------------------------------------------------------------------------
    # Minea Fields / Roda Trees
    # -------------------------------------------------------------------------
    "Minea Fields - Golden Vase": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 7, region="Minea Fields",
        loc_type=YsLocationType.PICKUP, vanilla_item="Golden Vase",
        memory_flag=0x531C28,
    ),
    "Minea Fields - Bestiary Potion Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 8, region="Minea Fields",
        loc_type=YsLocationType.CHEST, vanilla_item="Bestiary Potion",
        memory_flag=0x531894,
    ),
    "Minea Fields - Locked Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 9, region="Minea Fields",
        loc_type=YsLocationType.CHEST, vanilla_item="Piece of Paper",
        memory_flag=0x531898,
    ),
    "Southern Roda Tree": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 6, region="Minea Fields",
        loc_type=YsLocationType.EVENT, vanilla_item="Silver Sword",
        memory_flag=0x531C30,  # REVERSE FLAG: 1→0 when claimed
    ),

    # -------------------------------------------------------------------------
    # Shrine F1
    # -------------------------------------------------------------------------
    "Shrine F1 - Shield Ring Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 11, region="Shrine",
        loc_type=YsLocationType.CHEST, vanilla_item="Shield Ring",
        memory_flag=0x5318A0,  # locked chest
    ),
    "Shrine F1 - Ruby Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 10, region="Shrine",
        loc_type=YsLocationType.CHEST, vanilla_item="Ruby",
        memory_flag=0x5318A4,
    ),
    "Shrine F1 - Necklace Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 12, region="Shrine",
        loc_type=YsLocationType.CHEST, vanilla_item="Necklace",
        memory_flag=0x5318A8,  # locked chest
    ),

    # -------------------------------------------------------------------------
    # Shrine B2
    # -------------------------------------------------------------------------
    "Shrine B2 - Silver Bell Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 22, region="Shrine B2",
        loc_type=YsLocationType.CHEST, vanilla_item="Silver Bell",
        memory_flag=0x5318B0,
    ),
    "Shrine B2 - Mask of Eyes Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 23, region="Shrine B2",
        loc_type=YsLocationType.CHEST, vanilla_item="Mask of Eyes",
        memory_flag=0x5318AC,
    ),
    "Shrine B2 - Prison Key Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 20, region="Shrine B2",
        loc_type=YsLocationType.CHEST, vanilla_item="Prison Key",
        memory_flag=0x5318B4,
    ),
    "Shrine B2 - Treasure Box Key Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 21, region="Shrine B2",
        loc_type=YsLocationType.CHEST, vanilla_item="Treasure Box Key",
        memory_flag=0x5318B8,
    ),

    # -------------------------------------------------------------------------
    # Shrine B3
    # -------------------------------------------------------------------------
    "Shrine B3 - Marble Key Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 26, region="Shrine B3",
        loc_type=YsLocationType.CHEST, vanilla_item="Marble Key",
        memory_flag=0x5318BC,
    ),
    "Shrine B3 - Ivory Key Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 25, region="Shrine B3",
        loc_type=YsLocationType.CHEST, vanilla_item="Ivory Key",
        memory_flag=0x5318C0,
    ),
    "Shrine B3 - Silver Shield Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 28, region="Shrine B3",
        loc_type=YsLocationType.CHEST, vanilla_item="Silver Shield",
        memory_flag=0x5318C4,
    ),
    "Shrine B3 - Heal Potion Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 27, region="Shrine B3",
        loc_type=YsLocationType.CHEST, vanilla_item="Heal Potion",
        memory_flag=0x5318C8,
    ),
    "Shrine B3 - Volume Hadal Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 29, region="Shrine B3",
        loc_type=YsLocationType.CHEST, vanilla_item="Book of Ys (Hadal)",
        memory_flag=0x5318CC,
    ),
    "Boss: Jenocres": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 100, region="Shrine",
        loc_type=YsLocationType.BOSS, vanilla_item="Book of Ys (Hadal)",
        memory_flag=0x531950,
    ),

    # -------------------------------------------------------------------------
    # Mine F1
    # -------------------------------------------------------------------------
    "Mine F1 - Silver Armor Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 37, region="Mine F1",
        loc_type=YsLocationType.CHEST, vanilla_item="Silver Armor",
        memory_flag=0x5318D0,
    ),
    "Mine F1 - Heal Potion Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 35, region="Mine F1",
        loc_type=YsLocationType.CHEST, vanilla_item="Heal Potion",
        memory_flag=0x5318D4,
    ),
    "Mine F1 - Timer Ring Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 36, region="Mine F1",
        loc_type=YsLocationType.CHEST, vanilla_item="Timer Ring",
        memory_flag=0x5318D8,
    ),

    # -------------------------------------------------------------------------
    # Mine B1
    # -------------------------------------------------------------------------
    "Mine B1 - Heal Ring Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 40, region="Mine B1",
        loc_type=YsLocationType.CHEST, vanilla_item="Heal Ring",
        memory_flag=0x5318DC,
    ),
    "Mine B1 - Roda Tree Seed Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 42, region="Mine B1",
        loc_type=YsLocationType.CHEST, vanilla_item="Roda Tree Seed",
        memory_flag=0x5318E0,
    ),
    "Mine B1 - Silver Harmonica Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 41, region="Mine B1",
        loc_type=YsLocationType.CHEST, vanilla_item="Silver Harmonica",
        memory_flag=0x5318E4,
    ),

    # -------------------------------------------------------------------------
    # Mine B2
    # -------------------------------------------------------------------------
    "Mine B2 - Heal Potion Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 46, region="Mine B2",
        loc_type=YsLocationType.CHEST, vanilla_item="Heal Potion",
        memory_flag=0x5318E8,
    ),
    "Mine B2 - Darm Key Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 45, region="Mine B2",
        loc_type=YsLocationType.CHEST, vanilla_item="Darm Key",
        memory_flag=0x5318EC,
    ),
    "Mine B2 - Volume Dabbie Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 47, region="Mine B2",
        loc_type=YsLocationType.CHEST, vanilla_item="Book of Ys (Dabbie)",
        memory_flag=0x5318F0,
    ),
    "Boss: Nygtilger": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 101, region="Mine B1",
        loc_type=YsLocationType.BOSS, vanilla_item="Book of Ys (Dabbie)",
        memory_flag=0x531958,
    ),
    "Boss: Vagullion": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 102, region="Mine B2",
        loc_type=YsLocationType.BOSS, vanilla_item="Book of Ys (Dabbie)",
        memory_flag=0x531AC0,
    ),

    # -------------------------------------------------------------------------
    # Darm Tower - Lower (F1-F7)
    # -------------------------------------------------------------------------
    "Tower F2 - Heal Potion Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 50, region="Tower Lower",
        loc_type=YsLocationType.CHEST, vanilla_item="Heal Potion",
        memory_flag=0x5318FC,
    ),
    "Tower F2 - Mirror Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 51, region="Tower Lower",
        loc_type=YsLocationType.CHEST, vanilla_item="Mirror",
        memory_flag=0x531900,
    ),
    "Tower F2 - Evil Ring Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 53, region="Tower Lower",
        loc_type=YsLocationType.CHEST, vanilla_item="Evil Ring",
        memory_flag=0x531904,
    ),
    "Tower F2 - Talwar Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 52, region="Tower Lower",
        loc_type=YsLocationType.CHEST, vanilla_item="Talwar",
        memory_flag=0x531944,
    ),
    "Tower F4 - Reflex Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 54, region="Tower Lower",
        loc_type=YsLocationType.CHEST, vanilla_item="Reflex",
        memory_flag=0x531948,
    ),
    "Tower F6 - Large Shield Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 55, region="Tower Lower",
        loc_type=YsLocationType.CHEST, vanilla_item="Large Shield",
        memory_flag=0x53194C,
    ),
    "Tower F7 - Silver Sword Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 56, region="Tower Lower",
        loc_type=YsLocationType.CHEST, vanilla_item="Silver Sword",
        memory_flag=0x531914,
    ),

    # -------------------------------------------------------------------------
    # Darm Tower - F8 (Pictimos Boss)
    # -------------------------------------------------------------------------
    "Boss: Pictimos": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 103, region="Tower F8",
        loc_type=YsLocationType.BOSS, vanilla_item="Book of Ys (Mesa)",
        memory_flag=0x531968,
    ),

    # -------------------------------------------------------------------------
    # Darm Tower - Mid (F9-F13)
    # -------------------------------------------------------------------------
    "Tower F9 - Hammer Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 62, region="Tower Mid",
        loc_type=YsLocationType.CHEST, vanilla_item="Hammer",
        memory_flag=0x531918,
    ),
    "Tower F9 - Volume Mesa Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 63, region="Tower Mid",
        loc_type=YsLocationType.CHEST, vanilla_item="Book of Ys (Mesa)",
        memory_flag=0x53191C,
    ),
    "Tower F9 - Silver Shield Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 65, region="Tower Mid",
        loc_type=YsLocationType.CHEST, vanilla_item="Silver Shield",
        memory_flag=0x531920,
    ),
    "Tower F13 - Silver Armor Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 68, region="Tower Mid",
        loc_type=YsLocationType.CHEST, vanilla_item="Silver Armor",
        memory_flag=0x531924,
    ),
    "Dogi's Gift": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 66, region="Tower Mid",
        loc_type=YsLocationType.NPC, vanilla_item="Idol",
        memory_flag=0x531D38,
    ),
    "Raba Trade": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 67, region="Tower Mid",
        loc_type=YsLocationType.NPC, vanilla_item="Blue Necklace",
        memory_flag=0x531D00,  # also has 0x531D04
    ),
    "Reah's Gift": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 69, region="Tower Mid",
        loc_type=YsLocationType.NPC, vanilla_item="Monocle",
        memory_flag=0x531D64,
    ),
    "Luta Gemma's Gift": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 80, region="Tower Mid",
        loc_type=YsLocationType.NPC, vanilla_item="Blue Amulet",
        memory_flag=0x531D58,  # also has 0x531D5C
    ),

    # -------------------------------------------------------------------------
    # Darm Tower - F14 (Khonsclard Boss)
    # -------------------------------------------------------------------------
    "Tower F14 - Rod Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 72, region="Tower F14",
        loc_type=YsLocationType.CHEST, vanilla_item="Rod",
        memory_flag=0x531928,
    ),
    "Tower F14 - Volume Gemma Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 73, region="Tower F14",
        loc_type=YsLocationType.CHEST, vanilla_item="Book of Ys (Gemma)",
        memory_flag=0x53192C,
    ),
    "Boss: Khonsclard": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 104, region="Tower F14",
        loc_type=YsLocationType.BOSS, vanilla_item="Book of Ys (Gemma)",
        memory_flag=0x531978,
    ),

    # -------------------------------------------------------------------------
    # Darm Tower - Upper (F15-F21)
    # -------------------------------------------------------------------------
    "Tower F15 - Battle Shield Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 75, region="Tower Upper",
        loc_type=YsLocationType.CHEST, vanilla_item="Battle Shield",
        memory_flag=0x531930,
    ),
    "Tower F17 - Heal Potion Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 78, region="Tower Upper",
        loc_type=YsLocationType.CHEST, vanilla_item="Heal Potion",
        memory_flag=0x531934,
    ),
    "Tower F19 - Battle Armor Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 76, region="Tower Upper",
        loc_type=YsLocationType.CHEST, vanilla_item="Battle Armor",
        memory_flag=0x531938,
    ),
    "Tower F20 - Flame Sword Chest": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 77, region="Tower Upper",
        loc_type=YsLocationType.CHEST, vanilla_item="Flame Sword",
        memory_flag=0x53193C,
    ),
    "Boss: Yogleks & Omulgun": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 105, region="Tower Upper",
        loc_type=YsLocationType.BOSS, vanilla_item="Book of Ys (Fact)",
        memory_flag=0x531ACC,
    ),

    # -------------------------------------------------------------------------
    # Darm Tower - Top (F22-F25)
    # -------------------------------------------------------------------------
    "Boss: Dark Fact": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 106, region="Tower Upper",
        loc_type=YsLocationType.BOSS, vanilla_item="Book of Ys (Fact)",
        memory_flag=0x531A98,
    ),

    # -------------------------------------------------------------------------
    # Shops — Pim's (Minea)
    # -------------------------------------------------------------------------
    "Pim's Shop - Sapphire Ring": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 200, region="Minea",
        loc_type=YsLocationType.SHOP, vanilla_item="Sapphire Ring",
        memory_flag=0,  # detected by hook (caller 0x493475, game_id 41)
    ),
    "Pim's Shop - Mirror": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 201, region="Minea",
        loc_type=YsLocationType.SHOP, vanilla_item="Mirror",
        memory_flag=0,  # detected by hook (caller 0x493525, game_id 45)
    ),
    "Pim's Shop - Wing": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 202, region="Minea",
        loc_type=YsLocationType.SHOP, vanilla_item="Wing",
        memory_flag=0,  # detected by hook (caller 0x4935D5, game_id 47)
    ),

    # -------------------------------------------------------------------------
    # Shops — Weapon/Armor Dealer (Minea & Zepik)
    # -------------------------------------------------------------------------
    "Shop - Short Sword": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 210, region="Minea",
        loc_type=YsLocationType.SHOP, vanilla_item="Short Sword",
        memory_flag=0,  # game_id 0
    ),
    "Shop - Long Sword": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 211, region="Minea",
        loc_type=YsLocationType.SHOP, vanilla_item="Long Sword",
        memory_flag=0,  # game_id 1
    ),
    "Shop - Talwar": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 212, region="Zepik",
        loc_type=YsLocationType.SHOP, vanilla_item="Talwar",
        memory_flag=0,  # game_id 2
    ),
    "Shop - Small Shield": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 213, region="Minea",
        loc_type=YsLocationType.SHOP, vanilla_item="Small Shield",
        memory_flag=0,  # game_id 5
    ),
    "Shop - Middle Shield": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 214, region="Minea",
        loc_type=YsLocationType.SHOP, vanilla_item="Middle Shield",
        memory_flag=0,  # game_id 6
    ),
    "Shop - Large Shield": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 215, region="Zepik",
        loc_type=YsLocationType.SHOP, vanilla_item="Large Shield",
        memory_flag=0,  # game_id 7
    ),
    "Shop - Chain Mail": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 216, region="Minea",
        loc_type=YsLocationType.SHOP, vanilla_item="Chain Mail",
        memory_flag=0,  # game_id 10
    ),
    "Shop - Plate Mail": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 217, region="Minea",
        loc_type=YsLocationType.SHOP, vanilla_item="Plate Mail",
        memory_flag=0,  # game_id 11
    ),
    "Shop - Reflex": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 218, region="Zepik",
        loc_type=YsLocationType.SHOP, vanilla_item="Reflex",
        memory_flag=0,  # game_id 12
    ),
    "Shop - Heal Potion": YsLocationData(
        code=YS1_LOCATION_BASE_ID + 219, region="Minea",
        loc_type=YsLocationType.SHOP, vanilla_item="Heal Potion",
        memory_flag=0,  # game_id 44
    ),
}

# =============================================================================
# Reverse flag: Southern Roda Tree uses 1→0 instead of 0→1
# =============================================================================
REVERSE_FLAG_LOCATION_NAMES = {"Southern Roda Tree"}

# Set of flag addresses that use reverse logic (1→0 = checked)
REVERSE_FLAG_LOCATIONS: set = {
    data.memory_flag
    for name, data in YS1_LOCATIONS.items()
    if name in REVERSE_FLAG_LOCATION_NAMES and data.memory_flag
}

# =============================================================================
# Lookup Helpers
# =============================================================================

YS1_LOCATION_ID_TO_NAME: Dict[int, str] = {
    data.code: name for name, data in YS1_LOCATIONS.items()
}

location_name_to_id: Dict[str, int] = {
    name: data.code for name, data in YS1_LOCATIONS.items()
}

# Flag address -> AP location code (for client polling)
FLAG_TO_LOCATION: Dict[int, int] = {
    data.memory_flag: data.code
    for data in YS1_LOCATIONS.values()
    if data.memory_flag
}


def get_locations_in_region(region: str) -> list:
    return [n for n, d in YS1_LOCATIONS.items() if d.region == region]


def get_all_regions() -> set:
    return {d.region for d in YS1_LOCATIONS.values()}
