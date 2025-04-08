from typing import Dict, List, NamedTuple

from BaseClasses import Item, ItemClassification

BASE_ITEM_ID = 4000


class LandstalkerItem(Item):
    game: str = "Landstalker - The Treasures of King Nole"
    price_in_shops: int


class LandstalkerItemData(NamedTuple):
    id: int
    classification: ItemClassification
    price_in_shops: int
    quantity: int = 1


item_table: Dict[str, LandstalkerItemData] = {
    "EkeEke":               LandstalkerItemData(0,  ItemClassification.filler,      20,     0),  # Variable amount
    "Magic Sword":          LandstalkerItemData(1,  ItemClassification.useful,      300),
    "Sword of Ice":         LandstalkerItemData(2,  ItemClassification.useful,      300),
    "Thunder Sword":        LandstalkerItemData(3,  ItemClassification.useful,      500),
    "Sword of Gaia":        LandstalkerItemData(4,  ItemClassification.progression, 300),
    "Fireproof":            LandstalkerItemData(5,  ItemClassification.progression, 150),
    "Iron Boots":           LandstalkerItemData(6,  ItemClassification.progression, 150),
    "Healing Boots":        LandstalkerItemData(7,  ItemClassification.useful,      300),
    "Snow Spikes":          LandstalkerItemData(8,  ItemClassification.progression, 400),
    "Steel Breast":         LandstalkerItemData(9,  ItemClassification.useful,      200),
    "Chrome Breast":        LandstalkerItemData(10, ItemClassification.useful,      350),
    "Shell Breast":         LandstalkerItemData(11, ItemClassification.useful,      500),
    "Hyper Breast":         LandstalkerItemData(12, ItemClassification.useful,      700),
    "Mars Stone":           LandstalkerItemData(13, ItemClassification.useful,      150),
    "Moon Stone":           LandstalkerItemData(14, ItemClassification.useful,      150),
    "Saturn Stone":         LandstalkerItemData(15, ItemClassification.useful,      200),
    "Venus Stone":          LandstalkerItemData(16, ItemClassification.useful,      300),
    # Awakening Book: 17
    "Detox Grass":          LandstalkerItemData(18, ItemClassification.filler,      25,     9),
    "Statue of Gaia":       LandstalkerItemData(19, ItemClassification.filler,      75,     12),
    "Golden Statue":        LandstalkerItemData(20, ItemClassification.filler,      150,    10),
    "Mind Repair":          LandstalkerItemData(21, ItemClassification.filler,      25,     7),
    "Casino Ticket":        LandstalkerItemData(22, ItemClassification.progression, 50),
    "Axe Magic":            LandstalkerItemData(23, ItemClassification.progression, 400),
    "Blue Ribbon":          LandstalkerItemData(24, ItemClassification.filler,      50),
    "Buyer Card":           LandstalkerItemData(25, ItemClassification.progression, 150),
    "Lantern":              LandstalkerItemData(26, ItemClassification.progression, 200),
    "Garlic":               LandstalkerItemData(27, ItemClassification.progression, 150,    2),
    "Anti Paralyze":        LandstalkerItemData(28, ItemClassification.filler,      20,     7),
    "Statue of Jypta":      LandstalkerItemData(29, ItemClassification.useful,      250),
    "Sun Stone":            LandstalkerItemData(30, ItemClassification.progression, 300),
    "Armlet":               LandstalkerItemData(31, ItemClassification.progression, 300),
    "Einstein Whistle":     LandstalkerItemData(32, ItemClassification.progression, 200),
    "Blue Jewel":           LandstalkerItemData(33, ItemClassification.progression, 500,    0),  # Detox Book in base game
    "Yellow Jewel":         LandstalkerItemData(34, ItemClassification.progression, 500,    0),  # AntiCurse Book in base game
    # Record Book: 35
    # Spell Book: 36
    # Hotel Register: 37
    # Island Map: 38
    "Lithograph":           LandstalkerItemData(39, ItemClassification.progression, 250),
    "Red Jewel":            LandstalkerItemData(40, ItemClassification.progression, 500,    0),
    "Pawn Ticket":          LandstalkerItemData(41, ItemClassification.useful,      200,    4),
    "Purple Jewel":         LandstalkerItemData(42, ItemClassification.progression, 500,    0),
    "Gola's Eye":           LandstalkerItemData(43, ItemClassification.progression, 400),
    "Death Statue":         LandstalkerItemData(44, ItemClassification.filler,      150),
    "Dahl":                 LandstalkerItemData(45, ItemClassification.filler,      100,    18),
    "Restoration":          LandstalkerItemData(46, ItemClassification.filler,      40,     9),
    "Logs":                 LandstalkerItemData(47, ItemClassification.progression, 100,    2),
    "Oracle Stone":         LandstalkerItemData(48, ItemClassification.progression, 250),
    "Idol Stone":           LandstalkerItemData(49, ItemClassification.progression, 200),
    "Key":                  LandstalkerItemData(50, ItemClassification.progression, 150),
    "Safety Pass":          LandstalkerItemData(51, ItemClassification.progression, 250),
    "Green Jewel":          LandstalkerItemData(52, ItemClassification.progression, 500,    0),  # No52 in base game
    "Bell":                 LandstalkerItemData(53, ItemClassification.useful,      200),
    "Short Cake":           LandstalkerItemData(54, ItemClassification.useful,      250),
    "Gola's Nail":          LandstalkerItemData(55, ItemClassification.progression, 800),
    "Gola's Horn":          LandstalkerItemData(56, ItemClassification.progression, 800),
    "Gola's Fang":          LandstalkerItemData(57, ItemClassification.progression, 800),
    # Broad Sword: 58
    # Leather Breast: 59
    # Leather Boots: 60
    # No Ring: 61
    "Life Stock":           LandstalkerItemData(62, ItemClassification.filler,      250,    0),  # Variable amount
    "No Item":              LandstalkerItemData(63, ItemClassification.filler,      0,      0),
    "1 Gold":               LandstalkerItemData(64, ItemClassification.filler,      1),
    "20 Golds":             LandstalkerItemData(65, ItemClassification.filler,      20,     15),
    "50 Golds":             LandstalkerItemData(66, ItemClassification.filler,      50,     7),
    "100 Golds":            LandstalkerItemData(67, ItemClassification.filler,      100,    5),
    "200 Golds":            LandstalkerItemData(68, ItemClassification.useful,      200,    2),

    "Progressive Armor":    LandstalkerItemData(69, ItemClassification.useful,      250,    0),
    "Kazalt Jewel":         LandstalkerItemData(70, ItemClassification.progression, 500,    0)
}


def get_weighted_filler_item_names():
    weighted_item_names: List[str] = []
    for name, data in item_table.items():
        if data.classification == ItemClassification.filler:
            weighted_item_names += [name for _ in range(data.quantity)]
    return weighted_item_names


def build_item_name_to_id_table():
    return {name: data.id + BASE_ITEM_ID for name, data in item_table.items()}
